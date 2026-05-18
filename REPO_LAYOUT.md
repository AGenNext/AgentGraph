# Agent-Graph Repository Boundaries

This repository is the backend graph source of truth in the AGenNext stack.

## Ownership Matrix

| Repo | Primary Responsibility |
|------|------------------------|
| `Agent-Graph` | Backend graph source of truth, SurrealDB schema, backend APIs, SDK, and validation |
| `Agent-Runtime` | SurrealDB-only agent execution and enforcement runtime, tool use, and service wiring |
| `Agent-Identity` | WaltID wallet, issuer, verifier, and credential lifecycle |
| `Agent-Auth` | Authentication, sessions, permissions, and policy enforcement |
| `Agent-Protocols` | Protocol definitions, interoperability contracts, and policy interfaces |
| `Agent-LCM` | Lifecycle management, release orchestration, rollout, and deprecation policy |
| `Agent-Security` | Security controls, hardening, threat management, and remediation workflows |
| `Agent-Eval` | Evaluation suites, benchmarking, scoring, and acceptance criteria |
| `Agent-Flow` | Workflow definitions, orchestration graphs, routing, and step sequencing |
| `Agent-Orchestration` | Orchestration policies, execution control, and cross-service job coordination |
| `Agent-Memory` | Persistence, recall, long-term state, and retention policy |
| `Agent-Vision` | Multimodal perception, image/video understanding, and extraction pipelines |
| `Agent-Chat` | Conversational UI, chat session management, and message presentation |
| `Agent-Wallet` | Wallet UI/runtime and credential presentation UX |
| `Agent-Trust` | Trust, verification, attestation, and trust policy |
| `Agent-Registry` | All current services, versions, discovery, registration, signing, and service metadata |
| `Agent-Card` | Canonical agent cards, identity, capabilities, access, trust, and operational state |
| `Tool-Catalog` | All current tools, tool metadata, and tool discovery |
| `Prompt-Library` | All current prompts, prompt templates, and prompt governance |
| `Agent-Image` | Image generation, image pipelines, and image asset workflows |
| `Agent-Context` | Context management, context assembly, and runtime context policies |
| `Agent-Environment` | Environment configuration, deployment env, and runtime settings |
| `Agent-Builder` | Composition, scaffolding, and build-time generation |
| `Agent-RAG` | Retrieval, grounding, indexing, and RAG orchestration |
| `model-registry` | All current models, metadata, selection, and policy |
| `Agent-Bench` | Performance evaluation, benchmarking, and load/latency testing |
| `AAGFE` | Agent governance, governance policy, and oversight |
| `Agent-UI-Kit` | Shared UI primitives, components, and design system assets |
| `Agent-Harness` | Test harnesses, fixture orchestration, and environment drivers |
| `Model-Router` | Model routing, policy enforcement, and request selection |
| `Agent-FinOps` | Cost management, usage analytics, and spend operations |
| `Agent-Skills` | All current skills, skill lifecycle, and skill metadata |
| `Agent-Secrets` | Secret storage, rotation, and secret access policies |
| `Agent-Drive` | File storage, document drive, and content management |
| `Agent-Commerce` | Commerce, orders, billing, and transaction workflows |
| `Agent-Pay` | Payments, payment processing, and settlement workflows |
| `Agent-Connect` | A2A connectivity, agent transport, and agent messaging |
| `Agent-Channel` | Human interface layers, channel integrations, and user-facing agent surfaces |
| `Agent-Cloud` | Cloud deployment, cloud platform integration, and hosted infrastructure |
| `Agent-Teams` | Multi-agent teams, shared workspaces, and group workflows |
| `Agent-Frameworks` | All current frameworks, framework integrations, and support metadata |

## Repository Split

- `Agent-Graph`:
  - SurrealDB schema and graph assets
  - backend API contract
  - Python SDK package
  - validation harnesses
  - backend documentation

- `Agent-Runtime`:
  - SurrealDB-only executable runtime and enforcement code
  - agent execution, tool use, and service wiring
  - runtime integrations

- `Agent-Identity`:
  - WaltID wallet, issuer, and verifier
  - credential issuance and presentation flows
  - identity lifecycle handling

- `Agent-Auth`:
  - authentication, sessions, permissions, and policy enforcement
  - access-control and token handling

