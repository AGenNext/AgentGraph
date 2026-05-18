-- SurrealDB-native validation blocks for the schema graph and repository seed.

DEFINE FUNCTION OVERWRITE fn::validation::assert($condition: bool, $message: string) -> bool {
    IF !$condition {
        THROW $message;
    };

    RETURN true;
};

DEFINE FUNCTION OVERWRITE fn::validation::relation_summary(
    $table: string,
    $expected_count: int,
    $edges: array<object>
) -> bool {
    LET $rows = SELECT VALUE id FROM type::table($table);
    IF $expected_count > 0 AND $rows.len() != $expected_count {
        THROW "Unexpected edge count for " + $table + ": expected " + <string>$expected_count + ", got " + <string>$rows.len();
    };

    FOR $edge IN $edges {
        LET $matches = SELECT VALUE id FROM type::table($table) WHERE in = $edge.in AND out = $edge.out LIMIT 1;
        IF $matches.len() = 0 {
            THROW "Missing edge in " + $table + ": " + $edge.in + " -> " + $edge.out;
        };
    };

    RETURN true;
};

DEFINE FUNCTION OVERWRITE fn::validation::schema_paths(
    $expected_count: int,
    $paths: array<object>
) -> bool {
    LET $rows = SELECT VALUE id FROM schema_path;
    IF $expected_count > 0 AND $rows.len() != $expected_count {
        THROW "Unexpected schema_path count: expected " + <string>$expected_count + ", got " + <string>$rows.len();
    };

    FOR $path IN $paths {
        LET $matches = SELECT * FROM schema_path WHERE path_key = $path.path_key LIMIT 1;
        IF $matches.len() = 0 {
            THROW "Missing schema_path row: " + $path.path_key;
        };

        LET $row = $matches[0];
        IF $row.relation != $path.relation {
            THROW "schema_path relation mismatch for " + $path.path_key;
        };
        IF $row.source_id != $path.source_id {
            THROW "schema_path source_id mismatch for " + $path.path_key;
        };
        IF $row.target_id != $path.target_id {
            THROW "schema_path target_id mismatch for " + $path.path_key;
        };
        IF $row.hop_count != $path.hop_count {
            THROW "schema_path hop_count mismatch for " + $path.path_key;
        };
        IF $row.route != $path.route {
            THROW "schema_path route mismatch for " + $path.path_key;
        };
        IF $row.path != $path.path {
            THROW "schema_path path mismatch for " + $path.path_key;
        };
        IF $row.via_source_ids != $path.via_source_ids {
            THROW "schema_path via_source_ids mismatch for " + $path.path_key;
        };
        IF $row.source_record != $path.source_record {
            THROW "schema_path source_record mismatch for " + $path.path_key;
        };
        IF $row.target_record != $path.target_record {
            THROW "schema_path target_record mismatch for " + $path.path_key;
        };
        IF $row.generated_from != $path.generated_from {
            THROW "schema_path generated_from mismatch for " + $path.path_key;
        };
    };

    RETURN true;
};

