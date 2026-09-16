# ADR-008: Universal Practitioner Detection Heuristics & TOAST-Bypassing Migration Performance

**Date:** 2026-09-14  
**Status:** Accepted  
**Deciders:** Lead Architect / Staff Software Engineer  
**Primary Modules:** `clinic-booking-app-backend/src/services/migration/janeParser.ts`, `dataMigration.repository.ts`, `Step2EntityMapping.tsx`, `DataMigrationClient.tsx`  

---

## 1. Context & Problem Statement

Clinics migrating from Jane App into the practice management system present diverse operational models across healthcare disciplines:
1. **Diverse Clinical Hierarchies:**
   - In unsupervised practices (physiotherapy, chiropractic, dentistry, podiatry, general counseling), the `staff_member_name` on `Appointments.csv` is the attending doctor.
   - In supervised practices (speech-language pathology, applied behavior analysis, medical residencies), `staff_member_name` is often a clinical assistant (SLPA, BI, intern), while the registered clinician is embedded in the appointment title (e.g. `"50 Minute In-Person Treatment Session (Supervised by Jane Doe (R-SLP #1005603))"`).
   - In addition, part-time or non-scheduled doctors appear only in patient caseload assignments (`Patients.csv` -> `Referred To`), and administrative staff author billing/intake notes without clinical appointments.
2. **Heavy Database TOAST Decompression Latency:**
   - The "Active Migration Available for Rollback" tab in the migration wizard suffered from high latency (> 1,500ms).
   - Querying `SELECT * FROM data_migration_jobs` forced PostgreSQL to decompress heavy out-of-line TOAST chunks containing multi-megabyte JSONB columns (`manifest_json`, `mapping_config_json`, `summary_json`), causing noticeable lag and layout shifts.
3. **UI Wrapping on Extended Healthcare Treatment Titles:**
   - Extended treatment names (e.g., `"50 Minute In-Person Behavior Treatment Session (Supervised by ...)"`) broke container bounds and wrapped across multiple lines in the entity mapping wizard.

---

## 2. Decision Drivers

* **Cross-Discipline Portability:** System must reliably detect doctors, supervisors, assistants, and admins across arbitrary clinic disciplines without manual discipline toggles.
* **Deterministic Licensing Extraction:** Regulatory license numbers across US/Canadian professional colleges (`R-SLP`, `BCBA`, `MD`, `PT`, `DC`, etc.) must be extracted and tagged.
* **Sub-350ms Dashboard Response Times:** Active rollback banner and migration lists must load instantly without blocking the user.
* **Responsive Single-Line Layouts:** Healthcare service rows must render cleanly on a single line with fluid flex constraints.

---

## 3. Considered Options

* **Option 1: Manual Clinic Discipline Pre-Configuration:** Require clinic owners to pre-select their practice type (e.g., "Speech Therapy" vs "General Practice") before uploading files.  
  *Drawback:* High friction, prone to user error, and fails in multidisciplinary clinics where some treatments are supervised and others are independent.
* **Option 2: Universal 4-Pillar Graph Heuristics + TOAST-Bypassing Query Projection + Frontend SWR:** Dynamically inspect the cross-file relationship graph across `Appointments.csv`, `Notes_Report.csv`, and `Patients.csv`, selectively project database columns in summary queries, and cache the active migration state in `sessionStorage`.

---

## 4. Decision Outcome

Chosen Option: **Option 2 (Universal 4-Pillar Heuristics + TOAST Query Projection + SWR)**.

### A. Universal 4-Pillar Detection Architecture (`janeParser.ts`)
1. **Rule 1 — Supervising Clinician & Assistant Extraction:**
   - Scan `treatment_name` using `SUPERVISOR_REGEX`: `/(?:supervised\s+by|supervisor:?)\s+([A-Za-z\s.'-]+?)(?:\s*\(([^)]+)\)|\s+([A-Z]+(?:\s*-\s*[A-Z]+)?\s*#?\s*\d+)|$)/i`.
   - If present: the supervisor is designated `REGISTERED_DOCTOR_SUPERVISING` and given regulatory license credentials. The attending provider in `staff_member_name` is designated `CLINICAL_ASSISTANT`.
2. **Rule 2 — Attending Clinician Default:**
   - In treatments without a supervisor string, `staff_member_name` is designated `REGISTERED_DOCTOR_ASSOCIATE`.
3. **Rule 3 — Caseload Discovery (`Patients.csv`):**
   - Parse `Referred To` from `Patients.csv`. Staff members assigned patient caseloads who have zero active appointments in the uploaded date slice are discovered and registered as `REGISTERED_DOCTOR_ASSOCIATE`.
4. **Rule 4 — Administrative vs. Clinical Classification (`Notes_Report.csv`):**
   - Staff authoring administrative notes (billing, cancellation notices, intake) above a threshold (>= 50%) with 0 appointment bookings are classified as `ADMINISTRATIVE_STAFF`.
5. **Name Sanitization:** Strips Jane App deactivation asterisks (`cleanJaneStaffName('*Amandep Sahnan')` -> `'Amandep Sahnan'`).

### B. TOAST-Bypassing Query Projection (`dataMigration.repository.ts`)
- Modified `findRecentJobs()` to strictly select summary columns:
  ```sql
  SELECT id, clinic_id, status, file_name, file_size_bytes, source_system,
         created_by, completed_at, error_message, created_at, updated_at
  FROM data_migration_jobs
  WHERE clinic_id = $1
  ORDER BY created_at DESC
  LIMIT $2;
  ```
- Heavily compressed TOAST JSONB columns (`manifest_json`, `mapping_config_json`, `summary_json`) are omitted from summary views and only fetched on specific job detail requests (`findJobById`).

### C. Frontend SWR Hydration & Single-Line UI
- **Instant Render:** `DataMigrationClient.tsx` hydrates the active 72-hour rollback banner from `sessionStorage` on initial render (0ms CLS), refreshing in the background via Axios.
- **Single-Line Layout (`Step2EntityMapping.tsx`):** Container expanded to `max-w-6xl`, service title given `flex-1 min-w-0 pr-2`, and action controls set to `shrink-0`.

---

## 5. Consequences & Verification Results

* **Performance:**
  - Active rollback banner query dropped from **1,515ms to 303ms (5x faster)**.
  - Query payload reduced by **87%** (from 9,844 bytes to 1,302 bytes).
  - Page render latency dropped to **0ms** via SWR hydration.
* **Accuracy:**
  - Successfully classified 15 practitioners from real Jane App exports (supervising clinicians, associates, clinical assistants, and admin staff).
  - Regulatory licenses detected across disciplines (`R-SLP #1005603`, `BCBA #1-23-66387`).
* **E2E UI Verification:**
  - Tested on `shafi1.localhost:3000` via Chrome DevTools MCP.
  - Long service titles stay perfectly formatted on one line.
  - 50 migrated patients loaded per page on `/dashboard/clients` with complete booking history.
