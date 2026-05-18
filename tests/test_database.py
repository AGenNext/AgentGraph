"""SurrealDB schema and configuration tests."""

import json
from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "surreal" / "schema" / "schemaorg-vocabulary.surql"
KNOWLEDGE_GRAPH_PATH = Path(__file__).resolve().parents[1] / "surreal" / "knowledge-graph.surql"
PATHS_PATH = Path(__file__).resolve().parents[1] / "surreal" / "schema" / "schemaorg-paths.surql"
PATHS_SUMMARY_PATH = Path(__file__).resolve().parents[1] / "surreal" / "schema" / "schemaorg-paths-summary.json"


class TestSurrealSchema:
    """Test the canonical SurrealDB schema assets."""

    def test_schema_file_exists(self):
        assert SCHEMA_PATH.exists()
        assert SCHEMA_PATH.name == "schemaorg-vocabulary.surql"

    def test_schema_contains_table_definitions(self):
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        assert schema.startswith("-- Generated from the official Schema.org JSON-LD vocabulary dump.")
        assert "UPSERT schema_term:" in schema
        assert schema.count("UPSERT schema_term:") > 100


class TestKnowledgeGraph:
    """Test the seeded repository knowledge graph."""

    def test_knowledge_graph_file_exists(self):
        assert KNOWLEDGE_GRAPH_PATH.exists()

    def test_knowledge_graph_contains_core_edges(self):
        graph = KNOWLEDGE_GRAPH_PATH.read_text(encoding="utf-8")
        assert "UPSERT memory_object:repo_knowledge_graph" in graph
        assert "RELATE memory_object:repo_knowledge_graph->knowledge_about->entity:agent_graph_platform" in graph
        assert "RELATE artifact_ref:knowledge_graph_seed->generated_from->entity:schema_org_vocabulary" in graph


class TestSchemaPathLinks:
    """Test record-link typing for multi-step path storage."""

    def test_schema_path_uses_record_links(self):
        runtime_schema = (Path(__file__).resolve().parents[1] / "surreal" / "runtime-schema.surql").read_text(
            encoding="utf-8"
        )
        assert "DEFINE FIELD source_record ON TABLE schema_path TYPE option<record<schema_term>>;" in runtime_schema
        assert "DEFINE FIELD target_record ON TABLE schema_path TYPE option<record<schema_term>>;" in runtime_schema
        assert "DEFINE FIELD via_source_ids ON TABLE schema_path TYPE array<record<schema_term>>;" in runtime_schema


class TestSchemaPathsAsset:
    """Test the materialized relation-path asset."""

    def test_paths_file_exists(self):
        assert PATHS_PATH.exists()
        assert PATHS_SUMMARY_PATH.exists()

    def test_paths_summary_has_multi_step_routes(self):
        summary = json.loads(PATHS_SUMMARY_PATH.read_text(encoding="utf-8"))
        path_counts = summary["path_counts"]
        assert path_counts["total"] > 1000
        assert path_counts["multi_step"] > 0
        assert path_counts["domain_includes_path"] > 0
        assert path_counts["range_includes_path"] > 0

    def test_paths_file_contains_route_fields(self):
        paths = PATHS_PATH.read_text(encoding="utf-8")
        assert "UPSERT schema_path:" in paths
        assert '"route": ["domain_includes"]' in paths or '"route": ["subclass_of"]' in paths
