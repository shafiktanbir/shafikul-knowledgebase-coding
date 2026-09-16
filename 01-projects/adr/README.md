# Architecture Decision Records (ADRs)

This directory contains the immutable technical decision log for system architecture, database design, and security patterns across all repositories.

---

## 📜 Active ADR Ledger

| ADR ID | Title | Status | Primary Target / Migration | Key Decision |
| :--- | :--- | :--- | :--- | :--- |
| [`ADR-001`](ADR-001-multi-tenant-user-clinic-roles.md) | Multi-Tenant User Clinic Roles Model | **Accepted** | Migration `00096` | Junction table `user_clinic_roles` replacing static `users.clinic_id`. |
| [`ADR-002`](ADR-002-jane-aligned-relational-service-model.md) | Jane-Aligned Relational Service Model | **Accepted** | Migrations `00044` & `00045` | Global `departments` table and per-branch pricing duplication. |
| [`ADR-003`](ADR-003-multi-payer-split-billing-ledger.md) | Multi-Payer Split Billing & Invoicing | **Accepted** | EPIC-08 (Migrations `00101` & `00102`) | Mandatory 1:1 `invoices` with 1:N `transaction_splits` across payers. |
| [`ADR-004`](ADR-004-dynamic-rbac-permission-overrides.md) | Dynamic RBAC & Permission Overrides | **Accepted** | Migration `00103` | Granular `user_permission_overrides` for per-user, per-clinic overrides. |
| [`ADR-005`](ADR-005-jane-app-data-migration-engine.md) | Jane App Automated Data Migration Engine | **Accepted** | EPIC-10 (Migrations `00109`–`00111`) | 5-stage async ETL engine with practitioner/service auto-discovery and 72-hr rollback. |
| [`ADR-006`](ADR-006-jane-migration-batching-resiliency-and-conflict-resolution.md) | Jane Migration Optimization & VPS Conflict Resolution | **Accepted** | Migrations `00115`–`00118` | Vectorized 100-batch WAN ingestion, nullable staff emails, owner-only RBAC, 3-way parser signatures, and sequential migration re-indexing. |
| [`ADR-007`](ADR-007-enterprise-coss-contribute-to-hire-and-hybrid-oltp-olap.md) | Enterprise COSS "Contribute-to-Hire" & Hybrid OLTP/OLAP | **Accepted** | `opensource_project` | Strategic focus on YC/CNCF venture-backed repos (PostHog), Postgres/ClickHouse dual-DB pattern, and DRF headless orchestration. |
| [`ADR-008`](ADR-008-universal-practitioner-detection-and-toast-query-projection.md) | Universal Practitioner Detection & TOAST Query Projection | **Accepted** | `janeParser.ts`, `dataMigration.repository.ts` | 4-pillar doctor/supervisor/assistant/admin graph deduction across 3 CSVs, regulatory license regex extraction, TOAST-bypassing JSONB query projection for 5x rollback query speedup, and frontend SWR hydration. |