- `Agent-Protocols`:
  - protocol definitions and interoperability contracts
  - message, event, and handoff standards
  - policy interfaces and policy contract schemas
  - cross-service exchange schemas

- `Agent-LCM`:
  - lifecycle management and release orchestration
  - versioning, rollout, and deprecation policy
  - environment and deployment coordination

- `Agent-Security`:
  - security controls, hardening, and threat management
  - vulnerability policy and remediation workflows
  - security posture validation and reporting

- `Agent-Eval`:
  - evaluation suites and benchmarking
  - test harnesses for quality, regressions, and comparisons
  - scoring, grading, and acceptance criteria

- `Agent-Flow`:
  - workflow definitions and orchestration graphs
  - routing, transitions, and step sequencing
  - stateful flow composition and handoffs

- `Agent-Orchestration`:
  - orchestration policies and execution control
  - event coordination and workflow scheduling
  - cross-service job coordination

- `Agent-Memory`:
  - persistence and recall services
  - long-term state and memory lifecycle
  - memory indexing, retrieval, and retention policy

- `Agent-Vision`:
  - multimodal perception and vision pipelines
  - image/video understanding and extraction
  - vision-specific preprocessing and postprocessing

- `Agent-Chat`:
  - conversational UI and chat session management
  - chat transport, history, and presentation
  - user-facing messaging surfaces

- `Agent-Wallet`:
  - wallet UI and wallet runtime
  - credential storage and presentation UX
  - user-facing wallet flows

- `Agent-Trust`:
  - trust signals and trust policy
  - verification and attestation workflows
  - trust scoring, assertions, and audit-backed trust state

- `Agent-Registry`:
  - all current services and discovery
  - versioning and cryptographic signing
  - registration and service metadata
  - trusted artifact publication and registry policy

- `Agent-Card`:
  - canonical agent cards
  - identity, capabilities, and access metadata
  - trust and operational state for an agent

- `Tool-Catalog`:
  - all current tools and tool metadata
  - tool discovery and listing
  - tool categorization and normalization

- `Prompt-Library`:
  - all current prompts and templates
  - prompt governance and versioning
  - reusable prompt patterns and curation

- `Agent-Image`:
  - image generation workflows
  - image pipeline orchestration
  - image asset handling and transforms

- `Agent-Context`:
  - context management and assembly
  - runtime context policies and packing
  - conversation and prompt context lifecycle

- `Agent-Environment`:
  - environment configuration and runtime settings
  - deployment environment variables and profiles
  - environment policy, bootstrap data, and service endpoint configuration
  - hosted service wiring via environment variables

- `Agent-Builder`:
  - composition and scaffolding
  - build-time generation and assembly
  - project templates and creator workflows

- `Agent-RAG`:
  - retrieval and grounding
  - indexing and vector retrieval workflows
  - RAG orchestration and source selection

- `model-registry`:
  - all current models and metadata
  - model selection and availability policy
  - provider normalization and lookup

- `Agent-Bench`:
  - performance evaluation and benchmarking
  - load, latency, and throughput testing
  - benchmark reporting and regression tracking

- `AAGFE`:
  - agent governance and oversight
  - governance policy and compliance workflows
  - approvals, review, and escalation rules

- `Model-Router`:
  - model routing and request selection
  - policy enforcement for model choice
  - fallback, failover, and routing decisions

- `Agent-FinOps`:
  - cost management and spend tracking
  - usage analytics and chargeback
  - budget policy and optimization workflows

- `Agent-Skills`:
  - all current skills and lifecycle
  - skill metadata and normalization
  - skill publishing and discovery

- `Agent-Secrets`:
  - secret storage and rotation
  - secret access policies and controls
  - secret lifecycle and audit

- `Agent-Drive`:
  - file storage and document drive
  - content management and retrieval
  - drive metadata and document lifecycle

- `Agent-Commerce`:
  - commerce and transaction workflows
  - orders, billing, and checkout
  - commerce metadata and fulfillment state

- `Agent-Pay`:
  - payments and payment processing
  - settlement workflows and payment state
  - payment metadata and reconciliation

- `Agent-Connect`:
  - A2A connectivity and transport
  - agent messaging and message routing
  - agent handoff and peer-to-peer links

- `Agent-Channel`:
  - human interface layers and channel integrations
  - user-facing agent surfaces and channel adapters
  - human-agent interaction routing

