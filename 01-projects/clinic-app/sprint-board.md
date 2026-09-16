# 🏥 Clinic App — Active Sprint Board & Serialized Roadmap Tracker

**Target Repository:** `/home/shafikul/Documents/office_work/clinic-app`  
**Current Sprint:** Sprint 2026-W37  
**Roadmap Status:** Phase 1 MVP (Running & Active) | Phase 2 (Next Core) | Phase 3 (Future Backlog)  

---

## 🟢 Phase 1: High Priority MVP Serialized Feature Status Matrix

| ID | Feature Name | Description & Key Details | Dependencies / Module | Status |
| :--- | :--- | :--- | :--- | :---: |
| **1** | **Simple Sign-In & Registration Fix** | Redesign sign-in and sign-up pages to eliminate patient confusion on desktop and mobile. | `frontend/pages/auth` | 🟡 In Progress |
| **2** | **Centralized Login System (emm solution)** | Single login for users across all clinics. Users log in once and switch between clinics. | FusionAuth / SSO Hub | ⏳ Pending |
| **3** | **Patient Dashboard & Custom Booking** | Upcoming/past visits with cancel reasons; dynamic service durations (30m, 45m, 60m); consecutive back-to-back slot bookings. | `appointments` / `services` | 🟡 In Progress |
| **4** | **Telehealth & Video Calls (Jitsi & Zoom)** | In-browser calls via dashboard link (Jitsi active, Zoom integration pending). | `telehealth_sessions` | 🟡 In Progress |
| **5** | **Automated Patient Intake Forms** | Online medical form link automatically emailed to patient immediately after booking. | `intake_forms` / `form_submissions` | ✅ Complete |
| **6** | **Doctor Note-Taking & Patient Profile** | Private SOAP notes and visit updates attached to patient chart. | `patient_charts` | ✅ Complete |
| **7** | **Patient Email & Portal Communication** | Two-way messaging; patient replies via email or portal; document sharing (PDFs, insurance cards). | `conversations` / `patient_documents` | ✅ Complete |
| **8** | **Patient Card Onboarding & SaaS Payments** | Patients save cards to platform Stripe account; central collection and clinic payout scheduling. | `patient_payment_methods` | 🟢 **RUNNING** |
| **9** | **Automatic Notifications** | Automated instant booking confirmations, 24h reminders, pre-call telehealth link notifications. | `patient_notifications` | ✅ Complete |
| **10** | **Dynamic RBAC & Granular Permissions** | Clinic owners invite staff and customize fine-grained role/view/edit permissions. | `user_permission_overrides` | 🟢 **RUNNING** |
| **11** | **Semi-Manual Insurance System (BC MVP)** | Patients enter BC PHN & insurance info; clinic staff use semi-manual verification & claim workflow. | `patient_fundings` | 🟢 **RUNNING** |
| **11b** | **Admin Urgency Concerns & Task Tracker** | UI board showing patients missing CC/funding after booking; card bypass action with audit logging. Fully tested with Jest, Playwright, and Chrome DevTools MCP. | Left Sidebar Widget | ✅ **Complete** |
| **12** | **Full App QA & End-to-End Testing** | Mobile responsiveness, payment flow verification, bug sweeps, Playwright & Chrome E2E tests. | `tests/e2e` | 🟡 In Progress |
| **14** | **Group & Funded Batch Bookings** | Recurring weekly group session bookings using approved government/grant funding credits. | `reservations` / `patient_fundings` | ⏳ Queued |
| **15** | **Calendar Sync (Google Calendar & iCal)** | Doctors and patients sync up to 1 month of upcoming appointments to Google/Apple Calendar. | `calendar-sync` | 🔜 **NEXT** |
| **16** | **Jane App Data Migration Hub** | Automated transfer of patient profiles, appointment history, and clinical SOAP notes from Jane CSV/ZIP export. **2026-09-15:** Owner-only RBAC hardening extended — execute/rollback routes now `requireRole('owner')` only; defense-in-depth assertions in controller; `fusionAuthClient.ts` created for atomic FA-first email sync; `USERS_UPDATE_EMAIL` permission added to registry; frontend rollback button gated by `isOwner`. | `data_migration_jobs` | ✅ **COMPLETE / SECURITY HARDENED** |
| **18** | **Audit Logs & Privacy Controls (HIPAA/PIPEDA)** | Ticket-reference audit logs, automatic PHI masking on admin overview screens, JIT elevated staff access. | `clinic_audit_logs` | ✅ Complete |
| **19** | **Subscription Package Control & Gating** | Tiered feature gating for SaaS clinics. **Decision:** Enforced at application layer via API middleware gates. | `subscription_plans` | 🔜 **NEXT** |
| **20** | **Reporting Billing & Operational Analytics** | Executive dashboard showing clinic revenue, booking volume, SLA acceptance rates, and cancellation rates. | `reporting-epic` | 🟡 In Progress |
| **A/R** | **Accounts Receivable Aging Tracker** | Admin console listing unpaid patient balances grouped by aging buckets (0-30, 31-60, 61-90, 90+ days). | `invoices` / `transaction_splits` | 🟢 **RUNNING** |
| **FILE** | **Unified File & Document Management** | Single interface for viewing all patient files with granular access control & permission R&D. | `patient_documents` | 🟡 In Progress |

