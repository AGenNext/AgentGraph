DEFINE EVENT OVERWRITE agent_versioning ON TABLE agent
    WHEN $event = "CREATE" OR $event = "UPDATE" OR $event = "DELETE"
    THEN {
        LET $agent_record = $value.id;
        LET $agent_id = <string>meta::id($value.id);
        LET $snapshot = $value;
        LET $changes = IF $event = "CREATE" {
            "Initial version"
        } ELSE IF $event = "DELETE" {
            "Deleted agent"
        } ELSE {
            "Updated agent configuration"
        };

        UPDATE agent_version SET is_current = false WHERE agent_id = $agent_id;

        LET $version_record = CREATE agent_version SET
            agent = $agent_record,
            agent_id = $agent_id,
            version = $snapshot.version ?? "1.0",
            changes = $changes,
            created_at = time::now(),
            is_current = $event != "DELETE",
            event_type = string::lowercase($event),
            agent_snapshot = $snapshot;

        IF $event != "DELETE" {
            RELATE $version_record->version_of->$agent_record CONTENT {
                created_at: time::now()
            };
        };
    };

DEFINE EVENT OVERWRITE memory_object_timestamps ON TABLE memory_object
    WHEN $event = "CREATE" OR $event = "UPDATE"
    THEN {
        UPDATE ONLY $value.id SET updated_at = time::now();
    };

DEFINE EVENT OVERWRITE instruction_doc_timestamps ON TABLE instruction_doc
    WHEN $event = "CREATE" OR $event = "UPDATE"
    THEN {
        UPDATE ONLY $value.id SET updated_at = time::now();
    };

DEFINE EVENT OVERWRITE policy_doc_timestamps ON TABLE policy_doc
    WHEN $event = "CREATE" OR $event = "UPDATE"
    THEN {
        UPDATE ONLY $value.id SET updated_at = time::now();
    };

DEFINE EVENT OVERWRITE artifact_ref_timestamps ON TABLE artifact_ref
    WHEN $event = "CREATE" OR $event = "UPDATE"
    THEN {
        UPDATE ONLY $value.id SET updated_at = time::now();
    };

DEFINE EVENT OVERWRITE secret_ref_timestamps ON TABLE secret_ref
    WHEN $event = "CREATE" OR $event = "UPDATE"
    THEN {
        UPDATE ONLY $value.id SET updated_at = time::now();
    };

DEFINE EVENT OVERWRITE oidc_provider_timestamps ON TABLE oidc_provider
    WHEN $event = "CREATE" OR $event = "UPDATE"
    THEN {
        UPDATE ONLY $value.id SET updated_at = time::now();
    };

DEFINE EVENT OVERWRITE oidc_validation_timestamps ON TABLE oidc_validation
    WHEN $event = "CREATE" OR $event = "UPDATE"
    THEN {
        UPDATE ONLY $value.id SET updated_at = time::now();
    };
