# Backend Architecture & Technical Guidelines

This area contains technical standards, database design rules, API conventions, and security guidelines for backend development.

---

## 🏛️ Core Engineering Principles
1. **Explicit Control Flow:** Prefer clarity over hidden magic. Write self-documenting code.
2. **Database Integrity:** Always use foreign keys with explicit cascade policies (`ON DELETE CASCADE` / `RESTRICT`).
3. **Multi-Tenant Security:** Stamp every database table with `clinic_id` (Tenant UUID) and enforce Row-Level Security (RLS).
4. **Idempotency:** All batch ingestion scripts and background workers must be idempotent (safe to rerun without duplicating data).
5. **Hybrid OLTP/OLAP Workload Isolation:** Never run large-scale analytical aggregation queries against primary operational transactional databases (PostgreSQL); route analytical event workloads to columnar OLAP engines (ClickHouse).
6. **Distributed Resilience & Rate Limiting:** Enforce token-bucket continuous refill rate limiting and Redis-backed atomic Lua circuit breakers (`posthog:dbcb`) on hot database connection paths to prevent cascading failures.

---

## 📂 Sub-Directory & Reference Implementations Overview
* `database-migrations/` — Standards for Knex schema migrations.
* `api-contracts/` — OpenAPI / Postman collection specs.
* `security-rbac/` — Role-based access control and JWT authentication rules.
* 🦔 **Enterprise Reference Implementation:** [`knowledgebase/01-projects/posthog/architecture.md`](../../01-projects/posthog/architecture.md) — Production deep-dive of Hybrid OLTP/OLAP, Kafka streaming, PersonHog identity mesh, HogQL query compiler, and vertical slice modular isolation.

