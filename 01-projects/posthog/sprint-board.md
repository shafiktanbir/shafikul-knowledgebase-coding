# PostHog — Contribution Sprint Board & Target Backlog

> **Host Workspace Path:** `/home/shafikul/Documents/opensource_project/posthog/`  
> **Tracker Dashboard:** [`/home/shafikul/Documents/opensource_project/TRACKER.md`](file:///home/shafikul/Documents/opensource_project/TRACKER.md)  
> **Pipeline Stage:** `Evaluating` ➔ `First PR in Progress`  
> **Target Conviction Score:** 98 / 100  

---

## 🎯 Active Sprint Objectives (Contribute-to-Hire)

1. **Verify Local Development Environment:**
   - [x] Monorepo cloned and verified at `/home/shafikul/Documents/opensource_project/posthog`
   - [ ] Run `bin/hogli doctor` / verify local Python (uv), Node.js (pnpm), and Rust toolchains
   - [ ] Stand up local services via `docker-compose.dev.yml` (ClickHouse, Kafka, PostgreSQL, Redis, SeaweedFS)
   - [ ] Run test suite smoke test (`hogli test posthog/api/test/test_team.py`)

2. **Starter PR Candidates (Target: 48-72 Hour Merge):**
   - [ ] **Area A (Ingestion / Capture):** Error handling / retry telemetry on Kafka batch flush edge cases in `rust/capture`.
   - [ ] **Area B (MCP Tools / AI Observability):** Improve schema descriptions or error sanitization in `products/ai_observability/mcp/tools.yaml`.
   - [ ] **Area C (HogQL Query Runners):** Add parameter validation or optimize subquery formatting in `posthog/hogql_queries/`.
   - [ ] **Area D (Developer Experience / Documentation):** Address edge cases in `hogli` CLI or doc typos in `docs/published/`.

3. **Core Architectural PR Targets (High-Impact Credibility):**
   - [ ] Ingestion consumer backoff optimization under ClickHouse write backpressure.
   - [ ] New MCP tool integration or UI component for real-time trace inspection.
   - [ ] HogQL query runner benchmark & cache hit-rate telemetry integration.

---

## 📊 Sprint Task Matrix

| Task / Milestone | Category | Target File / Area | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Knowledge Architecture Ingestion** | Documentation | `knowledgebase/01-projects/posthog/` | Antigravity | **Completed** |
| **Local Docker & Stack Verification** | Infrastructure | `docker-compose.dev.yml`, `hogli` | Shafikul | **In Progress** |
| **Select Starter Issue on GitHub** | Open Source | [`PostHog/posthog` Issues](https://github.com/PostHog/posthog/issues) | Shafikul | **Ready** |
| **Join Discord Contributor Community** | Community | [`discord.gg/posthog`](https://discord.gg/posthog) / [Questions Forum](https://posthog.com/questions) | Shafikul | **Ready** |
| **Draft First Pull Request** | Engineering | `rust/` or `products/*/backend` | Shafikul | **Backlog** |
| **Maintainer Outreach** | Career Ops | Direct LinkedIn / Slack message | Shafikul | **Backlog** |

---

## 📜 Historical Daily Activity Log

### 2026-09-15
- Ingested PostHog monorepo into the canonical Master Knowledge Base at `knowledgebase/01-projects/posthog/`.
- Authored comprehensive architectural deep dive (`architecture.md`) covering Rust edge capture, Kafka topologies, ClickHouse/HogQL query engine, PersonHog distributed identity cluster, PostgreSQL OLTP multi-tenancy, and 89+ modular vertical slices.
- Generated interactive high-level architecture overview artifact (`posthog_architecture_overview.md`) with topology diagrams, entry point maps, and complete end-to-end data flows (Telemetry, Session Replay, Control Plane).
- Updated Master Index (`KNOWLEDGE_BASE_MASTER_INDEX.md`), Sub-Project Registry (`PROJECT_REGISTRY.md`), and Monorepo Architecture Map (`ARCHITECTURE_MAP.md`).
