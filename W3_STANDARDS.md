# W3 Standards Reference

## Related Standards

| Standard | URL | Schema.org Related |
|----------|-----|-----------------|
| **JSON-LD** | https://www.w3.org/TR/json-ld/ | Schema.org uses JSON-LD |
| **RDF** | https://www.w3.org/TR/rdf11-concepts/ | JSON-LD based on RDF |
| **Microdata** | https://www.w3.org/TR/microdata/ | Alternative to JSON-LD |
| **Dublin Core** | https://www.dublincore.org/specifications/dublin-core/ | Metadata vocabulary |
| **Dublin Core Terms** | https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ | Extended DC |
| **FOAF** | http://www.foaf-spec.org/ | Person/Organization identity |
| **SIOC** | https://www.w3.org/TR/sioc-core/ | Social web terminology |
| **SKOS** | https://www.w3.org/TR/skos-reference/ | Knowledge organization |
| **OWL** | https://www.w3.org/TR/owl-ref/ | Web ontology language |
| **SPARQL** | https://www.w3.org/TR/sparql11-overview/ | RDF query language |

## Implementation Mapping

| W3 Standard | Schema.org Files | Notes |
|--------------|-----------------|-------|
| JSON-LD | schema_org.py | Primary format |
| Dublin Core | knowledge_graph.py | Metadata fields |
| FOAF | person_organization.py | Person identity |
| SKOS | government_codes.py | Tax codes |
| OWL | schema_org.py | Type definitions |

## Schema.org + W3 Stack

```
Schema.org (V30.0, 2026)
         ↓ (implements)
   JSON-LD → RDF → OWL
         ↓ (uses)
   Dublin Core Terms
         ↓ (extends)
   FOAF, SKOS, SIOC
```

## Reference Files

| File | W3 Standard Used |
|------|-----------------|
| schema_org.py | JSON-LD |
| surreal/schema/schemaorg-vocabulary.surql | RDF-derived vocabulary graph |
| CONNECTION_MAP.md | RDF relationships |
| SCHEMA_WIRING.md | Full wiring |

Reference: https://www.w3.org/ | https://schema.org/docs/full.html
