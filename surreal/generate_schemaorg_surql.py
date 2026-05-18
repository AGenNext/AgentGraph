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
OUTPUT_PATHS_SURQL = SCHEMA_DIR / "schemaorg-paths.surql"
OUTPUT_PATHS_SUMMARY = SCHEMA_DIR / "schemaorg-paths-summary.json"


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
direct_edges = []
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
                direct_edges.append(("subclass_of", source_id, parent_id))
                edge_counters["subclass_of"] += 1
    elif term["term_kind"] == "property":
        for parent_id in term["parent_source_ids"]:
            line = relate("subproperty_of", source_id, parent_id, {"source": "rdfs:subPropertyOf"})
            if line:
                edge_lines.append(line)
                direct_edges.append(("subproperty_of", source_id, parent_id))
                edge_counters["subproperty_of"] += 1

    for domain_id in term["domain_source_ids"]:
        line = relate("domain_includes", source_id, domain_id, {"source": "schema:domainIncludes"})
        if line:
            edge_lines.append(line)
            direct_edges.append(("domain_includes", source_id, domain_id))
            edge_counters["domain_includes"] += 1

    for range_id in term["range_source_ids"]:
        line = relate("range_includes", source_id, range_id, {"source": "schema:rangeIncludes"})
        if line:
            edge_lines.append(line)
            direct_edges.append(("range_includes", source_id, range_id))
            edge_counters["range_includes"] += 1

    inverse_id = scalar_id(by_id[source_id].get("schema:inverseOf")) if source_id in by_id else None
    if inverse_id:
        line = relate("inverse_of", source_id, inverse_id, {"source": "schema:inverseOf"})
        if line:
            edge_lines.append(line)
            direct_edges.append(("inverse_of", source_id, inverse_id))
            edge_counters["inverse_of"] += 1

    for superseded_id in term["superseded_by_source_ids"]:
        line = relate("superseded_by", source_id, superseded_id, {"source": "schema:supersededBy"})
        if line:
            edge_lines.append(line)
            direct_edges.append(("superseded_by", source_id, superseded_id))
            edge_counters["superseded_by"] += 1

    if source_id in by_id:
        item = by_id[source_id]
        for equivalent_id in id_list(item.get("owl:equivalentClass")) + id_list(item.get("owl:equivalentProperty")):
            line = relate("equivalent_to", source_id, equivalent_id, {"source": "owl:equivalent"})
            if line:
                edge_lines.append(line)
                direct_edges.append(("equivalent_to", source_id, equivalent_id))
                edge_counters["equivalent_to"] += 1

        for exact_id in term["exact_match_urls"]:
            if exact_id in term_by_source:
                line = relate("exact_match", source_id, exact_id, {"source": "skos:exactMatch"})
                if line:
                    edge_lines.append(line)
                    direct_edges.append(("exact_match", source_id, exact_id))
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


def _path_record_id(relation: str, route: list[str], path: list[str]) -> str:
    import hashlib

    digest = hashlib.sha1(
        "|".join([relation, *route, *path]).encode("utf-8")
    ).hexdigest()[:16]
    return f"path_{slugify(relation)}_{digest}"


def _path_key(relation: str, route: list[str], path: list[str]) -> str:
    return " | ".join([relation, " -> ".join(route), " -> ".join(path)])


def _all_paths(start_id: str, parent_map: dict[str, list[str]], relation_name: str) -> list[tuple[list[str], list[str]]]:
    results: list[tuple[list[str], list[str]]] = []

    def walk(node_id: str, node_path: list[str], route_path: list[str], visited: set[str]) -> None:
        for parent_id in parent_map.get(node_id, []):
            if parent_id in visited:
                continue
            next_nodes = node_path + [parent_id]
            next_route = route_path + [relation_name]
            results.append((next_route, next_nodes))
            walk(parent_id, next_nodes, next_route, visited | {parent_id})

    walk(start_id, [start_id], [], {start_id})
    return results


class_parent_paths = {
    source_id: _all_paths(source_id, parents_map, "subclass_of")
    for source_id in class_ids
}

property_parent_map = {
    source_id: id_list(by_id[source_id].get("rdfs:subPropertyOf"))
    if source_id in by_id
    else []
    for source_id in property_ids
}

property_parent_paths = {
    source_id: _all_paths(source_id, property_parent_map, "subproperty_of")
    for source_id in property_ids
}


