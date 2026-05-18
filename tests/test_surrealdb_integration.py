"""End-to-end SurrealDB integration tests using testcontainers."""

from __future__ import annotations

import json
import os
import re
import time
from collections import defaultdict
from pathlib import Path

import httpx
import pytest
from pydantic import BaseModel, ConfigDict, Field
from testcontainers.core.container import DockerContainer


ROOT = Path(__file__).resolve().parents[1]
SURREAL_DIR = ROOT / "surreal"

SCHEMA_META_PATH = SURREAL_DIR / "schema" / "schema-meta.surql"
SCHEMA_VOCABULARY_PATH = SURREAL_DIR / "schema" / "schemaorg-vocabulary.surql"
SCHEMA_PATHS_PATH = SURREAL_DIR / "schema" / "schemaorg-paths.surql"
KNOWLEDGE_GRAPH_PATH = SURREAL_DIR / "knowledge-graph.surql"
GRAPH_VALIDATION_PATH = SURREAL_DIR / "validation" / "graph-validation.surql"
RUNTIME_SCHEMA_PATH = SURREAL_DIR / "runtime-schema.surql"
RUNTIME_FUNCTIONS_PATH = SURREAL_DIR / "runtime-functions.surql"
RUNTIME_EVENTS_PATH = SURREAL_DIR / "runtime-events.surql"

SCHEMA_SUMMARY = json.loads((SURREAL_DIR / "schema" / "schemaorg-summary.json").read_text(encoding="utf-8"))
PATHS_SUMMARY = json.loads((SURREAL_DIR / "schema" / "schemaorg-paths-summary.json").read_text(encoding="utf-8"))

RUN_INTEGRATION = os.getenv("RUN_SURREALDB_INTEGRATION") == "1"
NULL_TOKEN = re.compile(r"(?<![A-Za-z0-9_])null(?![A-Za-z0-9_])")
JSON_CONTENT_PREFIXES = ("UPSERT schema_term:", "UPSERT schema_path:", "RELATE ")
SCHEMAORG_RELATION_TABLES = {
    "subclass_of",
    "subproperty_of",
    "domain_includes",
    "range_includes",
    "inverse_of",
    "superseded_by",
    "equivalent_to",
    "exact_match",
}


class SchemaPathRow(BaseModel):
    model_config = ConfigDict(extra="ignore")

    path_key: str
    relation: str
    source_id: str
    target_id: str
    hop_count: int
    route: list[str]
    path: list[str]
    via_source_ids: list[str]
    source_record: str | None = None
    target_record: str | None = None
    generated_from: str | None = None


