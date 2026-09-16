# ADR-006: Jane Data Migration Hub Ingestion Optimization, Schema Harmonization & Deployment Stability

**Date:** September 11–12, 2026  
**Status:** Accepted & Implemented  
**Scope:** `clinic-booking-app-backend`, `clinic-booking-app-frontend`, PostgreSQL DB (`165.245.234.77:5432`), VPS Deployment CI/CD  
**Context Source:** Jane App Data Migration Hub (EPIC-10) Production Hardening  

---

## 1. Context & Architectural Challenges ("The 8 Struggles")

During live testing and deployment of the Jane App Automated Migration Hub across a WAN remote PostgreSQL database (`165.245.234.77:5432`), eight interconnected engineering challenges emerged:

### Struggle 1: WAN Network Latency Stalls (15–20 Mins for 1,176 Patients)
- **Root Cause:** Sequential row-by-row queries (`SELECT`, `INSERT`, `UPDATE`) created ~3,500 synchronous WAN roundtrips. Over a 30ms WAN ping, this resulted in 15–20 minutes of execution time. If the user closed the browser or experienced a Wi-Fi drop, the SSE stream severed and the UI hung.
- **Decision & Solution:** 
  - Refactored `streamCsvBatches` to process in 100-row vectorized chunks.
  - Pre-cached existing services, staff mappings, and locations into in-memory hash maps before batch processing.
  - Vectorized patient queries via `WHERE email = ANY($1::text[])` and multi-row parameterized `INSERT` statements.
  - Decoupled background Node.js batch execution from browser SSE connections: the worker continues running to completion even if the client disconnects.
  - **Result:** Cut 1,176 patient ingestion time from 15–20 minutes down to **727 milliseconds** (a 99% reduction).

### Struggle 2: The Fake Staff Email Dilemma (`users.email` NOT NULL)
- **Root Cause:** Jane App CSV exports (`Appointments.csv` and `Notes_Report.csv`) provide practitioner names but *never* include staff emails. The legacy code generated fake `@jane.clinic` synthetic emails because the PostgreSQL `users` table had a strict `NOT NULL` constraint on `email`.
- **Decision & Solution:** 
  - Applied migration `00118_make_users_email_nullable.js` (`ALTER TABLE users ALTER COLUMN email DROP NOT NULL;`).
  - Capitalized on PostgreSQL's SQL-standard behavior where `UNIQUE(email)` permits multiple `NULL` entries (`NULLS DISTINCT`).
  - Saved unmapped practitioners with `email: null`, eliminating all fake synthetic addresses.
  - Updated frontend staff lists and profile components to gracefully display `"No email provided"`.

### Struggle 3: Owner-Only User & Staff Email Permissions (RBAC)
- **Root Cause:** Lack of role-based authorization allowed non-owners to modify user email addresses, creating identity spoofing and credential hijacking risks.
- **Decision & Solution:**
  - Enforced server-side checks in `practitioner.controller.ts` and `user.controller.ts`: if `email` is modified, verify `req.user.roleName.toLowerCase() === 'owner'`, rejecting non-owners with `HTTP 403 Forbidden`.
  - Enforced duplicate email collision rejection with `HTTP 409 Conflict`.
  - Frontend (`EditPractitionerForm.tsx`) dynamically locks the field as read-only with a tooltip for non-owners, and unlocks it exclusively for the clinic Owner.

### Struggle 4: Axios 30-Second Browser Timeout on Rollback
- **Root Cause:** `rollback()` performed 368 sequential row-by-row `DELETE` and `UPDATE` statements. Over the remote WAN DB, this took 30–35 seconds. The frontend Axios client timed out at 30 seconds (`timeout: 30000`), displaying an error screen while the DB was still deleting in the background.
- **Decision & Solution:**
  - Vectorized the rollback engine into single PostgreSQL array queries:
    - `DELETE FROM patients WHERE id = ANY($1::uuid[])`
    - `UPDATE patients SET clinic_ids = ... WHERE id = ANY($2::uuid[])`
    - Vectorized deletion for appointments, services, and staff.
  - **Result:** Slashed rollback execution from 35 seconds down to **151 milliseconds**.
  - Enhanced `Step6CompletionDashboard.tsx` to query job status on mount, automatically rendering the reset state upon page refresh.

