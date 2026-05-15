DEFINE TABLE schema_term SCHEMAFULL;

DEFINE FIELD term_key ON TABLE schema_term TYPE string;
DEFINE FIELD source_id ON TABLE schema_term TYPE string;
DEFINE FIELD term_kind ON TABLE schema_term TYPE string ASSERT $value INSIDE [
  "class",
  "property",
  "datatype",
  "enumeration",
  "enumeration_value"
];
DEFINE FIELD label ON TABLE schema_term TYPE option<string>;
DEFINE FIELD comment ON TABLE schema_term TYPE option<string>;
DEFINE FIELD url ON TABLE schema_term TYPE option<string>;
DEFINE FIELD is_part_of ON TABLE schema_term TYPE option<string>;
DEFINE FIELD source_urls ON TABLE schema_term TYPE array<string>;
DEFINE FIELD contributor_urls ON TABLE schema_term TYPE array<string>;
DEFINE FIELD exact_match_urls ON TABLE schema_term TYPE array<string>;
DEFINE FIELD raw_types ON TABLE schema_term TYPE array<string>;
DEFINE FIELD parent_source_ids ON TABLE schema_term TYPE array<string>;
DEFINE FIELD domain_source_ids ON TABLE schema_term TYPE array<string>;
DEFINE FIELD range_source_ids ON TABLE schema_term TYPE array<string>;
DEFINE FIELD inverse_source_ids ON TABLE schema_term TYPE array<string>;
DEFINE FIELD superseded_by_source_ids ON TABLE schema_term TYPE array<string>;
DEFINE FIELD pending ON TABLE schema_term TYPE bool DEFAULT false;
DEFINE FIELD external ON TABLE schema_term TYPE bool DEFAULT false;

DEFINE INDEX schema_term_term_key ON TABLE schema_term FIELDS term_key UNIQUE;
DEFINE INDEX schema_term_source_id ON TABLE schema_term FIELDS source_id UNIQUE;
DEFINE INDEX schema_term_kind ON TABLE schema_term FIELDS term_kind;
DEFINE INDEX schema_term_label ON TABLE schema_term FIELDS label;

DEFINE TABLE subclass_of TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE TABLE subproperty_of TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE TABLE domain_includes TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE TABLE range_includes TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE TABLE inverse_of TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE TABLE superseded_by TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE TABLE equivalent_to TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE TABLE exact_match TYPE RELATION IN schema_term OUT schema_term SCHEMALESS;
