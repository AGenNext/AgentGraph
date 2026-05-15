# SurrealDB Schema Layer

This directory contains the database schema layer rebuilt from the official
Schema.org JSON-LD dump.

Files:

- `schema/schemaorg-current-https.jsonld`
  Canonical upstream Schema.org vocabulary dump.
- `schema/schema-meta.surql`
  SurrealDB metamodel for storing the Schema.org vocabulary as a graph.
- `schema/schemaorg-vocabulary.surql`
  Generated SurrealQL import of all types, properties, values, and relations.
- `schema/schemaorg-summary.json`
  Generated summary counts for verification.
- `generate_schemaorg_surql.py`
  Generator that converts the upstream JSON-LD dump into SurrealQL.

The vocabulary is represented as:

- `schema_term`
  All schema terms in one table with a `term_kind`.
- relation tables
  `subclass_of`, `subproperty_of`, `domain_includes`, `range_includes`,
  `inverse_of`, `superseded_by`, `equivalent_to`, `exact_match`.
