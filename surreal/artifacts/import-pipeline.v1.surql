-- AGenNext Artifact Import Pipeline v1
-- Agent-Graph owns source-to-record mapping and graph ingestion.
-- Artifact repositories define their native record schemas.
-- Agent-Grammar validates records.
-- Agent-Review gates publication.
--
-- Load order:
--   1. Agent-Grammar surreal rules and seed data
--   2. Artifact repository source schemas
--   3. Agent-Graph import pipeline
--
-- Required dependencies:
--   grammar_context
--   artifact_kind
--   blueprint_entity_type
--   blueprint_objective

DEFINE TABLE artifact_import_job_v1 SCHEMAFULL;
DEFINE FIELD artifact_kind ON TABLE artifact_import_job_v1 TYPE record<artifact_kind>;
DEFINE FIELD source_repository ON TABLE artifact_import_job_v1 TYPE string;
DEFINE FIELD source_path ON TABLE artifact_import_job_v1 TYPE string;
DEFINE FIELD source_commit_sha ON TABLE artifact_import_job_v1 TYPE option<string>;
DEFINE FIELD source_hash ON TABLE artifact_import_job_v1 TYPE option<string>;
DEFINE FIELD source_format ON TABLE artifact_import_job_v1 TYPE string ASSERT $value INSIDE ["yaml", "json", "markdown", "html", "text"];
DEFINE FIELD source_payload ON TABLE artifact_import_job_v1 TYPE any;
DEFINE FIELD status ON TABLE artifact_import_job_v1 TYPE string ASSERT $value INSIDE ["queued", "mapped", "validated", "failed"] DEFAULT "queued";
DEFINE FIELD mapped_record ON TABLE artifact_import_job_v1 TYPE option<any>;
DEFINE FIELD validation_report ON TABLE artifact_import_job_v1 TYPE option<object>;
DEFINE FIELD error ON TABLE artifact_import_job_v1 TYPE option<string>;
DEFINE FIELD created_at ON TABLE artifact_import_job_v1 TYPE datetime DEFAULT time::now();
DEFINE FIELD updated_at ON TABLE artifact_import_job_v1 TYPE datetime DEFAULT time::now();
DEFINE INDEX artifact_import_job_v1_kind ON TABLE artifact_import_job_v1 FIELDS artifact_kind;
DEFINE INDEX artifact_import_job_v1_source ON TABLE artifact_import_job_v1 FIELDS source_repository, source_path, source_commit_sha;

-- updated_at is managed by ingestion/update pipelines.

-- -----------------------------------------------------------------------------
-- Mapping helpers
-- -----------------------------------------------------------------------------

DEFINE FUNCTION fn::artifact_source_context() {
  RETURN grammar_context:agent_graph_content;
};

DEFINE FUNCTION fn::artifact_published_context() {
  RETURN grammar_context:schema_org_export;
};

DEFINE FUNCTION fn::map_skill_import_v1($doc: object, $source: object) {
  RETURN {
    context: fn::artifact_source_context(),
    type: "ag:Skill",
    skill_id: $doc.id,
    name: $doc.name,
    version: IF $doc.version != NONE THEN $doc.version ELSE "0.1.0" END,
    lifecycle_status: IF $doc.status != NONE THEN $doc.status ELSE "draft" END,
    category: $doc.category,
    risk: $doc.risk,
    description: $doc.description,
    creator: IF $doc.creator != NONE THEN $doc.creator ELSE { type: "Organization", name: "AGenNext" } END,
    publisher: IF $doc.publisher != NONE THEN $doc.publisher ELSE { type: "Organization", name: "AGenNext" } END,
    runtime_profiles: IF $doc.runtime_profiles != NONE THEN $doc.runtime_profiles ELSE [] END,
    required_tools: IF $doc.required_tools != NONE THEN $doc.required_tools ELSE [] END,
    required_secrets: $doc.required_secrets,
    approval_required: IF $doc.approval_required != NONE THEN $doc.approval_required ELSE false END,
    inputs: IF $doc.inputs != NONE THEN $doc.inputs ELSE {} END,
    outputs: IF $doc.outputs != NONE THEN $doc.outputs ELSE {} END,
    graph_context_owner: "Agent-Graph",
    semantic_class: "CreativeWork",
    graph_ownership: "Agent-Graph",
    does_not_define_graph_schema: true,
    published_structured_data_context: fn::artifact_published_context(),
    source_repository: $source.repository,
    source_path: $source.path,
    source_format: $source.format,
    source_commit_sha: $source.commit_sha,
    source_hash: $source.hash,
    date_created: IF $doc.dateCreated != NONE THEN <datetime>($doc.dateCreated + "T00:00:00Z") ELSE time::now() END,
    date_modified: time::now()
  };
};

