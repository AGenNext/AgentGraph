from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCHEMA_DIR = ROOT / "schema"
INPUT_JSONLD = SCHEMA_DIR / "schemaorg-current-https.jsonld"
OUTPUT_SURQL = SCHEMA_DIR / "schemaorg-vocabulary.surql"
OUTPUT_SUMMARY = SCHEMA_DIR / "schemaorg-summary.json"


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def id_list(value):
    ids = []
    for item in as_list(value):
        if isinstance(item, dict) and item.get("@id"):
            ids.append(item["@id"])
    return ids


def scalar_id(value):
    ids = id_list(value)
    return ids[0] if ids else None


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value)
    slug = slug.strip("_").lower()
    if not slug:
        slug = "term"
    if slug[0].isdigit():
        slug = f"n_{slug}"
    return slug


def record_id(kind: str, source_id: str) -> str:
    return f"{kind}_{slugify(source_id)}"


def schema_url(source_id: str) -> str | None:
    if source_id.startswith("schema:"):
        return f"https://schema.org/{source_id.split(':', 1)[1]}"
    return None


def load_graph():
    data = json.loads(INPUT_JSONLD.read_text(encoding="utf-8"))
    return data["@graph"]


graph = load_graph()
by_id = {
    item["@id"]: item
    for item in graph
    if isinstance(item, dict) and isinstance(item.get("@id"), str)
}

class_ids = {
    item_id
    for item_id, item in by_id.items()
    if item.get("@type") == "rdfs:Class"
}
property_ids = {
    item_id
    for item_id, item in by_id.items()
    if item.get("@type") == "rdf:Property"
}

parents_map = {
    item_id: [
        parent_id for parent_id in id_list(by_id[item_id].get("rdfs:subClassOf"))
        if parent_id in class_ids
    ]
    for item_id in class_ids
}


@lru_cache(None)
def has_ancestor(item_id: str, ancestor_id: str) -> bool:
    if item_id == ancestor_id:
        return True
    return any(has_ancestor(parent_id, ancestor_id) for parent_id in parents_map.get(item_id, []))


def kind_for_class(item_id: str) -> str:
    if has_ancestor(item_id, "schema:DataType"):
        return "datatype"
    if has_ancestor(item_id, "schema:Enumeration"):
        return "enumeration"
    return "class"


enumeration_class_ids = {item_id for item_id in class_ids if kind_for_class(item_id) == "enumeration"}


def term_kind(item: dict) -> str | None:
    item_type = item.get("@type")
    item_id = item.get("@id")
    if item_type == "rdf:Property":
        return "property"
    if item_type == "rdfs:Class" and item_id in class_ids:
        return kind_for_class(item_id)
    if isinstance(item_type, str) and item_type in enumeration_class_ids:
        return "enumeration_value"
    return None


terms = []
term_by_source = {}
for item in graph:
    if not isinstance(item, dict) or not isinstance(item.get("@id"), str):
        continue
    kind = term_kind(item)
    if not kind:
        continue
    source_id = item["@id"]
    key = record_id(kind, source_id)
    entry = {
        "record_id": key,
        "source_id": source_id,
        "term_key": key,
        "term_kind": kind,
        "label": item.get("rdfs:label"),
        "comment": item.get("rdfs:comment"),
        "url": schema_url(source_id),
        "is_part_of": scalar_id(item.get("schema:isPartOf")),
        "source_urls": id_list(item.get("schema:source")),
        "contributor_urls": id_list(item.get("schema:contributor")),
        "exact_match_urls": id_list(item.get("skos:exactMatch")),
        "raw_types": [item.get("@type")] if isinstance(item.get("@type"), str) else [],
        "parent_source_ids": [],
        "domain_source_ids": id_list(item.get("schema:domainIncludes")),
        "range_source_ids": id_list(item.get("schema:rangeIncludes")),
        "inverse_source_ids": [
            rel_id
            for rel_id in (
                scalar_id(item.get("schema:inverseOf")),
                scalar_id(item.get("schema:supersededBy")),
            )
            if rel_id
        ],
        "superseded_by_source_ids": id_list(item.get("schema:supersededBy")),
        "pending": scalar_id(item.get("schema:isPartOf")) == "https://pending.schema.org",
        "external": not source_id.startswith("schema:"),
    }
    if kind in {"class", "datatype", "enumeration"}:
        entry["parent_source_ids"] = parents_map.get(source_id, [])
    elif kind == "property":
        entry["parent_source_ids"] = id_list(item.get("rdfs:subPropertyOf"))
    elif kind == "enumeration_value":
        entry["parent_source_ids"] = [item["@type"]] if isinstance(item.get("@type"), str) else []
    terms.append(entry)
    term_by_source[source_id] = entry


