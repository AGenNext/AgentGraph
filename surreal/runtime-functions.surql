DEFINE FUNCTION OVERWRITE fn::runtime::agent::list(
    $status: option<string>,
    $search: option<string>
) -> array<object> {
    LET $needle = IF type::is_none($search) OR $search = "" {
        NONE
    } ELSE {
        string::lowercase($search)
    };

    RETURN SELECT * FROM agent
    WHERE (type::is_none($status) OR $status = "" OR status = $status)
      AND (
        type::is_none($needle)
        OR string::lowercase(name) CONTAINS $needle
        OR string::lowercase(description ?? "") CONTAINS $needle
      )
    ORDER BY created_at DESC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::agent::get($agent_id: string) -> option<object> {
    RETURN SELECT * FROM ONLY type::record("agent", $agent_id);
};

DEFINE FUNCTION OVERWRITE fn::runtime::agent::versions($agent_id: string) -> array<object> {
    RETURN SELECT * FROM agent_version
    WHERE agent_id = $agent_id
    ORDER BY created_at DESC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::agent::create(
    $agent_id: string,
    $agent: object
) -> object {
    LET $record = type::record("agent", $agent_id);
    RETURN CREATE ONLY $record CONTENT $agent;
};

DEFINE FUNCTION OVERWRITE fn::runtime::agent::update(
    $agent_id: string,
    $agent: object,
    $changes: option<string>
) -> option<object> {
    LET $record = type::record("agent", $agent_id);
    LET $existing = SELECT * FROM ONLY $record;

    IF !($existing) {
        RETURN NONE;
    };

    RETURN UPDATE ONLY $record CONTENT $agent;
};

DEFINE FUNCTION OVERWRITE fn::runtime::agent::delete($agent_id: string) -> bool {
    LET $record = type::record("agent", $agent_id);
    LET $existing = SELECT * FROM ONLY $record;

    IF !($existing) {
        RETURN false;
    };

    DELETE ONLY $record;

    RETURN true;
};

DEFINE FUNCTION OVERWRITE fn::runtime::agent::restore(
    $agent_id: string,
    $version_id: string
) -> option<object> {
    LET $version_record = type::record("agent_version", $version_id);
    LET $version = SELECT * FROM ONLY $version_record;

    IF !($version) OR $version.agent_id != $agent_id {
        RETURN NONE;
    };

    LET $snapshot = $version.agent_snapshot;
    RETURN UPDATE ONLY type::record("agent", $agent_id) CONTENT {
        ...$snapshot,
        updated_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::entity::list($type: option<string>) -> array<object> {
    RETURN SELECT * FROM entity
    WHERE type::is_none($type) OR $type = "" OR type = $type
    ORDER BY name ASC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::entity::upsert($entity: object) -> object {
    LET $record = type::record("entity", <string>$entity.id);
    LET $upserted = UPSERT ONLY $record CONTENT $entity;
    LET $schema_term = (SELECT VALUE id FROM schema_term WHERE source_id = $entity.type LIMIT 1)[0];

    IF !!$schema_term {
        DELETE entity_kind WHERE in = $record;
        RELATE $record->entity_kind->$schema_term CONTENT { source: "runtime" };
    };

    RETURN $upserted;
};

DEFINE FUNCTION OVERWRITE fn::runtime::human::upsert($human: object) -> object {
    LET $record = type::record("human", <string>$human.id);
    RETURN UPSERT ONLY $record CONTENT {
        ...$human,
        updated_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::memory::upsert($memory: object) -> object {
    LET $record = type::record("memory_object", <string>$memory.id);
    RETURN UPSERT ONLY $record CONTENT {
        ...$memory,
        updated_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::memory::list(
    $memory_type: option<string>,
    $owner_ref: option<string>
) -> array<object> {
    RETURN SELECT * FROM memory_object
    WHERE (type::is_none($memory_type) OR $memory_type = "" OR memory_type = $memory_type)
      AND (type::is_none($owner_ref) OR $owner_ref = "" OR owner_ref = $owner_ref)
    ORDER BY updated_at DESC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::memory::attach_owner(
    $memory_id: string,
    $owner_ref: string
) -> bool {
    LET $memory_record = type::record("memory_object", $memory_id);
    LET $owner_record = type::thing($owner_ref);

    DELETE memory_owned_by WHERE in = $memory_record;
    RELATE $memory_record->memory_owned_by->$owner_record CONTENT {
        created_at: time::now(),
        source: "runtime"
    };

    UPDATE ONLY $memory_record SET owner_ref = $owner_ref, updated_at = time::now();
    RETURN true;
};

DEFINE FUNCTION OVERWRITE fn::runtime::instruction::upsert($instruction: object) -> object {
    LET $record = type::record("instruction_doc", <string>$instruction.id);
    RETURN UPSERT ONLY $record CONTENT {
        ...$instruction,
        updated_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::policy::upsert($policy: object) -> object {
    LET $record = type::record("policy_doc", <string>$policy.id);
    RETURN UPSERT ONLY $record CONTENT {
        ...$policy,
        updated_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::artifact::upsert($artifact: object) -> object {
    LET $record = type::record("artifact_ref", <string>$artifact.id);
    RETURN UPSERT ONLY $record CONTENT {
        ...$artifact,
        updated_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::secret::upsert($secret: object) -> object {
    LET $record = type::record("secret_ref", <string>$secret.id);
    RETURN UPSERT ONLY $record CONTENT {
        ...$secret,
        updated_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::audit::append($event: object) -> object {
    LET $record = type::record("audit_event", <string>$event.id);
    RETURN CREATE ONLY $record CONTENT {
        ...$event,
        event_time: $event.event_time ?? time::now(),
        created_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::audit::link_target(
    $event_id: string,
    $target_ref: string
) -> bool {
    LET $event_record = type::record("audit_event", $event_id);
    LET $target_record = type::thing($target_ref);
    RELATE $event_record->acted_on->$target_record CONTENT {
        created_at: time::now(),
        source: "runtime"
    };
    RETURN true;
};

DEFINE FUNCTION OVERWRITE fn::runtime::audit::caused_by(
    $event_id: string,
    $parent_event_ref: string
) -> bool {
    LET $event_record = type::record("audit_event", $event_id);
    LET $parent_record = type::thing($parent_event_ref);
    RELATE $event_record->caused_by->$parent_record CONTENT {
        created_at: time::now(),
        source: "runtime"
    };
    RETURN true;
};
