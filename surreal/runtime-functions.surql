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

DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::discover($issuer_url: string) -> object {
    LET $discovery_url = $issuer_url + "/.well-known/openid-configuration";
    RETURN http::get($discovery_url);
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::upsert(
    $provider_key: string,
    $issuer_url: string,
    $configuration: object,
    $issuer_vendor: option<string>
) -> object {
    LET $record = type::record("oidc_provider", $provider_key);
    LET $discovery_url = $configuration.discovery_url ?? ($issuer_url + "/.well-known/openid-configuration");

    RETURN UPSERT ONLY $record CONTENT {
        provider_key: $provider_key,
        issuer_vendor: $issuer_vendor ?? "generic",
        issuer_url: $issuer_url,
        discovery_url: $discovery_url,
        jwks_uri: $configuration.jwks_uri ?? NONE,
        authorization_endpoint: $configuration.authorization_endpoint ?? NONE,
        token_endpoint: $configuration.token_endpoint ?? NONE,
        userinfo_endpoint: $configuration.userinfo_endpoint ?? NONE,
        end_session_endpoint: $configuration.end_session_endpoint ?? NONE,
        scopes_supported: $configuration.scopes_supported ?? [],
        response_types_supported: $configuration.response_types_supported ?? [],
        grant_types_supported: $configuration.grant_types_supported ?? [],
        id_token_signing_alg_values_supported: $configuration.id_token_signing_alg_values_supported ?? [],
        claims_supported: $configuration.claims_supported ?? [],
        subject_types_supported: $configuration.subject_types_supported ?? [],
        discovery_document: $configuration,
        status: "active",
        last_discovered_at: time::now(),
        refreshed_at: time::now(),
        created_at: time::now(),
        updated_at: time::now()
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::get($provider_key: string) -> option<object> {
    RETURN SELECT * FROM ONLY type::record("oidc_provider", $provider_key);
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::list($status: option<string>) -> array<object> {
    RETURN SELECT * FROM oidc_provider
    WHERE type::is_none($status) OR $status = "" OR status = $status
    ORDER BY updated_at DESC;
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::sync(
    $provider_key: string,
    $issuer_url: string,
    $issuer_vendor: option<string>
) -> object {
    LET $configuration = fn::runtime::identity::oidc::discover($issuer_url);
    RETURN fn::runtime::identity::oidc::upsert($provider_key, $issuer_url, $configuration, $issuer_vendor);
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::access_profile(
    $provider_key: string
) -> option<object> {
    LET $provider = SELECT * FROM ONLY type::record("oidc_provider", $provider_key);

    IF !($provider) {
        RETURN NONE;
    };

    RETURN {
        access_name: "oidc_" + $provider.provider_key,
        issuer_vendor: $provider.issuer_vendor,
        issuer_label: IF $provider.issuer_vendor = "waltid" {
            "WaltID"
        } ELSE {
            "OpenID Connect"
        },
        issuer_url: $provider.issuer_url,
        discovery_url: $provider.discovery_url,
        jwks_uri: $provider.jwks_uri,
        token_endpoint: $provider.token_endpoint,
        validation_mode: IF type::is_none($provider.jwks_uri) {
            "pending_discovery"
        } ELSE {
            "jwks_uri"
        },
        claims: {
            issuer: "iss",
            subject: "sub",
            audience: "aud",
            expiry: "exp",
            not_before: "nbf",
            token_id: "jti"
        },
        surreal: {
            token_access: "DEFINE ACCESS ... TYPE JWT URL <jwks_uri>",
            subject_table: "identity_ref",
            session_table: "auth_session",
            validation_table: "oidc_validation"
        }
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::waltid::profile(
    $provider_key: string,
    $issuer_url: string
) -> object {
    RETURN {
        provider_key: $provider_key,
        issuer_vendor: "waltid",
        issuer_label: "WaltID",
        issuer_url: $issuer_url,
        discovery_url: $issuer_url + "/.well-known/openid-configuration",
        jwks_uri: NONE,
        authorization_endpoint: NONE,
        token_endpoint: NONE,
        userinfo_endpoint: NONE,
        end_session_endpoint: NONE,
        scopes_supported: ["openid", "profile", "email"],
        response_types_supported: ["code"],
        grant_types_supported: ["authorization_code", "refresh_token"],
        id_token_signing_alg_values_supported: ["RS256"],
        claims_supported: ["iss", "sub", "aud", "exp", "nbf", "iat", "jti", "email", "name"],
        subject_types_supported: ["public"],
        validation_mode: "jwks_uri",
        surreal: {
            provider_table: "oidc_provider",
            validation_table: "oidc_validation",
            session_table: "auth_session",
            access_name: "oidc_" + $provider_key,
            access_definition: "DEFINE ACCESS ... TYPE JWT URL <jwks_uri>"
        }
    };
};

DEFINE FUNCTION OVERWRITE fn::runtime::identity::oidc::waltid::sync(
    $provider_key: string,
    $issuer_url: string
) -> object {
    LET $configuration = fn::runtime::identity::oidc::discover($issuer_url);
    RETURN fn::runtime::identity::oidc::upsert($provider_key, $issuer_url, $configuration, "waltid");
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

DEFINE FUNCTION OVERWRITE fn::runtime::auth::session::record_oidc_validation(
    $session_id: string,
    $validation_id: string,
    $provider_key: string,
    $issuer_vendor: string,
    $subject_ref: option<string>,
    $claims: object,
    $headers: object,
    $token_issuer: option<string>,
    $token_subject: option<string>,
    $token_audience: array<string>,
    $token_kid: option<string>,
    $token_algorithm: option<string>,
    $validation_status: string,
    $validation_reason: option<string>
) -> object {
    LET $session_record = type::record("auth_session", $session_id);
    LET $provider_record = type::record("oidc_provider", $provider_key);
    LET $validation_record = type::record("oidc_validation", $validation_id);

    LET $validation = UPSERT ONLY $validation_record CONTENT {
        provider_ref: $provider_record,
        issuer_vendor: $issuer_vendor,
        session_ref: $session_record,
        subject_ref: $subject_ref,
        token_issuer: $token_issuer,
        token_subject: $token_subject,
        token_audience: $token_audience,
        token_kid: $token_kid,
        token_algorithm: $token_algorithm,
        validation_status: $validation_status,
        validation_reason: $validation_reason,
        claims: $claims,
        headers: $headers,
        validated_at: time::now(),
        created_at: time::now(),
        updated_at: time::now()
    };

    UPDATE ONLY $session_record SET
        provider_ref = $provider_record,
        issuer_vendor = $issuer_vendor,
        auth_method = "oidc-jwt",
        token_issuer = $token_issuer,
        token_subject = $token_subject,
        token_audience = $token_audience,
        token_kid = $token_kid,
        token_algorithm = $token_algorithm,
        validation_status = $validation_status,
        validation_reason = $validation_reason,
        validated_at = time::now(),
        claims = $claims,
        updated_at = time::now();

    RETURN $validation;
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