DEFINE FUNCTION fn::map_blueprint_import_v1($doc: object, $source: object) {
  RETURN {
    context: fn::artifact_source_context(),
    type: "ag:Blueprint",
    blueprint_id: $doc.blueprint_id,
    name: $doc.name,
    version: IF $doc.version != NONE THEN $doc.version ELSE "0.1.0" END,
    blueprint_type: type::thing("blueprint_entity_type", $doc.blueprint_type),
    objective: type::thing("blueprint_objective", $doc.objective),
    lifecycle_status: IF $doc.status != NONE THEN $doc.status ELSE "draft" END,
    description: $doc.description,
    creator: IF $doc.creator != NONE THEN $doc.creator ELSE { type: "Organization", name: "AGenNext" } END,
    publisher: IF $doc.publisher != NONE THEN $doc.publisher ELSE { type: "Organization", name: "AGenNext" } END,
    keywords: $doc.keywords,
    audience: $doc.audience,
    about: $doc.about,
    date_created: IF $doc.dateCreated != NONE THEN <datetime>($doc.dateCreated + "T00:00:00Z") ELSE time::now() END,
    date_modified: time::now(),
    graph_context_owner: "Agent-Graph",
    semantic_class: "CreativeWork",
    graph_ownership: "Agent-Graph",
    does_not_define_graph_schema: true,
    published_structured_data_context: fn::artifact_published_context(),
    mission: $doc.mission,
    operating_constraints: $doc.operating_constraints,
    required_protocols: $doc.required_protocols,
    required_roles: $doc.required_roles,
    optional_roles: $doc.optional_roles,
    required_loops: $doc.required_loops,
    required_gates: $doc.required_gates,
    success_metrics: $doc.success_metrics,
    compatibility: $doc.compatibility,
    output_contract: $doc.output_contract,
    changelog: $doc.changelog,
    source_repository: $source.repository,
    source_path: $source.path,
    source_format: $source.format,
    source_commit_sha: $source.commit_sha,
    source_hash: $source.hash
  };
};

-- -----------------------------------------------------------------------------
-- Record creation helpers
-- -----------------------------------------------------------------------------

DEFINE FUNCTION fn::create_skill_source_record_v1($doc: object, $source: object) {
  LET $mapped = fn::map_skill_import_v1($doc, $source);

  RETURN CREATE skill_source_v1 CONTENT $mapped;
};

DEFINE FUNCTION fn::create_blueprint_source_record_v1($doc: object, $source: object) {
  LET $mapped = fn::map_blueprint_import_v1($doc, $source);

  RETURN CREATE blueprint_source_v1 CONTENT $mapped;
};

DEFINE FUNCTION fn::map_artifact_import_v1($artifact_kind: record<artifact_kind>, $doc: object, $source: object) {
  LET $kind = SELECT * FROM ONLY $artifact_kind;

  RETURN IF $kind.key = "skill" THEN fn::map_skill_import_v1($doc, $source)
    ELSE IF $kind.key = "blueprint" THEN fn::map_blueprint_import_v1($doc, $source)
    ELSE {
      error: true,
      message: "Unsupported artifact kind for import mapping"
    }
  END;
};
