# ADR-004: Dynamic RBAC & Fine-Grained Permission Overrides

**Date:** September 2026  
**Status:** Accepted (Implemented in Migration `00103`)  
**Context Source:** `clinic-app/ai-toolkit/specs/dynamic-rbac-stories.md`  

---

## 1. Context & Problem Statement
Role-Based Access Control (RBAC) with fixed roles (`clinic_admin`, `practitioner`, `staff`) creates rigidity when a clinic owner wants to grant a specific staff member extra capabilities (e.g. "Allow Sarah the receptionist to issue refunds up to $100") without promoting them to full `clinic_owner`.

---

## 2. Decision Outcome
We implemented **Dynamic RBAC Overrides** via the `user_permission_overrides` table:

```sql
CREATE TABLE user_permission_overrides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    clinic_id UUID NOT NULL REFERENCES clinics(id) ON DELETE CASCADE,
    permission VARCHAR(100) NOT NULL,
    is_allowed BOOLEAN NOT NULL DEFAULT true, -- true = grant, false = deny
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT user_clinic_permission_unique UNIQUE(user_id, clinic_id, permission)
);
```

### Permission Evaluation Flow:
```text
Has Explicit Override in user_permission_overrides?
   ├── YES (is_allowed = true)  ➔ GRANT PERMISSION
   ├── YES (is_allowed = false) ➔ DENY PERMISSION
   └── NO                       ➔ Fall back to Role Permissions in roles table
```

---

## 3. Consequences & Benefits
- Zero role proliferation (no need to create custom roles for every individual staff combination).
- Granular anti-lockout protection (prevents revoking owner permissions).
