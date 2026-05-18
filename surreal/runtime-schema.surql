DEFINE TABLE agent SCHEMAFULL;

DEFINE FIELD identity_type ON TABLE agent TYPE string DEFAULT "agent";
DEFINE FIELD canonical_id ON TABLE agent TYPE option<string>;
DEFINE FIELD name ON TABLE agent TYPE string;
DEFINE FIELD description ON TABLE agent TYPE option<string>;
DEFINE FIELD provider ON TABLE agent TYPE string;
DEFINE FIELD model ON TABLE agent TYPE string;
DEFINE FIELD temperature ON TABLE agent TYPE number;
DEFINE FIELD max_tokens ON TABLE agent TYPE int;
DEFINE FIELD system_prompt ON TABLE agent TYPE option<string>;
DEFINE FIELD status ON TABLE agent TYPE string;
DEFINE FIELD version ON TABLE agent TYPE string;
DEFINE FIELD is_default ON TABLE agent TYPE bool DEFAULT false;
DEFINE FIELD auth_method ON TABLE agent TYPE string;
DEFINE FIELD enable_chat ON TABLE agent TYPE bool DEFAULT true;
DEFINE FIELD enable_rag ON TABLE agent TYPE bool DEFAULT false;
DEFINE FIELD tools ON TABLE agent TYPE array<string>;
DEFINE FIELD world_location ON TABLE agent TYPE option<object>;
DEFINE FIELD valid_from ON TABLE agent TYPE option<datetime>;
DEFINE FIELD valid_to ON TABLE agent TYPE option<datetime>;
DEFINE FIELD created_at ON TABLE agent TYPE datetime;
DEFINE FIELD updated_at ON TABLE agent TYPE datetime;

DEFINE INDEX agent_canonical_id ON TABLE agent FIELDS canonical_id UNIQUE;
DEFINE INDEX agent_name ON TABLE agent FIELDS name;
DEFINE INDEX agent_status ON TABLE agent FIELDS status;
DEFINE INDEX agent_provider ON TABLE agent FIELDS provider;

DEFINE TABLE agent_version SCHEMAFULL;

DEFINE FIELD agent ON TABLE agent_version TYPE record<agent>;
DEFINE FIELD agent_id ON TABLE agent_version TYPE string;
DEFINE FIELD version ON TABLE agent_version TYPE string;
DEFINE FIELD changes ON TABLE agent_version TYPE string;
DEFINE FIELD created_at ON TABLE agent_version TYPE datetime;
DEFINE FIELD is_current ON TABLE agent_version TYPE bool DEFAULT false;
DEFINE FIELD event_type ON TABLE agent_version TYPE string;
DEFINE FIELD agent_snapshot ON TABLE agent_version TYPE object;

DEFINE INDEX agent_version_agent_id ON TABLE agent_version FIELDS agent_id;
DEFINE INDEX agent_version_current ON TABLE agent_version FIELDS agent_id, is_current;
DEFINE INDEX agent_version_created_at ON TABLE agent_version FIELDS created_at;

DEFINE TABLE version_of TYPE RELATION IN agent_version OUT agent SCHEMAFULL;
DEFINE FIELD created_at ON TABLE version_of TYPE datetime;

DEFINE TABLE entity SCHEMAFULL;

DEFINE FIELD type ON TABLE entity TYPE string;
DEFINE FIELD canonical_id ON TABLE entity TYPE option<string>;
DEFINE FIELD name ON TABLE entity TYPE string;
DEFINE FIELD description ON TABLE entity TYPE option<string>;
DEFINE FIELD jobTitle ON TABLE entity TYPE option<string>;
DEFINE FIELD employee ON TABLE entity TYPE option<string>;
DEFINE FIELD brand ON TABLE entity TYPE option<string>;
DEFINE FIELD category ON TABLE entity TYPE option<string>;
DEFINE FIELD price ON TABLE entity TYPE option<number>;
DEFINE FIELD author ON TABLE entity TYPE option<string>;
DEFINE FIELD datePublished ON TABLE entity TYPE option<string>;
DEFINE FIELD keywords ON TABLE entity TYPE option<string>;
DEFINE FIELD genre ON TABLE entity TYPE option<string>;
DEFINE FIELD address ON TABLE entity TYPE option<string>;
DEFINE FIELD geo ON TABLE entity TYPE option<string>;
DEFINE FIELD startDate ON TABLE entity TYPE option<string>;
DEFINE FIELD location ON TABLE entity TYPE option<string>;
DEFINE FIELD organizer ON TABLE entity TYPE option<string>;
DEFINE FIELD world_location ON TABLE entity TYPE option<object>;
DEFINE FIELD valid_from ON TABLE entity TYPE option<datetime>;
DEFINE FIELD valid_to ON TABLE entity TYPE option<datetime>;
DEFINE FIELD created_at ON TABLE entity TYPE option<datetime>;
DEFINE FIELD updated_at ON TABLE entity TYPE option<datetime>;