def _surql_literal(value) -> str:
    if value is None:
        return "NONE"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if value.startswith("schema_term:"):
            return value
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ", ".join(_surql_literal(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{ " + ", ".join(f"{key}: {_surql_literal(item)}" for key, item in value.items()) + " }"
    raise TypeError(f"Unsupported value type: {type(value)!r}")


def _schema_term_payload(payload: dict) -> dict:
    return {
        "term_key": payload["term_key"],
        "source_id": payload["source_id"],
        "term_kind": payload["term_kind"],
        "source_urls": payload.get("source_urls", []),
        "contributor_urls": payload.get("contributor_urls", []),
        "exact_match_urls": payload.get("exact_match_urls", []),
        "raw_types": payload.get("raw_types", []),
        "parent_source_ids": payload.get("parent_source_ids", []),
        "domain_source_ids": payload.get("domain_source_ids", []),
        "range_source_ids": payload.get("range_source_ids", []),
        "inverse_source_ids": payload.get("inverse_source_ids", []),
        "superseded_by_source_ids": payload.get("superseded_by_source_ids", []),
        "pending": payload.get("pending", False),
        "external": payload.get("external", False),
    }


def _prefix_schema_term_record(record_id: str | None) -> str | None:
    if not record_id:
        return record_id
    if ":" in record_id:
        return record_id
    return f"schema_term:{record_id}"


def _normalize_statement(statement: str) -> str:
    stripped = statement.strip()
    if stripped.startswith("UPSERT schema_term:"):
        head, separator, content = stripped.partition(" CONTENT ")
        if separator and content.endswith(";"):
            raw_content = content[:-1].strip()
            try:
                payload = json.loads(raw_content)
            except json.JSONDecodeError:
                pass
            else:
                payload = _schema_term_payload(payload)
                return f"{head} CONTENT {_surql_literal(payload)};"
    if stripped.startswith(JSON_CONTENT_PREFIXES):
        head, separator, content = stripped.partition(" CONTENT ")
        if separator and content.endswith(";"):
            raw_content = content[:-1].strip()
            try:
                payload = json.loads(raw_content)
            except json.JSONDecodeError:
                pass
            else:
                if head.startswith("UPSERT schema_path:"):
                    payload["source_record"] = _prefix_schema_term_record(payload.get("source_record"))
                    payload["target_record"] = _prefix_schema_term_record(payload.get("target_record"))
                    payload["via_source_ids"] = [
                        _prefix_schema_term_record(record_id) for record_id in payload.get("via_source_ids", [])
                    ]
                if head.startswith("RELATE "):
                    relation = head.split("->", 2)[1]
                    if relation in SCHEMAORG_RELATION_TABLES:
                        return f"{head};"
                return f"{head} CONTENT {_surql_literal(payload)};"
    return NULL_TOKEN.sub("NONE", statement)


def _load_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _iter_sql_statements(path: Path):
    current: list[str] = []
    depth = 0
    quote: str | None = None
    escape = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not current and (not line or line.startswith("--")):
            continue
        current.append(raw_line)

        for char in raw_line:
            if escape:
                escape = False
                continue
            if quote is not None:
                if char == "\\":
                    escape = True
                elif char == quote:
                    quote = None
                continue
            if char in {'"', "'"}:
                quote = char
            elif char in "{[(":
                depth += 1
            elif char in "}])" and depth > 0:
                depth -= 1

        if depth == 0 and quote is None and line.endswith(";"):
            yield "\n".join(current).strip()
            current = []
    if current:
        raise ValueError(f"Unterminated SQL statement in {path}")


def _parse_relation_edges(path: Path) -> dict[str, set[tuple[str, str]]]:
    edges: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("RELATE "):
            continue
        relation_stmt = line[len("RELATE ") :].split(" CONTENT ", 1)[0]
        left, relation, right = [part.strip() for part in relation_stmt.split("->")]
        edges[relation].add((left, right))
    return edges


def _parse_schema_paths(path: Path) -> dict[str, SchemaPathRow]:
    rows: dict[str, SchemaPathRow] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("UPSERT schema_path:"):
            continue
        content = line.split(" CONTENT ", 1)[1].rstrip(";")
        payload = json.loads(content)
        payload["source_record"] = _prefix_schema_term_record(payload.get("source_record"))
        payload["target_record"] = _prefix_schema_term_record(payload.get("target_record"))
        payload["via_source_ids"] = [
            _prefix_schema_term_record(record_id) for record_id in payload.get("via_source_ids", [])
        ]
        row = SchemaPathRow.model_validate(payload)
        rows[row.path_key] = row
    return rows


def _wait_for_health(client: httpx.Client, base_url: str) -> None:
    deadline = time.time() + 120
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            response = client.get(f"{base_url}/health")
            if response.status_code == 200:
                return
        except Exception as exc:  # pragma: no cover - transient container startup
            last_error = exc
        time.sleep(1)
    raise RuntimeError(f"SurrealDB did not become healthy: {last_error}")


def _sql_request(
    client: httpx.Client,
    base_url: str,
    statement: str,
    headers: dict[str, str] | None = None,
) -> list[dict]:
    statement = _normalize_statement(statement)
    request_headers = {"Surreal-NS": "agennext", "Surreal-DB": "schema"}
    if headers:
        request_headers.update(headers)
    response = client.post(
        f"{base_url}/sql",
        headers=request_headers,
        auth=("root", "root"),
        content=statement,
    )
    response.raise_for_status()
    payload = response.json()
    assert isinstance(payload, list)
    assert payload, "SurrealDB returned an empty response"
    for item in payload:
        assert item["status"] == "OK", item
    return payload


def _sql_result(client: httpx.Client, base_url: str, statement: str):
    return _sql_request(client, base_url, statement)[0]["result"]


def _apply_sql_file(
    client: httpx.Client,
    base_url: str,
    path: Path,
    headers: dict[str, str] | None = None,
    batch_size: int = 25,
) -> None:
    batch: list[str] = []
    for statement in _iter_sql_statements(path):
        batch.append(_normalize_statement(statement))
        if len(batch) >= batch_size:
            _sql_request(client, base_url, "\n".join(batch), headers=headers)
            batch = []
    if batch:
        _sql_request(client, base_url, "\n".join(batch), headers=headers)


def _call_validation(
    client: httpx.Client,
    base_url: str,
    function_name: str,
    payload,
) -> None:
    _sql_request(client, base_url, f"RETURN {function_name}({_surql_literal(payload)});")


def _chunked(items: list, size: int) -> list[list]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def _boot_surrealdb(files: list[Path]):
    for path in files:
        assert path.exists(), path

    with DockerContainer(
        "surrealdb/surrealdb:latest",
        command="start memory --user root --pass root --bind 0.0.0.0:8000",
        ports=[8000],
    ) as container:
        client = httpx.Client(timeout=120.0)
        try:
            base_url = f"http://{container.get_container_host_ip()}:{container.get_exposed_port(8000)}"
            _wait_for_health(client, base_url)
            _sql_request(
                client,
                base_url,
                "DEFINE NAMESPACE agennext; USE NS agennext; DEFINE DATABASE schema; USE DB schema;",
                headers={"Surreal-NS": "root", "Surreal-DB": "root"},
            )
            for path in files:
                _apply_sql_file(client, base_url, path)
            yield client, base_url
        finally:
            client.close()


@pytest.fixture(scope="module")
def surrealdb_runtime():
    if not RUN_INTEGRATION:
        pytest.skip("Set RUN_SURREALDB_INTEGRATION=1 to run SurrealDB integration tests.")

    files = [
        SCHEMA_META_PATH,
        SCHEMA_VOCABULARY_PATH,
        RUNTIME_SCHEMA_PATH,
        SCHEMA_PATHS_PATH,
        GRAPH_VALIDATION_PATH,
    ]
    yield from _boot_surrealdb(files)


@pytest.fixture(scope="module")
def surrealdb_knowledge_graph_runtime():
    if not RUN_INTEGRATION:
        pytest.skip("Set RUN_SURREALDB_INTEGRATION=1 to run SurrealDB integration tests.")

    files = [
        SCHEMA_META_PATH,
        SCHEMA_VOCABULARY_PATH,
        RUNTIME_SCHEMA_PATH,
        KNOWLEDGE_GRAPH_PATH,
        GRAPH_VALIDATION_PATH,
    ]
    yield from _boot_surrealdb(files)


class TestSurrealdbIntegration:
    def test_schema_term_count_matches_generated_summary(self, surrealdb_runtime):
        client, base_url = surrealdb_runtime
        rows = _sql_result(client, base_url, "SELECT * FROM schema_term;")
        assert len(rows) == SCHEMA_SUMMARY["term_counts"]["total"]

    def test_relation_tables_match_generated_schemaorg_edges(self, surrealdb_runtime):
        client, base_url = surrealdb_runtime
        expected_edges = _parse_relation_edges(SCHEMA_VOCABULARY_PATH)

        for relation, expected_count in SCHEMA_SUMMARY["edge_counts"].items():
            edges = [{"in": left, "out": right} for left, right in sorted(expected_edges[relation])]
            for batch_index, batch in enumerate(_chunked(edges, 100)):
                payload = {
                    "table": relation,
                    "expected_count": expected_count if batch_index == 0 else 0,
                    "edges": batch,
                }
                _call_validation(client, base_url, "fn::validation::relation_summary", payload)

    def test_schema_path_rows_match_generated_routes(self, surrealdb_runtime):
        client, base_url = surrealdb_runtime
        expected_rows = list(_parse_schema_paths(SCHEMA_PATHS_PATH).values())
        for batch_index, batch in enumerate(_chunked([expected_row.model_dump() for expected_row in expected_rows], 100)):
            payload = {
                "expected_count": PATHS_SUMMARY["path_counts"]["total"] if batch_index == 0 else 0,
                "paths": batch,
            }
            _call_validation(client, base_url, "fn::validation::schema_paths", payload)

    def test_schemaorg_validation_file_is_loaded(self, surrealdb_runtime):
        client, base_url = surrealdb_runtime
        result = _sql_result(client, base_url, "RETURN fn::validation::assert(true, 'ok');")
        assert result is True


class TestKnowledgeGraphValidation:
    def test_knowledge_graph_seed_validates_inside_surrealdb(self, surrealdb_knowledge_graph_runtime):
        client, base_url = surrealdb_knowledge_graph_runtime
        _call_validation(client, base_url, "fn::validation::knowledge_graph", {})
