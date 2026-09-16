# ADR-001: Multi-Tenant User Clinic Roles Junction Model

**Date:** August 2026  
**Status:** Accepted (Implemented in Migration `00096`)  
**Context Source:** `clinic-app/ai-toolkit/repository_sql_audit_user_clinic_roles.md`  

---

## 1. Context & Problem Statement
In earlier iterations of `clinic-app`, user membership and role assignments were stored directly as columns on the `users` table (`users.clinic_id` and `users.role_id`). This prevented a single practitioner or administrator from belonging to multiple clinics or holding different roles across different clinic branches.

---

## 2. Decision Outcome
We decided to decouple user identity from tenant membership by dropping `users.clinic_id` and `users.role_id`, and introducing the `user_clinic_roles` junction table:

```sql
CREATE TABLE user_clinic_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    clinic_id UUID NOT NULL REFERENCES clinics(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT user_clinic_roles_user_id_clinic_id_unique UNIQUE(user_id, clinic_id)
);
```

---

## 3. Positive Consequences
- **Multi-Tenant Mobility:** A practitioner (e.g. Dr. Jane Smith) can now log in once and belong to multiple distinct clinic accounts with different permissions per clinic.
- **FusionAuth SSO Alignment:** Preserves single global user email identity in `users` while delegating tenant authorization to `user_clinic_roles`.

---

## 4. Negative Trade-offs
- Authentication middleware must query `user_clinic_roles` on active clinic context switches instead of reading a static `users.clinic_id` column.