DEFINE INDEX entity_type ON TABLE entity FIELDS type;
DEFINE INDEX entity_canonical_id ON TABLE entity FIELDS canonical_id;
DEFINE INDEX entity_name ON TABLE entity FIELDS name;

DEFINE TABLE entity_kind TYPE RELATION IN entity OUT schema_term SCHEMAFULL;
DEFINE FIELD source ON TABLE entity_kind TYPE string;

DEFINE TABLE schema_path SCHEMAFULL;

DEFINE FIELD path_key ON TABLE schema_path TYPE string;
DEFINE FIELD relation ON TABLE schema_path TYPE string;
DEFINE FIELD source_id ON TABLE schema_path TYPE string;
DEFINE FIELD target_id ON TABLE schema_path TYPE string;
DEFINE FIELD hop_count ON TABLE schema_path TYPE int;
DEFINE FIELD route ON TABLE schema_path TYPE array<string>;
DEFINE FIELD path ON TABLE schema_path TYPE array<string>;
DEFINE FIELD via_source_ids ON TABLE schema_path TYPE array<record<schema_term>>;
DEFINE FIELD source_record ON TABLE schema_path TYPE option<record<schema_term>>;
DEFINE FIELD target_record ON TABLE schema_path TYPE option<record<schema_term>>;
DEFINE FIELD generated_from ON TABLE schema_path TYPE option<string>;
DEFINE FIELD created_at ON TABLE schema_path TYPE option<datetime>;
DEFINE FIELD updated_at ON TABLE schema_path TYPE option<datetime>;

DEFINE INDEX schema_path_path_key ON TABLE schema_path FIELDS path_key UNIQUE;
DEFINE INDEX schema_path_relation ON TABLE schema_path FIELDS relation;
DEFINE INDEX schema_path_source_id ON TABLE schema_path FIELDS source_id;
DEFINE INDEX schema_path_target_id ON TABLE schema_path FIELDS target_id;
DEFINE INDEX schema_path_hop_count ON TABLE schema_path FIELDS hop_count;

DEFINE TABLE human SCHEMAFULL;

DEFINE FIELD identity_type ON TABLE human TYPE string DEFAULT "human";
DEFINE FIELD canonical_id ON TABLE human TYPE option<string>;
DEFINE FIELD name ON TABLE human TYPE string;
DEFINE FIELD description ON TABLE human TYPE option<string>;
DEFINE FIELD status ON TABLE human TYPE string DEFAULT "active";
DEFINE FIELD world_location ON TABLE human TYPE option<object>;
DEFINE FIELD valid_from ON TABLE human TYPE option<datetime>;
DEFINE FIELD valid_to ON TABLE human TYPE option<datetime>;
DEFINE FIELD created_at ON TABLE human TYPE datetime;
DEFINE FIELD updated_at ON TABLE human TYPE datetime;

DEFINE INDEX human_canonical_id ON TABLE human FIELDS canonical_id UNIQUE;
DEFINE INDEX human_name ON TABLE human FIELDS name;
DEFINE INDEX human_status ON TABLE human FIELDS status;

DEFINE TABLE instruction_doc SCHEMAFULL;

DEFINE FIELD title ON TABLE instruction_doc TYPE string;
DEFINE FIELD source_path ON TABLE instruction_doc TYPE option<string>;
DEFINE FIELD source_hash ON TABLE instruction_doc TYPE option<string>;
DEFINE FIELD body ON TABLE instruction_doc TYPE string;
DEFINE FIELD format ON TABLE instruction_doc TYPE string DEFAULT "markdown";
DEFINE FIELD status ON TABLE instruction_doc TYPE string DEFAULT "active";
DEFINE FIELD valid_from ON TABLE instruction_doc TYPE option<datetime>;
DEFINE FIELD valid_to ON TABLE instruction_doc TYPE option<datetime>;
DEFINE FIELD world_location ON TABLE instruction_doc TYPE option<object>;
DEFINE FIELD created_at ON TABLE instruction_doc TYPE datetime;
DEFINE FIELD updated_at ON TABLE instruction_doc TYPE datetime;

DEFINE INDEX instruction_doc_source_path ON TABLE instruction_doc FIELDS source_path;
DEFINE INDEX instruction_doc_title ON TABLE instruction_doc FIELDS title;
DEFINE INDEX instruction_doc_status ON TABLE instruction_doc FIELDS status;

DEFINE TABLE policy_doc SCHEMAFULL;

