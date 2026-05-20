# Agent-Graph Ontology

Agent-Graph owns the AGenNext ontology.

Ontology defines the semantic model of the platform: the entity types, relationships, ownership boundaries, and meaning of records used across AGenNext.

This file is the public contributor reference. Contributors should read this before adding tools, skills, blueprints, grammar rules, seed data, reviews, or registry records.

## Why this exists

Without a shared ontology, contributors cannot know:

```text
- where a concept belongs
- which repo owns a record
- whether something is taxonomy, ontology, grammar, seed data, or registry data
- how objects relate to each other
- how to name and validate new records
```

The ontology makes contribution safe and consistent.

## Ontology vs taxonomy vs grammar

```text
Ontology
  = entities + relationships + meaning
  = owned by Agent-Graph

Taxonomy
  = accepted controlled terms/classes
  = owned by Agent-Vocabulary

Grammar
  = validation rules and acceptance constraints
  = owned by Agent-Grammar

Registry / artifact repositories
  = actual records and source objects
```

## Core entities

```text
Artifact
Tool
Capability
Skill
Blueprint
Agent
AgentTeam
Workflow
Protocol
RuntimeProfile
Role
ProviderOffer
Author
Publisher
ReviewRecord
SeedRecord
VocabularyTerm
GrammarRule
GraphContext
```

## Core relationships

```text
Artifact has representation
Artifact has lifecycle status
Artifact is validated by GrammarRule
Artifact is reviewed by ReviewRecord
Artifact uses VocabularyTerm

Tool implements Capability
Tool has Author
Tool has Publisher
Tool has ProviderOffer
Tool has registry version
Tool may reference upstream version
Tool may have sameAs links
Tool may have aliases

Skill requires Tool
Skill implements operational capability
Skill can be used by Agent
Skill can be used by Workflow

Blueprint describes Agent
Blueprint describes AgentTeam
Blueprint describes Workflow
Blueprint describes Protocol
Blueprint describes Capability
Blueprint describes RuntimeProfile
Blueprint describes Role

Agent executes Skill
Agent uses Tool
Agent belongs to AgentTeam
AgentTeam coordinates Agent
Workflow orchestrates Agent or AgentTeam

ProviderOffer exposes Tool
ProviderOffer has provider type
ProviderOffer has provider canonical identity

ReviewRecord reviews Artifact
ReviewRecord gates publication
```

## Ownership boundaries

```text
Agent-Graph
  owns ontology and graph context

Agent-Vocabulary
  owns taxonomy terms

Agent-Grammar
  owns validation grammar

Agent-Seed
  owns canonical seed data

Tool-Registry
  owns tool records

Agent-Blueprint
  owns blueprint records

Agent-Skills
  owns skill records

Agent-Review
  owns review records
```

## Contribution rules

### Adding a new taxonomy term

Add it to:

```text
Agent-Vocabulary
```

Examples:

```text
tool_type
provider_type
consumer_type
artifact_type
blueprint_entity_type
```

Do not add taxonomy terms directly inside registry records unless they already exist or are being proposed.

### Adding a new tool

Add the tool record to:

```text
Tool-Registry
```

A tool record must include:

```text
canonical_id
did
registry_version
capabilities
author
publisher
provider_offers
sameAs / aliases when applicable
```

Provider identity stays as provider metadata on the tool record. Provider type must reference Agent-Vocabulary taxonomy.

### Adding a new skill

Add the skill record/source to:

```text
Agent-Skills
```

Skills may require tools, but they do not define tool identity.

### Adding a new blueprint

Add the blueprint record/source to:

```text
Agent-Blueprint
```

Blueprint names must make the objective and entity type explicit.

### Adding validation rules

Add rules to:

```text
Agent-Grammar
```

Grammar validates records against Agent-Graph ontology and Agent-Vocabulary taxonomy.

### Adding seed data

Add seed data to:

```text
Agent-Seed
```

Seed data must be idempotent and loadable into SurrealDB.

## Important rules

```text
Provider identity is not taxonomy.
Provider type is taxonomy.

Tool identity belongs in Tool-Registry.
Tool type belongs in Agent-Vocabulary.

Blueprint identity belongs in Agent-Blueprint.
Blueprint entity type belongs in Agent-Vocabulary.

Ontology relationships belong in Agent-Graph.
Validation rules belong in Agent-Grammar.
Seed data belongs in Agent-Seed.
```

## Contributor decision guide

```text
Is it an accepted class/list of terms?
  → Agent-Vocabulary

Is it an entity relationship or meaning rule?
  → Agent-Graph

Is it a validation rule?
  → Agent-Grammar

Is it initial platform data?
  → Agent-Seed

Is it a tool identity?
  → Tool-Registry

Is it a skill?
  → Agent-Skills

Is it a blueprint?
  → Agent-Blueprint

Is it a review decision/gate?
  → Agent-Review
```
