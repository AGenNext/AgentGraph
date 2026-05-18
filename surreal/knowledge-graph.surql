-- Canonical SurrealDB knowledge graph for Agent-Graph.
-- This file seeds the repo's semantic backbone after the schema and runtime
-- tables are available.

UPSERT human:maintainer CONTENT {
    identity_type: "human",
    canonical_id: "human:maintainer",
    name: "Repository Maintainer",
    description: "Maintains the Agent-Graph runtime and documentation.",
    status: "active",
    world_location: { scope: "repository", repository: "Agent-Graph" },
    valid_from: time::now(),
    valid_to: NONE,
    created_at: time::now(),
    updated_at: time::now()
};

UPSERT entity:agent_graph_platform CONTENT {
    type: "schema:Organization",
    canonical_id: "entity:agent-graph-platform",
    name: "Agent-Graph Platform",
    description: "The repository and runtime platform as a knowledge node.",
    world_location: { scope: "repository", repository: "Agent-Graph" },
    valid_from: time::now(),
    valid_to: NONE,
    created_at: time::now(),
    updated_at: time::now()
};

UPSERT entity:surrealdb_runtime CONTENT {
    type: "schema:SoftwareApplication",
    canonical_id: "entity:surrealdb-runtime",
    name: "SurrealDB Runtime",
    description: "Database-native runtime layer for state, graph, and policy.",
    world_location: { scope: "database", database: "surrealdb" },
    valid_from: time::now(),
    valid_to: NONE,
    created_at: time::now(),
    updated_at: time::now()
};

UPSERT entity:schema_org_vocabulary CONTENT {
    type: "schema:CreativeWork",
    canonical_id: "entity:schema-org-vocabulary",
    name: "Schema.org Vocabulary",
    description: "Imported Schema.org vocabulary and relation graph.",
    world_location: { scope: "schema", repository: "Agent-Graph" },
    valid_from: time::now(),
    valid_to: NONE,
    created_at: time::now(),
    updated_at: time::now()
};

UPSERT memory_object:repo_knowledge_graph CONTENT {
    memory_type: "repository-knowledge",
    title: "Agent-Graph knowledge graph",
    content: {
        summary: "Core semantic graph for the repo, runtime, and schema assets.",
        nodes: [
            "human:maintainer",
            "entity:agent_graph_platform",
            "entity:surrealdb_runtime",
            "entity:schema_org_vocabulary"
        ],
        edges: [
            "knowledge_about",
            "instruction_applies_to",
            "policy_applies_to",
            "generated_from",
            "entity_kind"
        ]
    },
    content_text: "Semantic backbone for the Agent-Graph repository.",
    modality: "text",
    status: "active",
    source_kind: "surql",
    source_ref: "surreal/knowledge-graph.surql",
    created_by: "human:maintainer",
    owner_ref: "human:maintainer",
    importance: 10,
    world_location: { scope: "repository", repository: "Agent-Graph" },
    valid_from: time::now(),
    valid_to: NONE,
    created_at: time::now(),
    updated_at: time::now()
};

UPSERT instruction_doc:surreal_runtime_guide CONTENT {
    title: "SurrealDB Runtime Guide",
    source_path: "surreal/README.md",
    source_hash: NONE,
    body: "# SurrealDB Runtime Guide\n\nThe runtime layer owns semantic state, graph relations, and database-owned behavior.",
    format: "markdown",
    status: "active",
    valid_from: time::now(),
    valid_to: NONE,
    world_location: { scope: "repository", repository: "Agent-Graph" },
    created_at: time::now(),
    updated_at: time::now()
};

UPSERT policy_doc:graph_governance CONTENT {
    name: "Graph Governance Policy",
    policy_type: "governance",
    source_path: "surreal/AGENT.md",
    body: "The SurrealDB graph should stay database-native, append-only where required, and aligned with the imported Schema.org model.",
    status: "active",
    authority: "Agent-Graph",
    valid_from: time::now(),
    valid_to: NONE,
    world_location: { scope: "repository", repository: "Agent-Graph" },
    created_at: time::now(),
    updated_at: time::now()
};

UPSERT artifact_ref:knowledge_graph_seed CONTENT {
    artifact_type: "surql",
    name: "knowledge-graph.surql",
    uri: "surreal/knowledge-graph.surql",
    storage_kind: "repository",
    status: "active",
    owner_ref: "human:maintainer",
    created_by: "human:maintainer",
    world_location: { scope: "repository", repository: "Agent-Graph" },
    valid_from: time::now(),
    valid_to: NONE,
    created_at: time::now(),
    updated_at: time::now()
};

