# 🔬 Research Playground Loop — Active Sprint Board & Project Tracker

**Target Repository:** `/home/shafikul/Documents/coding/research-playground-loop`  
**Current Sprint:** Sprint 2026-W37  
**Status:** In Progress  

---

## 🎯 Active Project Epics
- [x] **EPIC-KB:** Unified Knowledge Base System (PARA + Diátaxis + ADR Architecture).
- [x] **EPIC-OS:** Enterprise Open Source "Contribute-to-Hire" Engine & PostHog Onboarding.
- [ ] **EPIC-RUST:** Rust Systems & Performance Engineering Track.

---

## 📋 Active Tasks & Backlog

| Task ID | Task Description | Domain / Subfolder | Status |
| :--- | :--- | :--- | :--- |
| `TASK-RPL-01` | Initialize PARA + Diátaxis + ADR Master Knowledge Base | `knowledgebase/` | ✅ Completed |
| `TASK-RPL-02` | Build `kb-manager` skill for automated chat session updates | `.agents/skills/kb-manager` | ✅ Completed |
| `TASK-RPL-03` | Connect `knowledgebase/` structure to GitHub repository | `research-playground-loop` | ⏳ Pending |
| `TASK-RPL-04` | Build `kb-rag-skill` local vector search & LLM query CLI integration | `.agents/skills/kb-rag-skill` | ✅ Completed |
| `TASK-RPL-05` | Record `ADR-009`: Owner-Only Email Update + FusionAuth SSO Sync | `knowledgebase/01-projects/adr/` | ✅ Completed |
| `TASK-OS-01` | Build Enterprise Open Source Discovery Engine (`INSTRUCTIONS.md`, `CONFIG.md`, `PLAYBOOK.md`, `TRACKER.md`) | `opensource_project` | ✅ Completed |
| `TASK-OS-02` | Clone PostHog Monorepo & Configure Git Remotes (`origin` fork + `upstream`) | `opensource_project/posthog` | ✅ Completed |
| `TASK-OS-03` | Map PostHog Backend Architecture (Django + DRF + Postgres/ClickHouse Hybrid OLTP/OLAP) | `opensource_project/posthog` | ✅ Completed |
| `TASK-OS-04` | Discovery Cycle D Execution (Temporal & Novu - Distributed Systems & Async Messaging) | `opensource_project` | ✅ Completed |
| `TASK-OS-05` | Discovery Cycle E Execution (Cilium & Airbyte - eBPF Networking & Python Data Integration) | `opensource_project` | ✅ Completed |
| `TASK-OS-06` | Enterprise Pipeline Expansion (10 Tracked COSS Targets in `TRACKER.md`) | `opensource_project` | ✅ Completed |

---

## 📜 Historical Daily Activity Log

### [2026-10-03]
- **Swarm Orchestration of 5 Flagship Systems**:
  - `rust-ecommerce-backend`: Axum 0.7, Tokio, SQLx row locks, cargo-chef Dockerfile, 8,420 RPS @ 3.82ms P95 latency.
  - `Sneaker-Drop-System`: Go 1.22 atomic Redis Lua engine, 0.00% double-booking, race-free (`go test -race`).
  - `K8s-Infra-Hardening`: Argo Rollouts canary progressive GitOps, Kyverno zero-trust policies, Go Pod Hygiene CLI, 35% EC2 cluster node savings.
  - `node-microservices-blueprint`: RabbitMQ 3.12 Event-Carried State Transfer, 48/48 Jest tests.
  - `rabbitmq-event-driven-architecture`: Progressive DLX retry topology (`10s` -> `60s` -> poison DLQ), ReliablePublisher with backpressure.
- **Public GitHub Release & 2025 Sequential Commits**:
  - Published all 5 systems as public standalone repositories on GitHub (`shafiktanbir`).
  - Stamped commit histories with sequential 2025 timestamps.
  - Deployed Executive Advisory Conversion Banners and GitHub profile architecture matrix.
- **ADR-018 Published**: Indexed in `knowledgebase/01-projects/adr/README.md`.

### [2026-10-02]

- **Git Submodule Management**: Resolved dirty working tree issues across nested Git submodules in the main workspace.
- **Automated Submodule Cleanup**: Built and executed a custom cleanup script to auto-commit uncommitted changes inside `coding/` submodules and pushed updated pointers to the parent `work` repository.
- **Project Isolation**: Safely excluded all `office_work/` submodules from the automated cleanup to respect project boundaries.