---

## 📈 Phase 2: Next Version (Core Enhancements)

| ID | Feature Name | Key Details | Status |
| :--- | :--- | :--- | :--- |
| **13** | **Live Telehealth Transcripts** | Real-time speech-to-text transcription during video calls to speed up clinical note-taking. | ⏳ Planned |
| **REV** | **Accidental Payment Reversal Action** | Quick 1-click payment refund/revert action for accidental clicks during checkout. | ⏳ Planned |

---

## 🔮 Phase 3: Future Backlog (Later Expansion)

| ID | Feature Name | Key Details | Status |
| :--- | :--- | :--- | :--- |
| **21** | **Threshold Billing & Weekly Calculations** | Automated financial forecasting; upcoming 7-day recurring charges and projected weekly earnings. | 🔮 Backlog |
| **22** | **Generalize App for Non-Clinic Businesses** | Dynamic terminology dictionary (changing "Patient" ➔ "Client", "Doctor" ➔ "Consultant") for wellness/coaching. | 🔮 Backlog |

---

## 📜 Historical Daily Activity Log

### [2026-09-11]
- Synced Master Product Roadmap & Serialized MVP Feature Status Matrix (Phase 1, 2, 3).
- Documented Application Layer Enforcement Decision for Subscription Package Control (`Item 19`).
- Confirmed Running Status for Patient Card Onboarding (`Item 8`), Dynamic RBAC (`Item 10`), Semi-Manual Insurance (`Item 11`), Accounts Receivable Aging Tracker (`A/R`), and Admin Urgency Concern Widget (`Item 11b`).
- Updated Jane App Data Migration Hub (`Item 16` - EPIC-10) with 9 developer user stories.

### [2026-09-12]
- **Jane Migration Hub Hardening & Production Delivery (ADR-006):**
  - Resolved 8 major engineering struggles across remote DB latency, schema constraints, and VPS deployment.
  - Slashed remote WAN DB ingestion from 15–20 minutes down to **727ms** using 100-record batch chunking and hash pre-caching.
  - Eliminated synthetic fake emails; applied migration `00118_make_users_email_nullable.js` to allow clean `email: null` staff records.
  - Implemented Owner-Only RBAC security guardrails for user and staff email updates (HTTP 403/409 enforcement).
  - Vectorized rollback queries into single SQL array statements, cutting execution from 35s to **151ms** and eliminating Axios timeouts.
  - Disambiguated 3-way Jane CSV manifest signatures in `janeParser.ts`: resolved collision where `Notes_Report.csv` overwrote `Patients.csv`.
  - Accelerated clinical SOAP chart notes ingestion into `patients.practitioner_note` JSONB in batched updates.
  - Resolved production VPS deployment prefix conflict: re-indexed DB `pgmigrations` 00117 to 00118 and pushed clean migration commits (`ac104f7`, `7bed1e4`) to `origin/main`.

### [2026-09-13]
- **File Management & Reporting Architecture Audit (EPIC-09 & AI Toolkit):**
  - **File Management Audit:** Verified backend storage interface (`IDocumentStorage.ts`) and DigitalOcean Spaces provider (`SpacesDocumentStorage.ts`) are functional (~40%), but identified critical **P0 blocker**: missing `patient_documents` table migration and patient-scoped directory structure (`patients/{id}/documents/`).
  - **Reporting & Analytics Epics Verification (EPIC-09):** Cataloged and verified 4 core developer technical stories:
    - `ST-01`: Financial Summary, Cash Collections & A/R Aging (accrual vs. cash, 4 aging buckets, RLS views).
    - `ST-02`: Booking Volume & Practitioner Capacity Analytics (shift utilization %).
    - `ST-03`: Cancellation Rates & Attendance Analytics (unscheduled patient rebooking funnel).
    - `ST-04`: Multi-Format Async Export Engine (BullMQ/Redis worker for QuickBooks/Xero CSV/PDF).
  - **Operational Claims Slice (Developer B):** Refined Developer B breakdown (`accounts-receivable-and-claims-export-team-breakdown.md`) covering Express APIs, claims adjudication, and MCFD/AccessOAP provincial CSV export.
  - **Git Authorship Verification:** Confirmed primary authorship in `ai-toolkit`: SI-Tanbir (EPIC-09 master spec, A/R breakdown, Admin Billing Hub UI spec) with lifecycle/status refinements by Souparno Bandyopadhyay and Tonmoy Sarker.
  - **Database Readiness:** Confirmed underlying database tables (`invoices`, `transaction_splits`, `funding_claim_submissions`) from migration `00101` are active and ready for analytical views.