def emit_term(term: dict) -> str:
    content = {
        "term_key": term["term_key"],
        "source_id": term["source_id"],
        "term_kind": term["term_kind"],
        "label": term["label"],
        "comment": term["comment"],
        "url": term["url"],
        "is_part_of": term["is_part_of"],
        "source_urls": term["source_urls"],
        "contributor_urls": term["contributor_urls"],
        "exact_match_urls": term["exact_match_urls"],
        "raw_types": term["raw_types"],
        "parent_source_ids": term["parent_source_ids"],
        "domain_source_ids": term["domain_source_ids"],
        "range_source_ids": term["range_source_ids"],
        "inverse_source_ids": term["inverse_source_ids"],
        "superseded_by_source_ids": term["superseded_by_source_ids"],
        "pending": term["pending"],
        "external": term["external"],
    }
    return f"UPSERT schema_term:{term['record_id']} CONTENT {json.dumps(content, ensure_ascii=False)};"


def relate(edge_table: str, from_id: str, to_id: str, metadata: dict | None = None) -> str | None:
    if from_id not in term_by_source or to_id not in term_by_source:
        return None
    left = term_by_source[from_id]["record_id"]
    right = term_by_source[to_id]["record_id"]
    if metadata:
        return (
            f"RELATE schema_term:{left}->{edge_table}->schema_term:{right} "
            f"CONTENT {json.dumps(metadata, ensure_ascii=False)};"
        )
    return f"RELATE schema_term:{left}->{edge_table}->schema_term:{right};"


edge_lines = []
edge_counters = {
    "subclass_of": 0,
    "subproperty_of": 0,
    "domain_includes": 0,
    "range_includes": 0,
    "inverse_of": 0,
    "superseded_by": 0,
    "equivalent_to": 0,
    "exact_match": 0,
}

for term in terms:
    source_id = term["source_id"]
    if term["term_kind"] in {"class", "datatype", "enumeration", "enumeration_value"}:
        for parent_id in term["parent_source_ids"]:
            line = relate("subclass_of", source_id, parent_id, {"source": "rdfs:subClassOf"})
            if line:
                edge_lines.append(line)
                edge_counters["subclass_of"] += 1
    elif term["term_kind"] == "property":
        for parent_id in term["parent_source_ids"]:
            line = relate("subproperty_of", source_id, parent_id, {"source": "rdfs:subPropertyOf"})
            if line:
                edge_lines.append(line)
                edge_counters["subproperty_of"] += 1

    for domain_id in term["domain_source_ids"]:
        line = relate("domain_includes", source_id, domain_id, {"source": "schema:domainIncludes"})
        if line:
            edge_lines.append(line)
            edge_counters["domain_includes"] += 1

    for range_id in term["range_source_ids"]:
        line = relate("range_includes", source_id, range_id, {"source": "schema:rangeIncludes"})
        if line:
            edge_lines.append(line)
            edge_counters["range_includes"] += 1

    inverse_id = scalar_id(by_id[source_id].get("schema:inverseOf")) if source_id in by_id else None
    if inverse_id:
        line = relate("inverse_of", source_id, inverse_id, {"source": "schema:inverseOf"})
        if line:
            edge_lines.append(line)
            edge_counters["inverse_of"] += 1

    for superseded_id in term["superseded_by_source_ids"]:
        line = relate("superseded_by", source_id, superseded_id, {"source": "schema:supersededBy"})
        if line:
            edge_lines.append(line)
            edge_counters["superseded_by"] += 1

    if source_id in by_id:
        item = by_id[source_id]
        for equivalent_id in id_list(item.get("owl:equivalentClass")) + id_list(item.get("owl:equivalentProperty")):
            line = relate("equivalent_to", source_id, equivalent_id, {"source": "owl:equivalent"})
            if line:
                edge_lines.append(line)
                edge_counters["equivalent_to"] += 1

        for exact_id in term["exact_match_urls"]:
            if exact_id in term_by_source:
                line = relate("exact_match", source_id, exact_id, {"source": "skos:exactMatch"})
                if line:
                    edge_lines.append(line)
                    edge_counters["exact_match"] += 1

term_lines = [emit_term(term) for term in sorted(terms, key=lambda x: (x["term_kind"], x["source_id"]))]

OUTPUT_SURQL.write_text(
    "\n".join(
        [
            "-- Generated from the official Schema.org JSON-LD vocabulary dump.",
            "-- Source: https://schema.org/version/latest/schemaorg-current-https.jsonld",
            *term_lines,
            *edge_lines,
            "",
        ]
    ),
    encoding="utf-8",
)

summary = {
    "source": "https://schema.org/version/latest/schemaorg-current-https.jsonld",
    "term_counts": {
        "total": len(terms),
        "class": sum(1 for term in terms if term["term_kind"] == "class"),
        "property": sum(1 for term in terms if term["term_kind"] == "property"),
        "datatype": sum(1 for term in terms if term["term_kind"] == "datatype"),
        "enumeration": sum(1 for term in terms if term["term_kind"] == "enumeration"),
        "enumeration_value": sum(1 for term in terms if term["term_kind"] == "enumeration_value"),
    },
    "edge_counts": edge_counters,
}
OUTPUT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