- `Agent-Cloud`:
  - cloud deployment and cloud platform integration
  - hosted infrastructure and platform operations
  - cloud environment provisioning and runtime support

- `Agent-Teams`:
  - multi-agent teams and team collaboration
  - group workflows and shared state
  - team membership and coordination

- `Agent-Frameworks`:
  - all current frameworks and integrations
  - support metadata and compatibility data
  - framework-specific adapters and normalization

## Legacy Namespace Migration Targets

These namespaces still exist in this repo, but they are not part of the intended long-term Agent-Graph package boundary:

- `core/` -> runtime/service logic to be moved into runtime-oriented repos
- `a2a/` -> protocol and message contracts to be moved into protocol/connectivity repos
- `agents/` -> agent implementations and adapters to be moved into the runtime repo
- `agentnext/` -> compatibility and app glue to be moved out of Agent-Graph

Treat these as migration targets, not as new surfaces to extend inside the schema package.

## Architecture Note

The platform is intentionally split into three layers:

- `Agent-Graph` defines the shared schema, contracts, and compatibility rules.
- `Agent-Runtime` executes and enforces behavior against the SurrealDB-backed platform.
- `Agent-Environment` configures hosted services, endpoints, and deployment wiring through environment variables.

This separation keeps the system modular and avoids hardcoding identity, LLM, storage, or similar hosted integrations into runtime code.

The base schema is core IP. Child repos and external vendors may extend it for their own use cases, but those extensions should remain Agent-Graph-compatible and only be absorbed into the core when they fit the platform's own repo and IP strategy.

- `Agent-UI-Kit`:
  - shared UI primitives and components
  - design system assets and patterns
  - reusable client-side building blocks

- `Agent-Harness`:
  - test harnesses and fixture orchestration
  - environment drivers and simulation layers
  - repeatable setup for validation runs

## What Belongs Here

Keep code in this repo when it defines or validates:

- graph schema
- SurrealDB `RELATE` edges and record links
- multi-step `route` / `path` materialization
- backend API behavior
- SDK packaging and client surface
- graph docs and validation docs

## What Does Not Belong Here

Do not place these concerns in `Agent-Graph`:

- wallet implementation details
- issuer/verifier runtime code
- authentication/session middleware that belongs to `Agent-Auth`
- runtime execution logic that belongs to `Agent-Runtime`
- protocol specifications that belong to `Agent-Protocols`
- policy contract interfaces that belong to `Agent-Protocols`
- lifecycle management concerns that belong to `Agent-LCM`
- security controls that belong to `Agent-Security`
- evaluation and benchmarking code that belongs to `Agent-Eval`
- workflow and orchestration definitions that belong to `Agent-Flow`
- orchestration control that belongs to `Agent-Orchestration`
- persistence and recall code that belongs to `Agent-Memory`
- multimodal vision code that belongs to `Agent-Vision`
- conversational UI code that belongs to `Agent-Chat`
- wallet UI/runtime code that belongs to `Agent-Wallet`
- trust and attestation code that belongs to `Agent-Trust`
- discovery and catalog code that belongs to `Agent-Registry`
- tool inventory and discovery code that belongs to `Tool-Catalog`
- prompt asset code that belongs to `Prompt-Library`
- image generation code that belongs to `Agent-Image`
- context management code that belongs to `Agent-Context`
- environment configuration code that belongs to `Agent-Environment`
- scaffolding and build-time generation code that belongs to `Agent-Builder`
- retrieval and grounding code that belongs to `Agent-RAG`
- model catalog and selection code that belongs to `model-registry`
- performance evaluation code that belongs to `Agent-Bench`
- governance policy and oversight code that belongs to `AAGFE`
- model routing code that belongs to `Model-Router`
- cost management code that belongs to `Agent-FinOps`
- skill catalog code that belongs to `Agent-Skills`
- secret management code that belongs to `Agent-Secrets`
- drive and content storage code that belongs to `Agent-Drive`
- commerce code that belongs to `Agent-Commerce`
- payment processing code that belongs to `Agent-Pay`
- A2A connectivity code that belongs to `Agent-Connect`
- human interface and channel code that belongs to `Agent-Channel`
- cloud deployment and platform code that belongs to `Agent-Cloud`
- team collaboration code that belongs to `Agent-Teams`
- framework integration code that belongs to `Agent-Frameworks`
- shared UI component code that belongs to `Agent-UI-Kit`
- harness and fixture orchestration code that belongs to `Agent-Harness`
- end-user UI application code unless it is explicitly part of the backend surface