DEFINE FUNCTION OVERWRITE fn::validation::knowledge_graph() -> bool {
    LET $maintainer = SELECT VALUE id FROM human WHERE id = human:maintainer LIMIT 1;
    IF $maintainer.len() = 0 {
        THROW "Missing human:maintainer";
    };

    LET $platform = SELECT VALUE id FROM entity WHERE id = entity:agent_graph_platform LIMIT 1;
    IF $platform.len() = 0 {
        THROW "Missing entity:agent_graph_platform";
    };

    LET $runtime = SELECT VALUE id FROM entity WHERE id = entity:surrealdb_runtime LIMIT 1;
    IF $runtime.len() = 0 {
        THROW "Missing entity:surrealdb_runtime";
    };

    LET $vocabulary = SELECT VALUE id FROM entity WHERE id = entity:schema_org_vocabulary LIMIT 1;
    IF $vocabulary.len() = 0 {
        THROW "Missing entity:schema_org_vocabulary";
    };

    LET $memory = SELECT * FROM memory_object WHERE id = memory_object:repo_knowledge_graph LIMIT 1;
    IF $memory.len() = 0 {
        THROW "Missing memory_object:repo_knowledge_graph";
    };

    LET $seed = $memory[0];
    IF $seed.content.summary != "Core semantic graph for the repo, runtime, and schema assets." {
        THROW "memory_object:repo_knowledge_graph summary mismatch";
    };
    IF $seed.content.nodes != [
        "human:maintainer",
        "entity:agent_graph_platform",
        "entity:surrealdb_runtime",
        "entity:schema_org_vocabulary"
    ] {
        THROW "memory_object:repo_knowledge_graph nodes mismatch";
    };
    IF $seed.content.edges != [
        "knowledge_about",
        "instruction_applies_to",
        "policy_applies_to",
        "generated_from",
        "entity_kind"
    ] {
        THROW "memory_object:repo_knowledge_graph edges mismatch";
    };

    LET $artifact = SELECT VALUE id FROM artifact_ref WHERE id = artifact_ref:knowledge_graph_seed LIMIT 1;
    IF $artifact.len() = 0 {
        THROW "Missing artifact_ref:knowledge_graph_seed";
    };

    LET $event = SELECT VALUE id FROM audit_event WHERE id = audit_event:knowledge_graph_seeded LIMIT 1;
    IF $event.len() = 0 {
        THROW "Missing audit_event:knowledge_graph_seeded";
    };

    LET $knowledge_about = SELECT VALUE id FROM knowledge_about WHERE in = memory_object:repo_knowledge_graph AND out = entity:agent_graph_platform LIMIT 1;
    IF $knowledge_about.len() = 0 {
        THROW "Missing knowledge_about edge to entity:agent_graph_platform";
    };

    LET $knowledge_about_runtime = SELECT VALUE id FROM knowledge_about WHERE in = memory_object:repo_knowledge_graph AND out = entity:surrealdb_runtime LIMIT 1;
    IF $knowledge_about_runtime.len() = 0 {
        THROW "Missing knowledge_about edge to entity:surrealdb_runtime";
    };

    LET $knowledge_about_vocab = SELECT VALUE id FROM knowledge_about WHERE in = memory_object:repo_knowledge_graph AND out = entity:schema_org_vocabulary LIMIT 1;
    IF $knowledge_about_vocab.len() = 0 {
        THROW "Missing knowledge_about edge to entity:schema_org_vocabulary";
    };

    LET $entity_kind_platform = SELECT VALUE id FROM entity_kind WHERE in = entity:agent_graph_platform AND out = schema_term:class_schema_organization LIMIT 1;
    IF $entity_kind_platform.len() = 0 {
        THROW "Missing entity_kind edge for entity:agent_graph_platform";
    };

    LET $entity_kind_runtime = SELECT VALUE id FROM entity_kind WHERE in = entity:surrealdb_runtime AND out = schema_term:class_schema_softwareapplication LIMIT 1;
    IF $entity_kind_runtime.len() = 0 {
        THROW "Missing entity_kind edge for entity:surrealdb_runtime";
    };

    LET $entity_kind_vocab = SELECT VALUE id FROM entity_kind WHERE in = entity:schema_org_vocabulary AND out = schema_term:class_schema_creativework LIMIT 1;
    IF $entity_kind_vocab.len() = 0 {
        THROW "Missing entity_kind edge for entity:schema_org_vocabulary";
    };

    LET $instruction_maintainer = SELECT VALUE id FROM instruction_applies_to WHERE in = instruction_doc:surreal_runtime_guide AND out = human:maintainer LIMIT 1;
    IF $instruction_maintainer.len() = 0 {
        THROW "Missing instruction_applies_to edge to human:maintainer";
    };

    LET $instruction_memory = SELECT VALUE id FROM instruction_applies_to WHERE in = instruction_doc:surreal_runtime_guide AND out = memory_object:repo_knowledge_graph LIMIT 1;
    IF $instruction_memory.len() = 0 {
        THROW "Missing instruction_applies_to edge to memory_object:repo_knowledge_graph";
    };

    LET $instruction_runtime = SELECT VALUE id FROM instruction_applies_to WHERE in = instruction_doc:surreal_runtime_guide AND out = entity:surrealdb_runtime LIMIT 1;
    IF $instruction_runtime.len() = 0 {
        THROW "Missing instruction_applies_to edge to entity:surrealdb_runtime";
    };

    LET $policy_maintainer = SELECT VALUE id FROM policy_applies_to WHERE in = policy_doc:graph_governance AND out = human:maintainer LIMIT 1;
    IF $policy_maintainer.len() = 0 {
        THROW "Missing policy_applies_to edge to human:maintainer";
    };

    LET $policy_memory = SELECT VALUE id FROM policy_applies_to WHERE in = policy_doc:graph_governance AND out = memory_object:repo_knowledge_graph LIMIT 1;
    IF $policy_memory.len() = 0 {
        THROW "Missing policy_applies_to edge to memory_object:repo_knowledge_graph";
    };

    LET $policy_runtime = SELECT VALUE id FROM policy_applies_to WHERE in = policy_doc:graph_governance AND out = entity:surrealdb_runtime LIMIT 1;
    IF $policy_runtime.len() = 0 {
        THROW "Missing policy_applies_to edge to entity:surrealdb_runtime";
    };

    LET $policy_artifact = SELECT VALUE id FROM policy_applies_to WHERE in = policy_doc:graph_governance AND out = artifact_ref:knowledge_graph_seed LIMIT 1;
    IF $policy_artifact.len() = 0 {
        THROW "Missing policy_applies_to edge to artifact_ref:knowledge_graph_seed";
    };

    LET $generated_instruction = SELECT VALUE id FROM generated_from WHERE in = artifact_ref:knowledge_graph_seed AND out = instruction_doc:surreal_runtime_guide LIMIT 1;
    IF $generated_instruction.len() = 0 {
        THROW "Missing generated_from edge to instruction_doc:surreal_runtime_guide";
    };

    LET $generated_policy = SELECT VALUE id FROM generated_from WHERE in = artifact_ref:knowledge_graph_seed AND out = policy_doc:graph_governance LIMIT 1;
    IF $generated_policy.len() = 0 {
        THROW "Missing generated_from edge to policy_doc:graph_governance";
    };

    LET $generated_memory = SELECT VALUE id FROM generated_from WHERE in = artifact_ref:knowledge_graph_seed AND out = memory_object:repo_knowledge_graph LIMIT 1;
    IF $generated_memory.len() = 0 {
        THROW "Missing generated_from edge to memory_object:repo_knowledge_graph";
    };

    LET $generated_vocab = SELECT VALUE id FROM generated_from WHERE in = artifact_ref:knowledge_graph_seed AND out = entity:schema_org_vocabulary LIMIT 1;
    IF $generated_vocab.len() = 0 {
        THROW "Missing generated_from edge to entity:schema_org_vocabulary";
    };

    LET $acted_on = SELECT VALUE id FROM acted_on WHERE in = audit_event:knowledge_graph_seeded AND out = artifact_ref:knowledge_graph_seed LIMIT 1;
    IF $acted_on.len() = 0 {
        THROW "Missing acted_on edge to artifact_ref:knowledge_graph_seed";
    };

    RETURN true;
};
