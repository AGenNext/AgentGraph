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

    IF $version.len() = 0 {
        RETURN NONE;
    };

    LET $snapshot = $version[0].agent_snapshot;
    RETURN UPDATE ONLY type::record("agent", $agent_id) CONTENT $snapshot;
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
    RETURN UPSERT ONLY $record CONTENT $human;
};

DEFINE FUNCTION OVERWRITE fn::runtime::memory::upsert($memory: object) -> object {
    LET $record = type::record("memory_object", <string>$memory.id);
    RETURN UPSERT ONLY $record CONTENT $memory;
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
    RETURN true;
};

DEFINE FUNCTION OVERWRITE fn::runtime::instruction::upsert($instruction: object) -> object {
    LET $record = type::record("instruction_doc", <string>$instruction.id);
    RETURN UPSERT ONLY $record CONTENT $instruction;
};

DEFINE FUNCTION OVERWRITE fn::runtime::policy::upsert($policy: object) -> object {
    LET $record = type::record("policy_doc", <string>$policy.id);
    RETURN UPSERT ONLY $record CONTENT $policy;
};

DEFINE FUNCTION OVERWRITE fn::runtime::artifact::upsert($artifact: object) -> object {
    LET $record = type::record("artifact_ref", <string>$artifact.id);
    RETURN UPSERT ONLY $record CONTENT $artifact;
};

DEFINE FUNCTION OVERWRITE fn::runtime::artifact::get($artifact_id: string) -> option<object> {
    RETURN SELECT * FROM ONLY type::record("artifact_ref", $artifact_id);
};

DEFINE FUNCTION OVERWRITE fn::runtime::artifact::list(
    $artifact_type: option<string>,
    $status: option<string>
) -> array<object> {
    RETURN SELECT * FROM artifact_ref
    WHERE (type::is_none($artifact_type) OR $artifact_type = "" OR artifact_type = $artifact_type)
      AND (type::is_none($status) OR $status = "" OR status = $status)
    ORDER BY created_at DESC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::secret::upsert($secret: object) -> object {
    LET $record = type::record("secret_ref", <string>$secret.id);
    RETURN UPSERT ONLY $record CONTENT $secret;
};

DEFINE FUNCTION OVERWRITE fn::runtime::protocol::upsert($protocol: object) -> object {
    LET $record = type::record("protocol_doc", <string>$protocol.id);
    RETURN UPSERT ONLY $record CONTENT $protocol;
};

DEFINE FUNCTION OVERWRITE fn::runtime::protocol::get($protocol_id: string) -> option<object> {
    RETURN SELECT * FROM ONLY type::record("protocol_doc", $protocol_id);
};

DEFINE FUNCTION OVERWRITE fn::runtime::protocol::list(
    $protocol_type: option<string>,
    $status: option<string>
) -> array<object> {
    RETURN SELECT * FROM protocol_doc
    WHERE (type::is_none($protocol_type) OR $protocol_type = "" OR protocol_type = $protocol_type)
      AND (type::is_none($status) OR $status = "" OR status = $status)
    ORDER BY updated_at DESC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::upsert($identity: object) -> object {
    LET $record = type::record("identity_ref", <string>$identity.id);
    RETURN UPSERT ONLY $record CONTENT $identity;
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::get($identity_id: string) -> option<object> {
    RETURN SELECT * FROM ONLY type::record("identity_ref", $identity_id);
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::list(
    $identity_type: option<string>,
    $status: option<string>
) -> array<object> {
    RETURN SELECT * FROM identity_ref
    WHERE (type::is_none($identity_type) OR $identity_type = "" OR identity_type = $identity_type)
      AND (type::is_none($status) OR $status = "" OR status = $status)
    ORDER BY updated_at DESC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::auth::session::upsert($session: object) -> object {
    LET $record = type::record("auth_session", <string>$session.id);
    RETURN UPSERT ONLY $record CONTENT $session;
};

DEFINE FUNCTION OVERWRITE fn::runtime::auth::session::get($session_id: string) -> option<object> {
    RETURN SELECT * FROM ONLY type::record("auth_session", $session_id);
};

DEFINE FUNCTION OVERWRITE fn::runtime::auth::session::list(
    $state: option<string>,
    $subject_ref: option<string>
) -> array<object> {
    RETURN SELECT * FROM auth_session
    WHERE (type::is_none($state) OR $state = "" OR state = $state)
      AND (type::is_none($subject_ref) OR $subject_ref = "" OR subject_ref = $subject_ref)
    ORDER BY issued_at DESC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::auth::session::revoke($session_id: string) -> option<object> {
    LET $record = type::record("auth_session", $session_id);
    LET $existing = SELECT * FROM ONLY $record;

    IF !($existing) {
        RETURN NONE;
    };

    RETURN UPDATE ONLY $record SET
        state = "revoked",
        revoked_at = time::now(),
        updated_at = time::now();
};

DEFINE FUNCTION OVERWRITE fn::runtime::auth::session::authorize(
    $session_id: string,
    $scope: string
) -> bool {
    LET $current_session = SELECT * FROM ONLY type::record("auth_session", $session_id);

    IF !($current_session) {
        RETURN false;
    };

    IF $current_session.state != "active" {
        RETURN false;
    };

    IF $current_session.expires_at AND $current_session.expires_at < time::now() {
        RETURN false;
    };

    RETURN $scope IN $current_session.scopes;
};

DEFINE FUNCTION OVERWRITE fn::runtime::audit::append($event: object) -> object {
    LET $record = type::record("audit_event", <string>$event.id);
    RETURN CREATE ONLY $record CONTENT $event;
};

DEFINE FUNCTION OVERWRITE fn::runtime::audit::link_target(
    $event_id: string,
    $target_ref: string
) -> bool {
    RETURN true;
};

DEFINE FUNCTION OVERWRITE fn::runtime::audit::caused_by(
    $event_id: string,
    $parent_event_ref: string
) -> bool {
    RETURN true;
};