### Struggle 5: 3-CSV Manifest Collision (Missing 2nd CSV & Slow Migration Root Cause)
- **Root Cause:** When uploading 3 CSVs (`Patients.csv` [1,328 rows], `Notes_Report.csv` [1,156 rows], `Appointments.csv` [36 rows]), the UI only showed 2 files. Jane's `Notes_Report.csv` contains columns `patient_guid` and `email`. Because the `patientsFile` check in `janeParser.ts` ran first, it misclassified `Notes_Report.csv` as `patientsFile`, overwriting the real Patients file and leaving `notesReportFile` undefined.
- **Consequence:** The engine attempted to insert 1,156 clinical SOAP notes into the `patients` table, causing massive unique constraint collisions (`patients_email_key`), severe stalls, and skipping SOAP notes entirely!
- **Decision & Solution:**
  - Reordered and hardened CSV inspection signatures in `inspectJaneDirectory`:
    1. **Notes Report**: Matched by `note type`, `author`, `text`, or `notes_report` / `notes` in filename.
    2. **Appointments**: Matched by `start_at` and `treatment_name`, or `appointment` in filename.
    3. **Patients**: Matched by `patient_guid` and `birth date` / `mobile phone` / `family doctor` / `patient` in filename.
  - **Result:** Restored 3-file manifest display (1,328 Patients, 36 Appointments, 1,156 Notes Report) with zero collisions.

### Struggle 6: Batched SOAP Chart Notes Ingestion (Phase 5)
- **Root Cause:** Because `notesReportFile` was previously undefined, Phase 5 never ran. Furthermore, row-by-row updates to `patients.practitioner_note` JSONB over the WAN DB took 70+ seconds.
- **Decision & Solution:**
  - Integrated `streamCsvBatches` with chunk size 100 for `Notes_Report.csv`.
  - Grouped notes by `patient_guid` and author in memory, appending to `patients.practitioner_note` JSONB in batched updates.
  - Recorded entity mappings in bulk using `createEntityMappingsBatch`.
  - **Result:** 1,156 SOAP notes import in **~1–2 seconds**, attaching historical clinical notes to patient charts.

### Struggle 7: Production VPS Deployment Migration Prefix Collision (00117 Conflict)
- **Root Cause:** During VPS deployment, container startup aborted with:
  `❌ MIGRATION CONFLICT: File "00117_make_appointment_id_optional_on_invoices.js" shares prefix "00117" with already applied migration "00117_make_users_email_nullable" in database.`
  Another teammate merged `00117_make_appointment_id_optional_on_invoices.js` while the database had already recorded `00117_make_users_email_nullable`.
- **Decision & Solution:**
  - In PostgreSQL `pgmigrations`, updated row 143:
    `UPDATE pgmigrations SET name = '00118_make_users_email_nullable' WHERE id = 143;`
  - Renamed the migration to `migrations/00118_make_users_email_nullable.js` and pushed it to `origin/main` via isolated commit `7bed1e4`.
  - Restored strictly consecutive, gapless migrations on `main`:
    `00115` ➔ `00116` ➔ `00117` ➔ `00118`.
  - Verified with `DRY_RUN=true node scripts/migrate.js` (exit code 0, all up to date).

### Struggle 8: Multi-Row Insert Unique Email Collisions in Patient Batches
- **Root Cause:** In multi-row parameterized `INSERT INTO patients ... VALUES (...)`, if an email already exists in the clinic or appears multiple times in the CSV, a raw multi-row insert triggers PostgreSQL error 23505 (`patients_email_key`).
- **Decision & Solution:**
  - Before inserting a batch, pre-query all unique batch emails:
    `SELECT id, email, clinic_ids FROM patients WHERE email = ANY($1::text[])`.
  - Route existing emails to `patientIdsToMerge` (updating `clinic_ids`).
  - Maintain an in-memory `knownEmailToPatientId` map across all batches so duplicate emails in subsequent rows map to the already-created patient ID instead of triggering a duplicate insert.

---

## 2. Decision Outcomes & Production Standards

1. **Strict Zero-Leak Git Workflow:** Migration files must be isolated on clean temporary worktrees off `origin/main` so that database schema changes can be merged without releasing unapproved application code.
2. **Deterministic CSV Signature Hierarchy:** Multi-file importers must inspect specialized/child files (notes, appointments) before general entity files (patients) to prevent header signature masking.
3. **Array-Vectorized Remote WAN Operations:** Over remote database connections, never use row-by-row queries for imports or rollbacks. Always use array operators (`ANY($1::uuid[])`) and batch inserts of 100 rows.
4. **PostgreSQL Nullable Unique Fields:** For external platforms that do not provide emails, use nullable unique columns (`DROP NOT NULL`) instead of fabricating fake domain emails.

---

## 3. Related Documents
- [ADR-005: Jane App Automated Data Migration Engine Architecture](file:///home/shafikul/Documents/coding/research-playground-loop/knowledgebase/01-projects/adr/ADR-005-jane-app-data-migration-engine.md)
- [Clinic App Sprint Board](file:///home/shafikul/Documents/coding/research-playground-loop/knowledgebase/01-projects/clinic-app/sprint-board.md)
- [Backend Migration 00118](file:///home/shafikul/Documents/office_work/clinic-app/clinic-booking-app-backend/migrations/00118_make_users_email_nullable.js)
- [Jane Batch Worker](file:///home/shafikul/Documents/office_work/clinic-app/clinic-booking-app-backend/src/services/migration/janeBatchWorker.ts)