UPSERT audit_event:knowledge_graph_seeded CONTENT {
    event_type: "knowledge_graph_seeded",
    stage: "system",
    actor_ref: "human:maintainer",
    actor_type: "human",
    target_ref: "artifact_ref:knowledge_graph_seed",
    parent_event_ref: NONE,
    request_id: NONE,
    trace_id: NONE,
    payload: {
        summary: "Seeded the Agent-Graph semantic knowledge graph.",
        nodes: 4,
        edges: 5
    },
    policy_context: {
        source: "surreal/AGENT.md",
        owner: "Agent-Graph"
    },
    world_location: { scope: "repository", repository: "Agent-Graph" },
    event_time: time::now(),
    created_at: time::now()
};

DELETE entity_kind WHERE in = entity:agent_graph_platform AND out = schema_term:class_schema_organization;
RELATE entity:agent_graph_platform->entity_kind->schema_term:class_schema_organization CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE entity_kind WHERE in = entity:surrealdb_runtime AND out = schema_term:class_schema_softwareapplication;
RELATE entity:surrealdb_runtime->entity_kind->schema_term:class_schema_softwareapplication CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE entity_kind WHERE in = entity:schema_org_vocabulary AND out = schema_term:class_schema_creativework;
RELATE entity:schema_org_vocabulary->entity_kind->schema_term:class_schema_creativework CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE knowledge_about WHERE in = memory_object:repo_knowledge_graph AND out = entity:agent_graph_platform;
RELATE memory_object:repo_knowledge_graph->knowledge_about->entity:agent_graph_platform CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE knowledge_about WHERE in = memory_object:repo_knowledge_graph AND out = entity:surrealdb_runtime;
RELATE memory_object:repo_knowledge_graph->knowledge_about->entity:surrealdb_runtime CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE knowledge_about WHERE in = memory_object:repo_knowledge_graph AND out = entity:schema_org_vocabulary;
RELATE memory_object:repo_knowledge_graph->knowledge_about->entity:schema_org_vocabulary CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE instruction_applies_to WHERE in = instruction_doc:surreal_runtime_guide AND out = human:maintainer;
RELATE instruction_doc:surreal_runtime_guide->instruction_applies_to->human:maintainer CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE instruction_applies_to WHERE in = instruction_doc:surreal_runtime_guide AND out = memory_object:repo_knowledge_graph;
RELATE instruction_doc:surreal_runtime_guide->instruction_applies_to->memory_object:repo_knowledge_graph CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE instruction_applies_to WHERE in = instruction_doc:surreal_runtime_guide AND out = entity:surrealdb_runtime;
RELATE instruction_doc:surreal_runtime_guide->instruction_applies_to->entity:surrealdb_runtime CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE policy_applies_to WHERE in = policy_doc:graph_governance AND out = human:maintainer;
RELATE policy_doc:graph_governance->policy_applies_to->human:maintainer CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE policy_applies_to WHERE in = policy_doc:graph_governance AND out = memory_object:repo_knowledge_graph;
RELATE policy_doc:graph_governance->policy_applies_to->memory_object:repo_knowledge_graph CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE policy_applies_to WHERE in = policy_doc:graph_governance AND out = entity:surrealdb_runtime;
RELATE policy_doc:graph_governance->policy_applies_to->entity:surrealdb_runtime CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE policy_applies_to WHERE in = policy_doc:graph_governance AND out = artifact_ref:knowledge_graph_seed;
RELATE policy_doc:graph_governance->policy_applies_to->artifact_ref:knowledge_graph_seed CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE generated_from WHERE in = artifact_ref:knowledge_graph_seed AND out = instruction_doc:surreal_runtime_guide;
RELATE artifact_ref:knowledge_graph_seed->generated_from->instruction_doc:surreal_runtime_guide CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE generated_from WHERE in = artifact_ref:knowledge_graph_seed AND out = policy_doc:graph_governance;
RELATE artifact_ref:knowledge_graph_seed->generated_from->policy_doc:graph_governance CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE generated_from WHERE in = artifact_ref:knowledge_graph_seed AND out = memory_object:repo_knowledge_graph;
RELATE artifact_ref:knowledge_graph_seed->generated_from->memory_object:repo_knowledge_graph CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE generated_from WHERE in = artifact_ref:knowledge_graph_seed AND out = entity:schema_org_vocabulary;
RELATE artifact_ref:knowledge_graph_seed->generated_from->entity:schema_org_vocabulary CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE acted_on WHERE in = audit_event:knowledge_graph_seeded AND out = artifact_ref:knowledge_graph_seed;
RELATE audit_event:knowledge_graph_seeded->acted_on->artifact_ref:knowledge_graph_seed CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};

DELETE acted_on WHERE in = audit_event:knowledge_graph_seeded AND out = memory_object:repo_knowledge_graph;
RELATE audit_event:knowledge_graph_seeded->acted_on->memory_object:repo_knowledge_graph CONTENT {
    source: "knowledge-graph",
    created_at: time::now()
};