## Boundary Rule

If a change affects graph structure, API shape, SDK contracts, or graph validation, it belongs here.

Agents own credential references, credential state mappings, and backend-side credential graph links.

If a change affects identity, authorization, runtime orchestration, or protocol governance, it belongs in the corresponding service repo.

Each repo may extend the shared base schema for its own domain, and Agent-Graph will accommodate those extensions while keeping every schema Agent-Graph-compatible.

Hosted services such as WaltID, external LLMs, cloud storage, and similar integrations should be configured through `Agent-Environment` and environment variables rather than hardcoded into `Agent-Runtime`.

## Repo Map

| Repo | Inputs | Outputs | Dependencies |
|------|--------|---------|--------------|
| `Agent-Graph` | Graph schema, API requests, validation runs | SurrealDB assets, backend API responses, Python SDK | SurrealDB, FastAPI, Pydantic |
| `Agent-Runtime` | Orchestration events, tool calls, execution requests | Agent execution, runtime state, job results | `Agent-Graph`, `Agent-Protocols`, `Agent-Environment`, `Agent-Memory` |
| `Agent-Identity` | Credential issuance and verification requests | Wallet flows, VCs, identity assertions | WaltID, `Agent-Auth`, `Agent-Protocols` |
| `Agent-Auth` | Login, session, token, and policy requests | Auth decisions, sessions, tokens, access policy | `Agent-Identity`, `Agent-Security`, `Agent-Protocols` |
| `Agent-Protocols` | Service requirements, policy needs, exchange constraints | Protocol specs, message schemas, policy contracts | `AAGFE` |
| `Agent-LCM` | Release metadata, version inputs, rollout triggers | Release plans, rollout policy, deprecation notices | `Agent-Graph`, `Agent-Builder`, `Agent-Registry` |
| `Agent-Security` | Findings, hardening requirements, threat reports | Security controls, remediation workflows, posture reports | `Agent-Auth`, `AAGFE`, `Agent-Protocols` |
| `Agent-Eval` | Test suites, benchmarks, target behavior | Evaluation scores, regression reports, acceptance signals | `Agent-Graph`, `Agent-Runtime`, `Agent-Bench` |
| `Agent-Flow` | Workflow definitions, transitions, step inputs | Orchestration graphs, step sequencing, flow state | `Agent-Orchestration`, `Agent-Runtime` |
| `Agent-Orchestration` | Scheduling needs, coordination events, jobs | Execution control, cross-service coordination, handoff state | `Agent-Flow`, `Agent-Runtime`, `Agent-Protocols` |
| `Agent-Memory` | Memory writes, retrieval requests, retention policy | Stored memories, recall results, memory indexes | `Agent-Graph`, `Agent-RAG`, `Agent-Context` |
| `Agent-Vision` | Images, video, multimodal payloads | Vision features, extracted signals, vision metadata | `Agent-Runtime`, `Agent-Image`, `Agent-Context` |
| `Agent-Chat` | User messages, chat sessions, conversation state | Chat UI state, conversation views, message history | `Agent-Context`, `Agent-Runtime`, `Agent-Wallet` |
| `Agent-Wallet` | Wallet actions, credential presentation requests | Wallet UI/runtime state, credential presentation UX | `Agent-Identity`, `Agent-Auth`, `Agent-Trust` |
| `Agent-Trust` | Trust signals, attestations, verification inputs | Trust state, attestations, trust policy outputs | `Agent-Identity`, `Agent-Security`, `AAGFE` |
| `Agent-Registry` | Service and repo metadata, registration requests, version inputs, signing inputs | Trusted registry records, signed artifacts, lookup results | `Agent-Protocols`, `Tool-Catalog`, `Agent-Card` |
| `Agent-Card` | Agent identity, capability, access, and trust inputs | Canonical agent cards, operational state views, trust state | `Agent-Registry`, `Agent-Auth`, `Agent-Trust` |
| `Tool-Catalog` | Tool metadata, tool descriptors, capability updates | Tool listings, normalized catalog entries | `Agent-Registry`, `Agent-Runtime` |
| `Prompt-Library` | Prompt drafts, prompt updates, governance inputs | Prompt templates, prompt versions, reusable prompts | `Agent-Context`, `Agent-Graph` |
| `Agent-Image` | Image generation requests, asset inputs | Generated images, image workflows, transforms | `Agent-Runtime`, `Agent-Context`, `Prompt-Library` |
| `Agent-Context` | Prompt context, conversation context, runtime context | Packed context objects, context policies, context state | `Agent-Memory`, `Agent-Graph`, `Prompt-Library` |
| `Agent-Environment` | Environment configuration, deployment profiles, runtime settings | Env bundles, bootstrap settings, runtime config | `Agent-LCM`, `Agent-Builder`, `Agent-Registry` |
| `Agent-Builder` | Project specs, scaffolding inputs, creator workflows | Generated project structure, templates, build-time artifacts | `Agent-Environment`, `Agent-Registry`, `Prompt-Library` |
| `Agent-RAG` | Retrieval queries, source corpora, grounding requests | Retrieved context, ranked sources, RAG traces | `Agent-Graph`, `Agent-Memory`, `Agent-Context` |
| `model-registry` | Model metadata, provider data, selection policy | Model catalogs, availability views, selection outputs | `Agent-Registry`, `Agent-Protocols` |
| `Agent-Bench` | Benchmarks, load targets, latency goals | Performance reports, regression data, benchmark scores | `Agent-Graph`, `Agent-Runtime`, `Agent-Eval` |
| `AAGFE` | Governance inputs, review requests, oversight triggers | Governance policy, approvals, escalation outcomes | `Agent-Protocols`, `Agent-Security`, `Agent-Trust` |
| `Agent-UI-Kit` | Design tokens, shared component specs, layout patterns | Reusable UI primitives, component library assets | `Agent-Chat`, `Agent-Wallet`, `Agent-Builder` |
| `Agent-Harness` | Test fixtures, environment drivers, simulation inputs | Repeatable harness runs, fixture orchestration, setup state | `Agent-Eval`, `Agent-Bench`, `Agent-Environment` |
| `Model-Router` | Model routing requests, policy inputs, model metadata | Routed model choice, failover decisions, routing traces | `model-registry`, `Agent-Protocols`, `Agent-Runtime` |
| `Agent-FinOps` | Cost, usage, and spend inputs | Spend reports, budget views, cost optimization outputs | `Agent-Registry`, `model-registry`, `Agent-Bench` |
| `Agent-Skills` | Skill definitions, skill metadata, publishing inputs | Skill catalog entries, skill lifecycle state, skill discovery | `Tool-Catalog`, `Prompt-Library`, `Agent-Registry` |
| `Agent-Secrets` | Secret material, secret rotation inputs, access policy | Secret vault records, rotation state, audit traces | `Agent-Auth`, `Agent-Environment`, `Agent-Security` |
| `Agent-Drive` | File uploads, document metadata, content inputs | Drive records, file storage state, content listings | `Agent-Memory`, `Agent-Registry`, `Agent-UI-Kit` |
| `Agent-Commerce` | Orders, billing, pricing, and transaction inputs | Commerce records, invoice state, fulfillment outputs | `Agent-Auth`, `Agent-Registry`, `Agent-Protocols` |
| `Agent-Pay` | Payment intents, charges, and settlement inputs | Payment records, settlement state, reconciliation outputs | `Agent-Commerce`, `Agent-Auth`, `Agent-Trust` |
| `Agent-Connect` | A2A transport requests, message inputs, peer metadata | Agent transport routes, handoff state, peer messaging outputs | `Agent-Protocols`, `Agent-Orchestration`, `Agent-Registry` |
| `Agent-Channel` | Human interaction requests, channel events, UI integrations | Channel responses, human-facing agent surfaces, delivery state | `Agent-Chat`, `Agent-Connect`, `Agent-UI-Kit` |
| `Agent-Cloud` | Cloud deployment requests, platform inputs, infra metadata | Cloud runtime state, hosted services, provisioning outputs | `Agent-LCM`, `Agent-Environment`, `Agent-Registry` |
| `Agent-Teams` | Team membership, workspace, and group-workflow inputs | Team workspace state, collaboration outputs, shared coordination | `Agent-Auth`, `Agent-Chat`, `Agent-Registry` |
| `Agent-Frameworks` | Framework metadata, integration requests, compatibility inputs | Framework catalogs, adapter state, compatibility outputs | `Agent-Registry`, `Tool-Catalog`, `Agent-Runtime` |
