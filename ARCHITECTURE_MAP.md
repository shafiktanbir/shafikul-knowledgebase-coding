# ARCHITECTURE_MAP.md — System Architecture & Domain Map

> **Monorepo Architecture, Technology Stacks, and Component Interaction Patterns**

---

## 🏗️ Architecture Overview

`research-playground-loop` is an agentic engineering and learning monorepo designed for high-velocity software development, deep technical learning loops, backend system design, and AI agent orchestration.

```
                           +-------------------------------------+
                           |         Workspace Root              |
                           |   research-playground-loop           |
                           +------------------+------------------+
                                              |
      +-------------------+-------------------+-------------------+-------------------+
      |                   |                   |                   |                   |
+-----+-----+       +-----+-----+       +-----+-----+       +-----+-----+       +-----+-----+
|  Systems  |       |   Backend  |       | Learning  |       | AI Agents |       | Marketing |
| & Rust    |       | Playgrounds|       |  Mentors  |       | & Career  |       | & Web Apps|
+-----------+       +-----------+       +-----------+       +-----------+       +-----------+
| coven     |       | ecom-mv   |       | k8s-labs  |       | discovery |       | market-lab|
| k8s core  |       | uploader  |       | interview |       | career-ops|       | website   |
+-----------+       +-----------+       +-----------+       +-----------+       +-----------+
```

---

## 📐 Technology Layer Breakdown

### Layer 1: Rust Authority & Execution Runtime (`coven`)
- **Core Technology**: Rust (2021 Edition), Cargo Workspaces, Tokio Async, TS npm wrappers.
- **Architectural Pattern**: Authority layer pattern. Core decisions, safety checks, and session governance live strictly in Rust crates; TypeScript packages act solely as thin integration surfaces.
- **Key Constraints**: Zero tolerance for Clippy warnings (`-D warnings`), mandatory secret scanning (`check-secrets.py`), worktree claims registry (`coven claim`).

### Layer 2: Node.js & NestJS Backend Engineering (`backend-playground`)
- **Core Technology**: NestJS, Node.js, Express, Redis, BullMQ, PostgreSQL, Prisma/TypeORM.
- **Architectural Pattern**: Microservices, Event-Driven Processing, Producer-Consumer Queues (e.g. `file-uploader-system`), Multi-Vendor E-Commerce APIs.
- **Key Features**: Asynchronous task queues, chunked file uploads, JWT authentication, stateful workflow management.

### Layer 3: Infrastructure, Networking & Kubernetes Labs
- **Core Technology**: Kubernetes (`kubernetes/`), Linux Cgroups/Namespaces, eBPF, Bash, Docker.
- **Architectural Pattern**: Hands-on lab sandbox for deep kernel/networking diagnostics, container runtimes, CNI plugins, and Kubernetes controller internals.

### Layer 4: Interactive Mentorship & Learning Engines
- **Core Technology**: Markdown-driven state machines, Antigravity Custom Skills, Progress trackers.
- **Sub-Domains**:
  - `interview-prep/`: Mock interviewer engine operating under strict Staff-level evaluation criteria.
  - `freelance mentor/`: Software agency positioning, client acquisition, sales negotiation, value pricing.
  - `product enginer/`: Android product engineer learning curriculum across 10 production-grade apps.

### Layer 5: AI Agents & Automation (`product analysis discovery agent`, `career-ops`)
- **Core Technology**: Python 3.11+, Embeddings/Vector DBs, Web Scraping (Reddit/Play Store APIs), LLM clustering.
- **Architectural Pattern**: Autonomous discovery pipeline: Ingestion -> Preprocessing -> Vector Clustering -> Pain-point Scoring -> App Idea Generation -> Weekly Report.

### Layer 6: Enterprise Open-Source & Modern Analytics Architecture (`PostHog`)
- **Core Technology**: Rust (`rust/capture`, `personhog`), Apache Kafka, ClickHouse OLAP, HogQL Engine, Python 3.11+ / Django 4.x, PostgreSQL, Redis, React / TypeScript / Kea.
- **Architectural Pattern**: Distributed Event-Driven Hybrid OLTP/OLAP & Modular Vertical Slice Monorepo.
- **Key Sub-Systems**:
  - **Edge Ingestion**: Zero-copy Rust capture proxy streaming events to partitioned Kafka topics.
  - **Distributed Identity**: `personhog` Rust cluster managing distinct IDs, person merges, and Raft/lease coordination.
  - **HogQL & Columnar OLAP**: AST-compiled sandboxed queries executed over ClickHouse shards with sub-millisecond Hypercache.
  - **Modular Products**: 89+ isolated vertical slices in `products/` guarded by `tach` import boundaries and frozen dataclass facade contracts.
  - **Agentic AI & MCP**: Unified Go/Python AI Gateway (`PostHog/ai-gateway`), native Model Context Protocol (MCP) server, and automated evaluation harnesses.
- **Documentation**: [`knowledgebase/01-projects/posthog/architecture.md`](01-projects/posthog/architecture.md)

---

## 🔒 Security & Operational Safety Standards

1. **Secrets & Privacy**: Secrets, private credentials, and personal tokens are strictly prohibited in code and docs. Automated checks (`check-secrets.py`, `check-coven-privacy.py`) run before commits.
2. **Reversibility**: All destructive bash commands (e.g. `rm -rf`, `docker system prune`, `git reset --hard`) require explicit confirmation according to `user_global` rules.
3. **Clean Boundaries**: Domain logic must remain encapsulated within its target project folder without leakage into unrelated directories.