DEFINE FIELD name ON TABLE policy_doc TYPE string;
DEFINE FIELD policy_type ON TABLE policy_doc TYPE string;
DEFINE FIELD source_path ON TABLE policy_doc TYPE option<string>;
DEFINE FIELD body ON TABLE policy_doc TYPE string;
DEFINE FIELD status ON TABLE policy_doc TYPE string DEFAULT "active";
DEFINE FIELD authority ON TABLE policy_doc TYPE option<string>;
DEFINE FIELD valid_from ON TABLE policy_doc TYPE option<datetime>;
DEFINE FIELD valid_to ON TABLE policy_doc TYPE option<datetime>;
DEFINE FIELD world_location ON TABLE policy_doc TYPE option<object>;
DEFINE FIELD created_at ON TABLE policy_doc TYPE datetime;
DEFINE FIELD updated_at ON TABLE policy_doc TYPE datetime;

DEFINE INDEX policy_doc_name ON TABLE policy_doc FIELDS name;
DEFINE INDEX policy_doc_type ON TABLE policy_doc FIELDS policy_type;
DEFINE INDEX policy_doc_status ON TABLE policy_doc FIELDS status;

DEFINE TABLE memory_object SCHEMAFULL;

DEFINE FIELD memory_type ON TABLE memory_object TYPE string;
DEFINE FIELD title ON TABLE memory_object TYPE option<string>;
DEFINE FIELD content ON TABLE memory_object TYPE object;
DEFINE FIELD content_text ON TABLE memory_object TYPE option<string>;
DEFINE FIELD modality ON TABLE memory_object TYPE string DEFAULT "text";
DEFINE FIELD status ON TABLE memory_object TYPE string DEFAULT "active";
DEFINE FIELD source_kind ON TABLE memory_object TYPE option<string>;
DEFINE FIELD source_ref ON TABLE memory_object TYPE option<string>;
DEFINE FIELD created_by ON TABLE memory_object TYPE option<string>;
DEFINE FIELD owner_ref ON TABLE memory_object TYPE option<string>;
DEFINE FIELD importance ON TABLE memory_object TYPE option<number>;
DEFINE FIELD world_location ON TABLE memory_object TYPE option<object>;
DEFINE FIELD valid_from ON TABLE memory_object TYPE option<datetime>;
DEFINE FIELD valid_to ON TABLE memory_object TYPE option<datetime>;
DEFINE FIELD created_at ON TABLE memory_object TYPE datetime;
DEFINE FIELD updated_at ON TABLE memory_object TYPE datetime;

DEFINE INDEX memory_object_type ON TABLE memory_object FIELDS memory_type;
DEFINE INDEX memory_object_status ON TABLE memory_object FIELDS status;
DEFINE INDEX memory_object_source_ref ON TABLE memory_object FIELDS source_ref;
DEFINE INDEX memory_object_owner_ref ON TABLE memory_object FIELDS owner_ref;

DEFINE TABLE artifact_ref SCHEMAFULL;

DEFINE FIELD artifact_type ON TABLE artifact_ref TYPE string;
DEFINE FIELD name ON TABLE artifact_ref TYPE string;
DEFINE FIELD uri ON TABLE artifact_ref TYPE string;
DEFINE FIELD storage_kind ON TABLE artifact_ref TYPE string;
DEFINE FIELD status ON TABLE artifact_ref TYPE string DEFAULT "active";
DEFINE FIELD owner_ref ON TABLE artifact_ref TYPE option<string>;
DEFINE FIELD created_by ON TABLE artifact_ref TYPE option<string>;
DEFINE FIELD world_location ON TABLE artifact_ref TYPE option<object>;
DEFINE FIELD valid_from ON TABLE artifact_ref TYPE option<datetime>;
DEFINE FIELD valid_to ON TABLE artifact_ref TYPE option<datetime>;
DEFINE FIELD created_at ON TABLE artifact_ref TYPE datetime;
DEFINE FIELD updated_at ON TABLE artifact_ref TYPE datetime;

DEFINE INDEX artifact_ref_name ON TABLE artifact_ref FIELDS name;
DEFINE INDEX artifact_ref_uri ON TABLE artifact_ref FIELDS uri UNIQUE;
DEFINE INDEX artifact_ref_type ON TABLE artifact_ref FIELDS artifact_type;

DEFINE TABLE secret_ref SCHEMAFULL;

DEFINE FIELD name ON TABLE secret_ref TYPE string;
DEFINE FIELD backend ON TABLE secret_ref TYPE string;
DEFINE FIELD locator ON TABLE secret_ref TYPE string;
DEFINE FIELD policy_ref ON TABLE secret_ref TYPE option<string>;
DEFINE FIELD owner_ref ON TABLE secret_ref TYPE option<string>;
DEFINE FIELD status ON TABLE secret_ref TYPE string DEFAULT "active";
DEFINE FIELD world_location ON TABLE secret_ref TYPE option<object>;
DEFINE FIELD valid_from ON TABLE secret_ref TYPE option<datetime>;
DEFINE FIELD valid_to ON TABLE secret_ref TYPE option<datetime>;
DEFINE FIELD created_at ON TABLE secret_ref TYPE datetime;
DEFINE FIELD updated_at ON TABLE secret_ref TYPE datetime;