def _make_path_entries() -> list[dict]:
    entries: list[dict] = []
    seen: set[str] = set()

    def add_entry(relation: str, route: list[str], path: list[str], source_id: str, target_id: str, via: list[str]) -> None:
        source_term = term_by_source.get(source_id)
        target_term = term_by_source.get(target_id)
        if not source_term or not target_term:
            return
        record_id = _path_record_id(relation, route, path)
        if record_id in seen:
            return
        seen.add(record_id)
        entries.append(
            {
                "record_id": record_id,
                "path_key": _path_key(relation, route, path),
                "relation": relation,
                "source_id": source_id,
                "target_id": target_id,
                "hop_count": max(len(path) - 1, 1),
                "route": route,
                "path": path,
                "via_source_ids": via,
                "source_record": source_term["record_id"],
                "target_record": target_term["record_id"],
                "generated_from": "schemaorg-current-https.jsonld",
            }
        )

    for relation, source_id, target_id in direct_edges:
        if source_id in term_by_source and target_id in term_by_source:
            add_entry(
                relation=f"{relation}_path",
                route=[relation],
                path=[source_id, target_id],
                source_id=source_id,
                target_id=target_id,
                via=[],
            )

    for source_id, paths in class_parent_paths.items():
        for route, node_path in paths:
            add_entry(
                relation="subclass_of_path",
                route=route,
                path=node_path,
                source_id=source_id,
                target_id=node_path[-1],
                via=[term_by_source[node]["record_id"] for node in node_path[1:-1] if node in term_by_source],
            )

    for source_id, property_paths in property_parent_paths.items():
        for prop_route, prop_path in property_paths:
            prop_tail = prop_path[-1]
            inherited_props = [prop_tail, *prop_path[1:-1]]
            # The path above walks source -> ancestor properties. We want each
            # property in the chain, including the ancestor that supplies the
            # domain/range.
            property_chain = [source_id, *prop_path[1:]]
            for property_node in property_chain:
                direct_domains = id_list(by_id.get(property_node, {}).get("schema:domainIncludes"))
                direct_ranges = id_list(by_id.get(property_node, {}).get("schema:rangeIncludes"))

                for domain_id in direct_domains:
                    domain_paths = class_parent_paths.get(domain_id, [])
                    if not domain_paths:
                        add_entry(
                            relation="domain_includes_path",
                            route=prop_route + ["domain_includes"],
                            path=property_chain + [domain_id],
                            source_id=source_id,
                            target_id=domain_id,
                            via=[term_by_source[node]["record_id"] for node in property_chain[1:-1] if node in term_by_source],
                        )
                    for class_route, class_path in domain_paths:
                        add_entry(
                            relation="domain_includes_path",
                            route=prop_route + ["domain_includes", *class_route],
                            path=property_chain + [domain_id, *class_path[1:]],
                            source_id=source_id,
                            target_id=class_path[-1],
                            via=[term_by_source[node]["record_id"] for node in property_chain[1:-1] if node in term_by_source]
                            + [term_by_source[node]["record_id"] for node in class_path[1:-1] if node in term_by_source],
                        )

                for range_id in direct_ranges:
                    range_paths = class_parent_paths.get(range_id, [])
                    if not range_paths:
                        add_entry(
                            relation="range_includes_path",
                            route=prop_route + ["range_includes"],
                            path=property_chain + [range_id],
                            source_id=source_id,
                            target_id=range_id,
                            via=[term_by_source[node]["record_id"] for node in property_chain[1:-1] if node in term_by_source],
                        )
                    for class_route, class_path in range_paths:
                        add_entry(
                            relation="range_includes_path",
                            route=prop_route + ["range_includes", *class_route],
                            path=property_chain + [range_id, *class_path[1:]],
                            source_id=source_id,
                            target_id=class_path[-1],
                            via=[term_by_source[node]["record_id"] for node in property_chain[1:-1] if node in term_by_source]
                            + [term_by_source[node]["record_id"] for node in class_path[1:-1] if node in term_by_source],
                        )

    return entries


def _emit_path(entry: dict) -> str:
    content = {
        "path_key": entry["path_key"],
        "relation": entry["relation"],
        "source_id": entry["source_id"],
        "target_id": entry["target_id"],
        "hop_count": entry["hop_count"],
        "route": entry["route"],
        "path": entry["path"],
        "via_source_ids": entry["via_source_ids"],
        "source_record": entry["source_record"],
        "target_record": entry["target_record"],
        "generated_from": entry["generated_from"],
        "created_at": None,
        "updated_at": None,
    }
    return f"UPSERT schema_path:{entry['record_id']} CONTENT {json.dumps(content, ensure_ascii=False)};"


path_entries = _make_path_entries()
path_lines = [ _emit_path(entry) for entry in sorted(path_entries, key=lambda x: x["path_key"]) ]

OUTPUT_PATHS_SURQL.write_text(
    "\n".join(
        [
            "-- Generated multi-step Schema.org relation paths.",
            "-- Source: https://schema.org/version/latest/schemaorg-current-https.jsonld",
            *path_lines,
            "",
        ]
    ),
    encoding="utf-8",
)

path_summary = {
    "source": "https://schema.org/version/latest/schemaorg-current-https.jsonld",
    "path_counts": {
        "total": len(path_entries),
        "direct": sum(1 for entry in path_entries if entry["hop_count"] == 1),
        "multi_step": sum(1 for entry in path_entries if entry["hop_count"] > 1),
        "subclass_of_path": sum(1 for entry in path_entries if entry["relation"] == "subclass_of_path"),
        "subproperty_of_path": sum(1 for entry in path_entries if entry["relation"] == "subproperty_of_path"),
        "domain_includes_path": sum(1 for entry in path_entries if entry["relation"] == "domain_includes_path"),
        "range_includes_path": sum(1 for entry in path_entries if entry["relation"] == "range_includes_path"),
    },
}
OUTPUT_PATHS_SUMMARY.write_text(json.dumps(path_summary, indent=2, sort_keys=True), encoding="utf-8")
