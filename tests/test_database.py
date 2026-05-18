"""SurrealDB schema and configuration tests."""

import json
from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "surreal" / "schema" / "schemaorg-vocabulary.surql"
KNOWLEDGE_GRAPH_PATH = Path(__file__).resolve().parents[1] / "surreal" / "knowledge-graph.surql"
PATHS_PATH = Path(__file__).resolve().parents[1] / "surreal" / "schema" / "schemaorg-paths.surql"
PATHS_SUMMARY_PATH = Path(__file__).resolve().parents[1] / "surreal" / "schema" / "schemaorg-paths-summary.json"
VALIDATION_PATH = Path(__file__).resolve().parents[1] / "surreal" / "validation" / "graph-validation.surql"


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

    def test_schema_term_accepts_jsonld_text_and_relation_metadata(self):
        schema_meta = (Path(__file__).resolve().parents[1] / "surreal" / "schema" / "schema-meta.surql").read_text(
            encoding="utf-8"
        )
        assert "DEFINE FIELD label ON TABLE schema_term TYPE any;" in schema_meta
        assert "DEFINE FIELD comment ON TABLE schema_term TYPE any;" in schema_meta
        assert "DEFINE FIELD source ON TABLE subclass_of TYPE option<string>;" in schema_meta
        assert "DEFINE FIELD created_at ON TABLE subclass_of TYPE option<datetime>;" in schema_meta


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


class TestValidationBlocks:
    """Test the SurrealDB-native validation blocks."""

    def test_validation_file_exists(self):
        assert VALIDATION_PATH.exists()

    def test_validation_file_defines_functions(self):
        validation = VALIDATION_PATH.read_text(encoding="utf-8")
        assert "DEFINE FUNCTION OVERWRITE fn::validation::relation_summary" in validation
        assert "DEFINE FUNCTION OVERWRITE fn::validation::schema_paths" in validation
        assert "DEFINE FUNCTION OVERWRITE fn::validation::knowledge_graph" in validation


class TestRuntimeNamespaces:
    """Test the runtime namespace definitions."""

    def test_runtime_schema_defines_artifact_protocol_identity_auth_tables(self):
        runtime_schema = (Path(__file__).resolve().parents[1] / "surreal" / "runtime-schema.surql").read_text(
            encoding="utf-8"
        )
        assert "DEFINE TABLE artifact_ref SCHEMAFULL;" in runtime_schema
        assert "DEFINE TABLE protocol_doc SCHEMAFULL;" in runtime_schema
        assert "DEFINE TABLE identity_ref SCHEMAFULL;" in runtime_schema
        assert "DEFINE TABLE auth_session SCHEMAFULL;" in runtime_schema

    def test_runtime_functions_define_artifact_protocol_identity_auth_namespaces(self):
        runtime_functions = (Path(__file__).resolve().parents[1] / "surreal" / "runtime-functions.surql").read_text(
            encoding="utf-8"
        )
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::artifact::list" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::protocol::upsert" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::identity::upsert" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::auth::session::authorize" in runtime_functions


class TestOidcRuntime:
    """Test the DB-native OIDC discovery and validation contract."""

    def test_runtime_schema_defines_oidc_tables_and_session_links(self):
        runtime_schema = (Path(__file__).resolve().parents[1] / "surreal" / "runtime-schema.surql").read_text(
            encoding="utf-8"
        )
        assert "DEFINE TABLE oidc_provider SCHEMAFULL;" in runtime_schema
        assert "DEFINE TABLE oidc_binding SCHEMAFULL;" in runtime_schema
        assert "DEFINE TABLE oidc_validation SCHEMAFULL;" in runtime_schema
        assert "DEFINE FIELD issuer_vendor ON TABLE oidc_provider TYPE string DEFAULT \"generic\";" in runtime_schema
        assert "DEFINE FIELD issuer_vendor ON TABLE auth_session TYPE string DEFAULT \"generic\";" in runtime_schema
        assert "DEFINE FIELD issuer_vendor ON TABLE oidc_validation TYPE string DEFAULT \"generic\";" in runtime_schema
        assert "DEFINE FIELD provider_ref ON TABLE auth_session TYPE option<record<oidc_provider>>;" in runtime_schema
        assert "DEFINE FIELD validation_status ON TABLE auth_session TYPE string DEFAULT \"pending\";" in runtime_schema
        assert "DEFINE INDEX oidc_provider_issuer_url ON TABLE oidc_provider FIELDS issuer_url UNIQUE;" in runtime_schema
        assert "DEFINE INDEX oidc_binding_key ON TABLE oidc_binding FIELDS binding_key UNIQUE;" in runtime_schema

    def test_runtime_functions_define_oidc_discovery_and_validation_helpers(self):
        runtime_functions = (Path(__file__).resolve().parents[1] / "surreal" / "runtime-functions.surql").read_text(
            encoding="utf-8"
        )
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::discover" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::sync" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::access_profile" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::waltid::profile" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::waltid::sync" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::binding::upsert" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::binding::materialize" in runtime_functions
        assert "DEFINE FUNCTION OVERWRITE fn::runtime::auth::session::record_oidc_validation" in runtime_functions
        assert "http::get($discovery_url)" in runtime_functions

    def test_runtime_events_define_oidc_timestamps(self):
        runtime_events = (Path(__file__).resolve().parents[1] / "surreal" / "runtime-events.surql").read_text(
            encoding="utf-8"
        )
        assert "DEFINE EVENT OVERWRITE oidc_provider_timestamps ON TABLE oidc_provider" in runtime_events
        assert "DEFINE EVENT OVERWRITE oidc_validation_timestamps ON TABLE oidc_validation" in runtime_events
        assert "DEFINE EVENT OVERWRITE oidc_binding_timestamps ON TABLE oidc_binding" in runtime_events