DEFINE INDEX secret_ref_name ON TABLE secret_ref FIELDS name;
DEFINE INDEX secret_ref_locator ON TABLE secret_ref FIELDS locator UNIQUE;
DEFINE INDEX secret_ref_status ON TABLE secret_ref FIELDS status;

DEFINE TABLE audit_event SCHEMAFULL;

DEFINE FIELD event_type ON TABLE audit_event TYPE string;
DEFINE FIELD stage ON TABLE audit_event TYPE string ASSERT $value INSIDE [
  "input",
  "processing",
  "stream",
  "output",
  "policy",
  "system"
];
DEFINE FIELD actor_ref ON TABLE audit_event TYPE option<string>;
DEFINE FIELD actor_type ON TABLE audit_event TYPE option<string>;
DEFINE FIELD target_ref ON TABLE audit_event TYPE option<string>;
DEFINE FIELD parent_event_ref ON TABLE audit_event TYPE option<string>;
DEFINE FIELD request_id ON TABLE audit_event TYPE option<string>;
DEFINE FIELD trace_id ON TABLE audit_event TYPE option<string>;
DEFINE FIELD payload ON TABLE audit_event TYPE object;
DEFINE FIELD policy_context ON TABLE audit_event TYPE option<object>;
DEFINE FIELD world_location ON TABLE audit_event TYPE option<object>;
DEFINE FIELD event_time ON TABLE audit_event TYPE datetime;
DEFINE FIELD created_at ON TABLE audit_event TYPE datetime;

DEFINE INDEX audit_event_type ON TABLE audit_event FIELDS event_type;
DEFINE INDEX audit_event_stage ON TABLE audit_event FIELDS stage;
DEFINE INDEX audit_event_actor_ref ON TABLE audit_event FIELDS actor_ref;
DEFINE INDEX audit_event_target_ref ON TABLE audit_event FIELDS target_ref;
DEFINE INDEX audit_event_event_time ON TABLE audit_event FIELDS event_time;
DEFINE INDEX audit_event_trace_id ON TABLE audit_event FIELDS trace_id;

DEFINE TABLE knowledge_about TYPE RELATION IN memory_object OUT entity SCHEMAFULL;
DEFINE FIELD created_at ON TABLE knowledge_about TYPE datetime;
DEFINE FIELD source ON TABLE knowledge_about TYPE string;

DEFINE TABLE memory_owned_by TYPE RELATION IN memory_object OUT agent|human SCHEMAFULL;
DEFINE FIELD created_at ON TABLE memory_owned_by TYPE datetime;
DEFINE FIELD source ON TABLE memory_owned_by TYPE string;

DEFINE TABLE instruction_applies_to TYPE RELATION IN instruction_doc OUT agent|human|memory_object|entity SCHEMAFULL;
DEFINE FIELD created_at ON TABLE instruction_applies_to TYPE datetime;
DEFINE FIELD source ON TABLE instruction_applies_to TYPE string;

DEFINE TABLE policy_applies_to TYPE RELATION IN policy_doc OUT agent|human|artifact_ref|secret_ref|memory_object|entity SCHEMAFULL;
DEFINE FIELD created_at ON TABLE policy_applies_to TYPE datetime;
DEFINE FIELD source ON TABLE policy_applies_to TYPE string;

DEFINE TABLE generated_from TYPE RELATION IN artifact_ref OUT memory_object|instruction_doc|policy_doc|entity SCHEMAFULL;
DEFINE FIELD created_at ON TABLE generated_from TYPE datetime;
DEFINE FIELD source ON TABLE generated_from TYPE string;

DEFINE TABLE references_secret TYPE RELATION IN artifact_ref|memory_object OUT secret_ref SCHEMAFULL;
DEFINE FIELD created_at ON TABLE references_secret TYPE datetime;
DEFINE FIELD source ON TABLE references_secret TYPE string;

DEFINE TABLE caused_by TYPE RELATION IN audit_event OUT audit_event SCHEMAFULL;
DEFINE FIELD created_at ON TABLE caused_by TYPE datetime;
DEFINE FIELD source ON TABLE caused_by TYPE string;

DEFINE TABLE acted_on TYPE RELATION IN audit_event OUT agent|human|entity|artifact_ref|secret_ref|memory_object SCHEMAFULL;
DEFINE FIELD created_at ON TABLE acted_on TYPE datetime;
DEFINE FIELD source ON TABLE acted_on TYPE string;