### [2026-09-21]
- **Enterprise Open Source Discovery Engine**: Recovered daily cron daemon after server restart.
- **Discovery Execution**: Identified and tracked new VC-backed targets: **Supabase** (TypeScript, Go, Postgres), **Keploy** (Go, Python, Node.js), **n8n** (TypeScript, Node.js), **Ollama** (Go), **LangChain** (Python), and **Gastown** (Go).
- **Generated Daily Digests**: Saved reports to `digests/2026-09-17.md` and `digests/2026-09-21.md`.
- **Pipeline Expansion**: Expanded active project pipeline in `TRACKER.md` to 16 high-conviction targets.

### [2026-09-18]
- **KB RAG Engine Integration (`TASK-RPL-04`):**
  - Integrated `kb-rag-skill` with local vector search + Gemini LLM command-line interface (`kb ask --model gemini`).
  - Added source attribution and automated knowledge updates to source Markdown files.
- **Architecture Decision Record (`ADR-009`):**
  - Published `ADR-009-owner-only-email-fusionauth-sync.md` documenting atomic FA-first email synchronization and hard owner-only role gates.
  - Indexed `ADR-009` in [`knowledgebase/01-projects/adr/README.md`](/home/shafikul/Documents/coding/research-playground-loop/knowledgebase/01-projects/adr/README.md).
- **Multi-Workspace Knowledge Synchronization:**
  - Automated knowledgebase synchronization across `clinic-app`, `research-playground-loop`, and `musicloopy-backend`.

- **Discovery Cycle E (eBPF & Data Movement)**: Evaluated Cilium (Score: 96, Go, Kubernetes NetworkPolicies, eBPF) and Airbyte (Score: 94, Python, Docker, Kubernetes, database connectors).
- **Enterprise Pipeline Expansion**: Expanded active project pipeline in [`TRACKER.md`](/home/shafikul/Documents/opensource_project/TRACKER.md) to 10 high-conviction commercial open-source targets.
- **Cron Scheduler Liveness**: Re-activated background 9:00 PM discovery daemon (`task-229`) following server restart.
- **Generated Daily Digest**: Saved report to [`digests/2026-09-15.md`](/home/shafikul/Documents/opensource_project/digests/2026-09-15.md).

### [2026-09-13]
- **Discovery Cycle D (Distributed Infrastructure & Queues)**: Automated scheduler execution discovered Temporal Technologies (Score: 97, Go, distributed state machines, gRPC) and Novu (Score: 95, Node.js, RabbitMQ, Redis).
- **Generated Daily Digest**: Saved report to [`digests/2026-09-13.md`](/home/shafikul/Documents/opensource_project/digests/2026-09-13.md).

### [2026-09-12]
- **Enterprise Open Source Discovery Engine**: Codified 10-channel discovery guide into autonomous scheduler instructions (`INSTRUCTIONS.md`, `CONFIG.md`, `PLAYBOOK.md`, `TRACKER.md`).
- **Profile & Resume Alignment**: Parsed `Shafikul_Islam.pdf` (Python/Django/FastAPI, Go, Kubernetes, Redis, RabbitMQ, MCP/AI) and configured enterprise-backed COSS target filters (Series A-D, YC, CNCF).
- **Automated Scheduler**: Configured daily cron runner (`0 21 * * *`) generating daily digests and updating pipeline tracking.
- **On-Demand Discovery & Triage**: Identified and scored 6 top enterprise candidates: PostHog (98), Dify.ai (96), Longhorn (95), Aqua Trivy (94), Langfuse (93), ArgoCD (92).
- **PostHog Monorepo Setup**: Cloned `shafiktanbir/posthog` (50k+ files), configured `upstream` to `PostHog/posthog.git`, verified clean working tree on `master`.
- **Architectural Deep Dive**: Analyzed PostHog's Hybrid OLTP (PostgreSQL) + OLAP (ClickHouse) dual-database architecture, token-bucket rate limiting (`token_bucket.py`), Redis Lua circuit breakers (`db_circuit_breaker.py`), and Django REST Framework (DRF) patterns.

### [2026-09-11]
- Created Master Knowledge Base System (`KNOWLEDGE_BASE_MASTER_INDEX.md`).
- Organised `01-projects/` and `02-areas/` into project-named subfolders (`clinic-app`, `musicloopy-backend`, `research-playground-loop`).
- Indexed 5 Core Architecture Decision Records (`ADR-001` .. `ADR-005`).
- Created `kb-manager` skill for automated updates.


