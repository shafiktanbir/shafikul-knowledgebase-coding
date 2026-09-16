# ADR-002: Jane-Aligned Relational Service & Discipline Model

**Date:** August 2026  
**Status:** Accepted (Implemented in Migrations `00044` & `00045`)  
**Context Source:** `clinic-app/clinic-booking-app-backend/docs/WHY_JANE_MODEL.md`  

---

## 1. Context & Problem Statement
Legacy service models stored service-to-branch mappings as hierarchical JSON arrays or tightly coupled single-branch foreign keys. This caused two core problems:
1. Searching services by discipline (e.g. "Show all Speech Therapy services") required O(n²) scans across jsonb arrays.
2. Multi-branch clinics could not customize per-branch pricing without creating duplicate un-categorized service entries.

---

## 2. Decision Outcome
We adopted the **Jane-Aligned Relational Model** by creating a top-level `departments` table and linking `services.department_id`:

```sql
CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_id UUID NOT NULL REFERENCES clinics(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE services ADD COLUMN department_id UUID NOT NULL REFERENCES departments(id);
```

Per-branch pricing is handled Jane-style by duplicating the service row for specific branches (`branch_id`) while sharing global defaults (`is_shared = true`).

---

## 3. Consequences & Benefits
- **O(1) Discipline Filtering:** Patients can instantly filter services by discipline across any clinic branch.
- **Data Migration Alignment:** Matches Jane App's exact relational schema, making legacy Jane service imports 100% loss-less.
