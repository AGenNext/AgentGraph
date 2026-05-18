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
DEFINE FIELD label ON TABLE schema_term TYPE any;
DEFINE FIELD comment ON TABLE schema_term TYPE any;
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
DEFINE FIELD source ON TABLE subclass_of TYPE option<string>;
DEFINE FIELD created_at ON TABLE subclass_of TYPE option<datetime>;
DEFINE TABLE subproperty_of TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE FIELD source ON TABLE subproperty_of TYPE option<string>;
DEFINE FIELD created_at ON TABLE subproperty_of TYPE option<datetime>;
DEFINE TABLE domain_includes TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE FIELD source ON TABLE domain_includes TYPE option<string>;
DEFINE FIELD created_at ON TABLE domain_includes TYPE option<datetime>;
DEFINE TABLE range_includes TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE FIELD source ON TABLE range_includes TYPE option<string>;
DEFINE FIELD created_at ON TABLE range_includes TYPE option<datetime>;
DEFINE TABLE inverse_of TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE FIELD source ON TABLE inverse_of TYPE option<string>;
DEFINE FIELD created_at ON TABLE inverse_of TYPE option<datetime>;
DEFINE TABLE superseded_by TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE FIELD source ON TABLE superseded_by TYPE option<string>;
DEFINE FIELD created_at ON TABLE superseded_by TYPE option<datetime>;
DEFINE TABLE equivalent_to TYPE RELATION IN schema_term OUT schema_term SCHEMAFULL;
DEFINE FIELD source ON TABLE equivalent_to TYPE option<string>;
DEFINE FIELD created_at ON TABLE equivalent_to TYPE option<datetime>;
DEFINE TABLE exact_match TYPE RELATION IN schema_term OUT schema_term SCHEMALESS;
