# PostHog — Enterprise Open-Source Product Analytics & Platform Architecture

> **Monorepo / Workspace Path:** `/home/shafikul/Documents/opensource_project/posthog`  
> **Host Repository & Pipeline Tracker:** `/home/shafikul/Documents/opensource_project/`  
> **Category:** Enterprise Commercial Open-Source Software (COSS) / Analytics Platform  
> **Status:** Active Target in "Contribute-to-Hire" Pipeline (Conviction Score: **98/100**, Stage: `Evaluating`)  

---

## 1. Executive Summary

**PostHog** is the leading open-source product analytics, session replay, feature flagging, A/B testing, surveys, error tracking, and data warehouse platform. Backed by Y Combinator (W20) and top-tier venture capital (Series B, $55M+), PostHog operates a massive polyglot monorepo engineered to process billions of events per day at extreme throughput and sub-second analytical query latencies.

Within Shafikul Islam's engineering career operations, PostHog represents the **#1 primary target repository** for the Enterprise Open Source **"Contribute-to-Hire"** strategy.

---

## 2. Core Technology Stack Matrix

| Architectural Domain | Primary Technologies | Key Responsibility |
| :--- | :--- | :--- |
| **High-Throughput Ingestion** | **Rust**, **Apache Kafka** | Edge event capture proxy (`rust/capture`), log/metrics streaming, PII redaction. |
| **Distributed Identity** | **Rust** (`personhog`), **PostgreSQL** | Distributed identity resolution, distinct ID leasing, person merges, overrides. |
| **OLAP Analytics Database** | **ClickHouse** | Columnar distributed store for trillions of events, replays, and analytical aggregations. |
| **Unified Query Layer** | **HogQL** (Python + Rust AST parser) | SQL dialect transpiled safely to ClickHouse SQL with tenant isolation and virtual schemas. |
| **OLTP Control Plane** | **Python (Django 4.x / DRF)**, **PostgreSQL** | Multi-tenant organization/team metadata, feature flags, RBAC, dashboards, billing. |
| **Async Orchestration** | **Celery**, **Redis**, **Temporal** | Periodic jobs, webhook dispatch, distributed locks, durable long-running workflows. |
| **Modular Products** | **Vertical Slices** (89+ products) | Decoupled sub-apps in `products/` (models, logic, routes, facades, presentation, MCP). |
| **AI & MCP Gateway** | **Go** / **Python**, **Model Context Protocol** | Unified LLM routing (`ai-gateway`), native MCP server & UI tools (`services/mcp`). |
| **Frontend Architecture** | **TypeScript**, **React**, **Kea**, **Lemon UI**, **Tailwind** | Redux/Saga-style Kea logic state machines, Lemon design system, Quill for MCP apps. |
| **Developer Experience** | **hogli** (Python CLI), **Flox**, **Tach**, **Turbo** | Universal test runner, scaffolding, import boundary enforcement, monorepo caching. |

---

## 3. Key Monorepo Entry Points

All code paths below reside in `/home/shafikul/Documents/opensource_project/posthog`:

- **Edge Capture & Ingestion (Rust):** [`rust/capture/`](file:///home/shafikul/Documents/opensource_project/posthog/rust/capture/)
- **Distributed Identity Cluster (Rust):** [`rust/personhog-identity/`](file:///home/shafikul/Documents/opensource_project/posthog/rust/personhog-identity/) and [`rust/personhog-router/`](file:///home/shafikul/Documents/opensource_project/posthog/rust/personhog-router/)
- **Django Core & API Routing:** [`posthog/api/__init__.py`](file:///home/shafikul/Documents/opensource_project/posthog/posthog/api/__init__.py) and [`posthog/settings/web.py`](file:///home/shafikul/Documents/opensource_project/posthog/posthog/settings/web.py)
- **HogQL Query Engine:** [`posthog/hogql/`](file:///home/shafikul/Documents/opensource_project/posthog/posthog/hogql/) and [`posthog/hogql_queries/`](file:///home/shafikul/Documents/opensource_project/posthog/posthog/hogql_queries/)
- **Modular Products Directory:** [`products/`](file:///home/shafikul/Documents/opensource_project/posthog/products/) (89+ vertical slices including `feature_flags`, `session_replay`, `data_warehouse`, `posthog_ai`)
- **Model Context Protocol (MCP) Services:** [`services/mcp/`](file:///home/shafikul/Documents/opensource_project/posthog/services/mcp/) and individual product definitions in `products/*/mcp/tools.yaml`
- **Frontend Core & Logic:** [`frontend/src/`](file:///home/shafikul/Documents/opensource_project/posthog/frontend/src/)
- **Developer CLI (`hogli`):** [`tools/hogli/`](file:///home/shafikul/Documents/opensource_project/posthog/tools/hogli/) and [`hogli.yaml`](file:///home/shafikul/Documents/opensource_project/posthog/hogli.yaml)

---

## 4. Documentation Index

- 📐 **Detailed Architectural Deep Dive:** [`architecture.md`](architecture.md) — Comprehensive breakdown of data ingestion, ClickHouse/HogQL query engine, personhog distributed identity, multi-tenancy OLTP patterns, modular product isolation, and AI/MCP integrations.
- 🎯 **Sprint & Contribution Tracker:** [`sprint-board.md`](sprint-board.md) — Active local development setup, starter issues, high-impact PR targets, and contribution lifecycle.
- 📜 **Upstream Developer Guide:** [`posthog/AGENTS.md`](file:///home/shafikul/Documents/opensource_project/posthog/AGENTS.md) — Upstream engineering conventions, commit rules, and lint invariants.