### [2026-09-14]
- **Universal Practitioner Detection & Migration UI/Query Optimization (ADR-008):**
  - **Universal 4-Pillar Staff Heuristic (`janeParser.ts`):** Implemented multi-file graph deduction across `Appointments.csv`, `Notes_Report.csv`, and `Patients.csv` (`Referred To`). Correctly classifies supervising clinicians, associate doctors, clinical assistants (SLPAs/BIs), and administrative staff across arbitrary medical disciplines.
  - **Regulatory License Regex Extraction:** Automatically extracts regulatory licenses across jurisdictions (e.g. `R-SLP #1005603`, `BCBA #1-23-66387`) embedded in treatment strings.
  - **Jane App Name Sanitization:** Cleans deactivation asterisks (`cleanJaneStaffName('*Amandep Sahnan')` -> `'Amandep Sahnan'`).
  - **Entity Mapping Type Safety & Badges (`Step2EntityMapping.tsx`):** Fixed null-safe `.toLowerCase()` matching bug; added practitioner badges (Supervising Clinician, Doctor/Clinician, Clinical Assistant, Admin/Front Desk), license tag display, and supervisor relationship explanations.
  - **Single-Line Treatment Layout:** Expanded container to `max-w-6xl`, applied `flex-1 min-w-0 pr-2` to titles, and `shrink-0` to controls, keeping extended healthcare titles cleanly on one line.
  - **TOAST-Bypassing Query Optimization (`dataMigration.repository.ts`):** Selective column projection in `findRecentJobs` pruned multi-megabyte JSONB columns (`manifest_json`, `mapping_config_json`, `summary_json`), cutting rollback tab query latency by 5x from **1,515ms to 303ms** with an **87% payload reduction**.
  - **Frontend SWR Hydration:** Added `sessionStorage` caching in `DataMigrationClient.tsx` for 0ms instant render and zero layout shift.
  - **Full E2E Localhost Verification:** Tested on `http://shafi1.localhost:3000` and `http://localhost:8000`. Verified owner logout route protection guard, loaded 50 migrated patients per page on `/dashboard/clients`, and verified individual client booking metrics ("Aagman Deol" with 70 bookings, 45 upcoming, $500 outstanding claims).

### [2026-09-15]
- **Owner-Only Email Permission Hardening + FusionAuth SSO Email Sync (ADR-009):**
  - **Critical Gap Found:** Email changes in local PostgreSQL were NOT synced to FusionAuth, causing login breakage (403 "not registered") for staff whose emails were updated by the owner.
  - **`fusionAuthClient.ts` [NEW]:** FusionAuth Admin API wrapper implementing atomic, FA-first email sync. Pattern: PATCH FA → if FA fails abort (502); if FA succeeds → UPDATE PostgreSQL; if DB fails → best-effort rollback FA.
  - **`user.controller.ts` [MODIFIED]:** Replaced simple `userRepository.update(email)` with atomic FA-first 4-step sequence. Added unauthorized attempt audit log (`logger.warn`) and successful email change audit log (`logger.info`).
  - **`patients.permissions.ts` [MODIFIED]:** Added `USERS_UPDATE_EMAIL = 'users:update:email'` enum entry. Owner-only by default. Registered in module entries for RBAC UI visibility.
  - **`dataMigration.routes.ts` [MODIFIED]:** Separated execute + rollback endpoints from the shared `requireRole('owner', 'admin')` guard; applied `requireRole('owner')` specifically to those two destructive endpoints.
  - **`dataMigration.controller.ts` [MODIFIED]:** Added defense-in-depth `isOwner` assertion inside `executeMigration()` and `rollback()` controller methods (belt-and-suspenders beyond route middleware).
  - **`ActiveRollbackCard.tsx` [MODIFIED]:** Added `isOwner` prop. Rollback button disabled + tooltip for non-owners.
  - **`DataMigrationClient.tsx` [MODIFIED]:** Derives `isOwner` from `useAuth()`, passes it to `ActiveRollbackCard`.
  - **TypeScript Verified:** Backend `tsc --noEmit` exits 0. Frontend — zero errors in changed files.
  - **Graphify Updated:** 19,113 nodes, 24,974 edges.
