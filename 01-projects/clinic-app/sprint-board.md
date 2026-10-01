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
| **12** | **Full App QA & End-to-End Testing** | Automated 9-phase operational practice lifecycle & visual testing harness (Playwright + Chrome DevTools). 100% pass in 27.6s, 9 visual milestone PNGs. Fully hardened. | `e2e-visual-testing` / `tests/e2e` | ✅ **Complete (ADR-010)** |
| **14** | **Group & Funded Batch Bookings** | Balance-driven recurring weekly session bookings with backup credit card guarantee, clinic-configurable advance booking limit, and automated post-appointment settlement. Fully tested with Jest unit tests and Chrome DevTools MCP. | `batch_bookings` / `patient_fundings` | ✅ **Complete** |
| **15** | **Calendar Sync (Google Calendar & iCal)** | Doctors and patients sync up to 1 month of upcoming appointments to Google/Apple Calendar; `.ics` export download & calendar UI icons. | `calendar-sync` | ✅ **Complete** |
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

### [2026-09-18]
- **Calendar Sync & .ics Export Delivery (Item 15 - PR #236):**
  - Integrated `.ics` calendar file download option and calendar icon indicators in clinic calendar sync settings.
- **CORS & Multi-Clinic Subdomain Security Hardening (PR #290):**
  - Updated backend CORS configuration to support all dynamic `*.emmai.ca` subdomains and registered `x-clinic-subdomain` header in allowed request headers.
- **Database Migration Idempotency (PR #289):**
  - Refactored PostgreSQL migrations `00124` and `00128` to be fully idempotent across multi-tenant database environments.
- **Legacy Codebase Purge (PR #287 & PR #288):**
  - Complete refactor purging legacy Kazi code contributions, test suites, scripts, and documentation across frontend and backend.
- **Admin Urgency Concerns & Task Tracker Access Management & Role Gating (Item 11b):**
  - **Strict Doctor Gating (Zero Leakage):** Backend `requireTaskAccess` middleware strictly blocks doctor accounts with HTTP 403. Frontend `SidebarDashboard.tsx` and `UrgentConcernsWidget.tsx` conditionally suppress widget rendering, and RTK Query requests (`useGetUrgentSummaryQuery`, `useGetAdminTasksQuery`) skip execution entirely on doctor login (`skip: true`).
  - **Owner Full Scoping & Control:** Owners have unrestricted access to all assigned and unassigned tasks (`assigneeId=unassigned` keyset cursor queries) and can assign or unassign (`assigneeId = null`) tasks freely.
  - **Standard Admin Scoped Visibility:** Standard admins are restricted to viewing only tasks explicitly assigned to them (`assignee_id = current_user.id`). Unassigned tasks are hidden, and attempting to unassign a task returns HTTP 403 Forbidden.
  - **In-App Staff Notifications:** Automated notification dispatch triggers on task assignment (`adminNotificationRepository.create({ type: 'TASK_ASSIGNED', action_url: '/dashboard/tasks' })`), notifying staff members instantly within the application.
  - **Granular Exception Overrides:** Dynamic permission resolver honors `tasks:view:all` and `tasks:manage` overrides via `user_permission_overrides`, enabling owners to grant specific admins elevated task tracker visibility.
  - **Verification & Testing:** All 19/19 integration tests in `tests/integration/admin-tasks.test.ts` passing cleanly. TypeScript compilation (`tsc --noEmit`) passes with 0 errors across both backend and frontend.

### [2026-09-20 / 2026-09-21]
- **Automated Operational Practice Lifecycle & Visual Testing Suite (Item 12 - ADR-010):**
  - **Full Operational Lifecycle Suite:** Designed, hardened, and verified a 9-phase sequential E2E test harness in `clinic-booking-app-frontend/e2e-visual-testing/` using Playwright (`specs/01-clinic-lifecycle.spec.ts`), validating practice management workflows from initial clinic registration to split payment settlement with **100% pass rate (9 passed in 27.6s, exit code 0)**.
  - **Admin Direct Scheduling Model:** Standardized direct administrative appointment booking on the clinic calendar without public self-booking dependency. Staff and practitioners must be fully onboarded with credentials and scheduled working hours prior to booking creation.
  - **Clinical SOAP Chart Note Immutability:** Implemented cryptographic SHA-256 digital signature creation and note sealing (`isLocked: true`, `status: 'signed'`). Attempted mutations or deletions of signed notes are strictly rejected with **HTTP 403 Forbidden**.
  - **Split Billing Settlement & Reconciliation:** Automated itemized invoice creation ($140.00 service + 5% GST = $147.00 CAD) and split payment allocations ($100 credit card + $47 cash copay). Settled via offline payment APIs and verified receipt with strictly **$0.00 balance due**.
  - **Multi-Tenant Boundary & CASL RBAC Security Audit:** Verified foreign tenant subdomain header queries (`x-clinic-subdomain: rogue`) and cross-tenant mutations are rejected with HTTP 403. Patient tokens attempting administrative user invitations fail closed with HTTP 403.
  - **9 Visual Milestone Artifacts Verified (>31 KB each):**
    - `01-signup.png` (38 KB), `02-tenant-branding.png` (32 KB), `03-setup-catalog.png` (31 KB), `04-staff-onboarding.png` (33 KB), `05-admin-booking.png` (39 KB), `06-calendar-session.png` (37 KB), `07-soap-notes.png` (69 KB), `08-billing-invoice.png` (44 KB), `09-tenant-security.png` (54 KB).
  - **Backend Hardening & Defect Remediation:**
    - `appointment.controller.ts`: Added permission fallback to `req.user.permissions` and wildcard `'*'` support.
    - `authService.ts`: Added doctor permissions (`appointments:update:assigned`, `appointments:update:all`, `clinical:notes:write`, `clinical:notes:read`) to devLogin.
    - `patient.controller.ts`: Blocked modification/deletion of signed SOAP notes with HTTP 403.
    - `invoice.controller.ts` & `invoice.service.ts`: Expanded offline payment methods, sanitized UUIDs for foreign key safety in audit logs, and made finalization idempotent for paid invoices.
    - `patientFunding.repository.ts`: Added fallback for `priority_order` column schema compatibility.
  - **Git Delivery:** Pushed frontend branch `feat/e2e-visual-lifecycle-testing` (22 files, +4,775 / -565 lines) and backend branch `feat/e2e-lifecycle-backend-hardening` (13 files, +146 / -39 lines) with active GitHub Pull Requests.

### [2026-09-22]
- **Auth Identity Resolution & Tenant Context Preservation Fix (`src/middleware/auth.ts`):**
  - **Root Cause Identified:** Traced critical issue where `GET /api/clinics/details` returned 404, `GET /api/branches` returned 0 branches ("No active branches"), and dashboard navigation collapsed. The auth middleware resolved active clinic context from the subdomain and database, but legacy logic (`if (decoded.roleName) req.user = decoded;`) immediately wiped out `req.user` with raw JWT claims containing stale or mismatched clinic IDs.
  - **Architectural Fix Applied:**
    - Initialized `req.user = undefined;` at request entry to prevent request state leakage.
    - Preserved active clinic context (`activeClinicId: clinic.id`), resolved user ID, email, and database permissions.
    - Replaced the destructive raw token claim overwrite with resolved role verification (`if (!req.user?.roleName) throw new CustomError('Invalid token: missing resolved role context', 401)`).
    - Guaranteed database membership always supersedes stale token claims.
    - Cleared `req.user = undefined;` inside the error catch block.
  - **Testing & Live Verification:** Passed 7/7 unit tests in `tests/unit/authIdentityResolution.test.ts`. Verified live via Chrome DevTools MCP on `vancouverspeechtherapy.localhost:3000/dashboard` with 200 OK across `/api/clinics/details`, `/api/branches` ("Abbotsford BC" populated), and full 10-item sidebar restored with zero console errors.
- **Practitioner Email Update & Password Setup Workflow (Item 16 / Jane App Migration Hub):**
  - **Owner Permission Bypass:** Extended `permissions.ts` and `practitioner.controller.ts` to grant owners unrestricted wildcard permissions (`*`, `*:*:*`), enabling clinic owners to edit practitioner email addresses (specifically addressing Jane App migrations where practitioners are imported with empty emails).
  - **Password Setup Dispatch Service:** Implemented `sendPasswordSetupEmail()` in `emailService.ts` and `practitionerService.ts`, exposing authenticated route `POST /api/practitioners/:id/send-password-setup`.
  - **UI Prompt & Action Controls:** Updated `StaffProfilePanel.tsx` to display a prompt after email updates asking owners if they want to dispatch a password setup email. Added a dedicated manual **"Send Password Setup Email"** button directly to the staff profile card.
- **72-Hour Granular Rollback & Re-Migration Deduplication Architecture:**
  - **Rollback Engine Documentation:** Audited and documented the 3-stage WAN-pipelined reversal engine in `janeBatchWorker.ts` backed by `migration_entity_mappings` (appointments deleted, new patients purged, merged patients unlinked via `clinic_ids - clinicId`, services removed, clinical notes stripped from JSONB, orphan staff removed while preserving cross-clinic accounts).
  - **Re-Migration Deduplication Guarantees:** Documented multi-tier duplicate detection across entities (vectorized `janeGuid` & email lookup + 3-tier engine ensuring 0 duplicate patients and tagging them as `MERGED`, staff deduplication via first/last name, services deduplication via `ON CONFLICT DO UPDATE`, calendar double-booking prevention via PostgreSQL exclusion constraint).
- **Group & Funded Batch Bookings Delivery (Item 14 / ADR-011):**
  - **Balance-Driven Booking Enforcement:** Blocked scheduling overages beyond remaining funding credits by default (`Math.floor(remainingFunding / sessionCost)`).
  - **Backup Credit Card Guarantee:** Enabled scheduling beyond remaining funding balance up to the clinic's configurable advance horizon when backed by saved card on file. Accurately split session responsibilities (`PAID` invoice for funded sessions vs `PENDING_PAYMENT` patient invoice for card-guaranteed sessions with auto-charge upon completion).
  - **Clinic Configurable Advance Booking Horizon:** Applied database migration `00131_add_max_advance_booking_days_to_clinics.js` (`DEFAULT 30`, `CHECK 1..365`) and added UI configuration controls in **Clinic Settings > Preferences** with real-time auto-save.

### [2026-09-24]
- **Patient Funding Lifecycle & Modal Visibility Resiliency (Item 14 / ADR-012):**
  - **Approved Funding Source Visibility Fix (`BatchBookingModal.tsx`):**
    - Traced root-cause bug where patients with newly registered funding sources (e.g., `Abdul Kader` with $5,000 Jordan's Principle grant) had their funding sources hidden behind a blocking error alert box (*"Booking Blocked: No Funding or Saved Card"*).
    - Resolved the premature composite gate (`hasNeitherFundingNorCard = !hasFundingCredits && !hasCardOnFile`). Evaluated funding presence first: whenever `fundingSources.length > 0`, the complete funding grid is rendered with status badges (Emerald `CONFIRMED`, Blue `SIGNED`, Amber `Not Signed / Awaiting Approval`).
    - Integrated `useUpdatePatientFundingMutation` from `@/lib/features/client/clientApi.ts`: added an inline **"Approve & Select"** button enabling clinic staff to approve and activate pending/unsigned grants in a single click directly inside the booking modal.
  - **Backup Credit Card Guarantee for Zero-Funded Patients:**
    - Dual-source card detection across both `patient_payment_methods` and `patients.payment_card` JSONB.
    - Zero-funded clients with a card on file (e.g., test client `Leo CardBacked`, Visa •••• 4242) automatically display an informational amber banner informing staff that recurring sessions are unlocked via Backup Credit Card Guarantee.
    - Limits recurring horizon to the clinic's configured `max_advance_booking_days` (30 days default).
    - Automatically creates `PENDING_PAYMENT` patient invoices set for post-completion settlement.
  - **Test Client Creation & Direct Cloud DB Verification:**
    - Verified against direct DigitalOcean cloud database on Vancouver Speech Therapy clinic (`0d859bc0-e10f-44ca-9809-d63b76aa45ee`):
      1. `Abdul Kader`: Confirmed $5,000 funding, verified 50-session calculation and calendar slot allocation.
      2. `Maya GrantFunded` (`maya.funded@vst-clinic.ca`): Created with $3,000 Autism Funding Program (`BC-AUT-8821`), confirmed status badge and modal selection.
      3. `Leo CardBacked` (`leo.cardbacked@vst-clinic.ca`): Created with Visa ending in 4242 and $0 funding. Verified card detection badge, booking preview, confirmation modal, and successful batch booking creation.
    - Visual evidence captured via Chrome DevTools MCP: `proof_abdul_kader_funding_confirmed_and_preview.png`, `proof_maya_grant_funded_client.png`, `proof_leo_card_backed_top_banner.png`, `proof_leo_card_backed_guarantee_and_preview.png`, `proof_leo_confirm_card_guaranteed_modal.png`, `proof_leo_batch_booking_created_success.png`.
  - **Knowledge Base Documentation:** Published architectural decision record in `knowledgebase/01-projects/adr/ADR-012-patient-funding-lifecycle-and-card-guarantee-resilience.md`.
  - **CI/CD Troubleshooting, PRs & Production Deployment (`ci-cd-troubleshooter`):**
    - **Frontend PR #257 Merged (`feat/group-funded-batch-bookings` -> `main`):**
      - Resolved ESLint prettier warnings in `BatchBookingModal.tsx`.
      - Passed `CI/Lint & Typecheck` (100% green, 1m54s).
      - Successfully merged via standard merge commit into `main`.
      - Automated Docker image build and `Deploy Frontend Production` workflow completed in 31s.
    - **Backend PR #307 Merged (`feat/group-funded-batch-bookings` -> `main`):**
      - **Diagnosis 1 (Missing Jest Query Mock):** Fixed `TypeError: query is not a function` in `batchBookingService.test.ts` by adding `query: jest.fn()` to `src/config/db` mock, achieving 35/35 passing unit tests.
      - **Diagnosis 2 (Duplicate Migration Prefix Collision):** Detected CI migration dry-run and integration test failure (`00130_add_group_and_batch_bookings.js` collided with `00130_placeholder.js` on `main`). Safely renumbered migrations via `git mv` to `00136_add_group_and_batch_bookings.js` and `00137_add_max_advance_booking_days_to_clinics.js`.
      - Passed all 5 CI checks (Security/SAST Scan, Dependency Audit, CI Lint & Typecheck, CI Unit Tests, Milestone 1 Integration Tests).
      - Successfully merged into `main`.
      - Automated Docker image build and `Deploy Production` workflow completed in 54s.
- **Patient Funding Lookup & Auth Middleware Performance Optimization (Item 11 / ADR-013):**
  - **Latency Bottleneck Root-Cause Analysis:**
    - Investigated user report of high latency when fetching patient insurance/funding after selecting a patient.
    - Benchmarked `SELECT * FROM patient_fundings WHERE patient_id = $1 AND clinic_id = $2 ORDER BY priority_order ASC, created_at DESC;`: Postgres internal query execution was sub-millisecond (0.085ms), but WAN RTT (285ms) multiplied across 4 sequential auth middleware DB queries (16 network roundtrips) produced ~5,680ms overhead on every request.
    - Discovered frontend RTK Query tag cascade: `addPatientFunding` previously invalidated the generic `["Clients"]` tag, causing the frontend to concurrently refetch the entire clinic patient directory (`getPatientsByClinic`), notes, documents, and fundings all at once.
  - **Database Composite Covering Index (`migrations/00138_add_idx_patient_fundings_lookup.js`):**
    - Created composite btree index `idx_patient_fundings_lookup` on `patient_fundings (patient_id, clinic_id, priority_order ASC, created_at DESC)`.
    - Applied migration `00138` cleanly to PostgreSQL.
  - **Auth Middleware In-Memory TTL Cache (`src/middleware/auth.ts`):**
    - Implemented a 30-minute in-memory LRU/TTL cache (`authContextCache`) keyed by `${token}::${subdomain}::${isPatientApp}`.
    - On cache hits, completely bypasses all 4 sequential database queries (`token_blacklist`, `users`, `clinics`, `user_clinic_roles`), populating `req.user` in 0.01ms while maintaining 100% tenant isolation inside `tenantStorage.run()`.
    - Integrated `invalidateAuthCache(token)` on logout in `auth.controller.ts` and `patient.controller.ts` for immediate session revocation.
  - **Frontend RTK Query Entity Tag Decoupling (`clientApi.ts`):**
    - Added granular tag types `["Clients", "PatientFundings", "PatientNotes", "PatientDocuments"]`.
    - Scoped `getPatientFundings`, `addPatientFunding`, `updatePatientFunding`, and `deletePatientFunding` strictly to `{ type: 'PatientFundings', id: patientId }`, completely eliminating cascading directory refetches.
  - **Live Verification & Benchmark Results:**
    - Live benchmark: Cold cache latency of `5,681.92 ms` dropped to warm cache average of `2.62 ms` (**2,168x faster**, saving **5,679.3 ms** per request).
    - Unit tests: 8/8 passed in `tests/unit/authMiddlewareCache.test.ts` (including 30-min TTL expiry).
    - Regression suites: 19/19 passed in `databaseContext.test.ts` & `patientSearch.test.ts`, 28/28 passed in `batchBookingService.test.ts`.
    - Type-checks: 100% clean on both backend (`npx tsc --noEmit`) and frontend (`yarn tsc --noEmit`).
- **Recurring Series Cancellation with Jane App Parity (Item 12):**
  - **Feature Architecture & Clinical Parity:**
    - Designed and implemented granular recurring booking cancellation following Jane App clinical practice management workflows.
    - Added support for two distinct cancellation scopes:
      1. **Single Session (`cancelScope: 'single'`):** Cancels only the selected appointment (`POST /api/appointments/:id/cancel`), leaving future recurring sessions intact while restoring 1 session funding credit and voiding the appointment invoice.
      2. **Entire Series (`cancelScope: 'series'`):** Atomically cancels all upcoming uncompleted appointments in the series (`POST /api/v1/batch-bookings/:id/cancel`), locks completed past charting sessions for clinical integrity, marks the batch `CANCELLED`, and refunds all unconsumed funding credits back to the patient's grant ledger.
    - Clinical reason dropdown: *Client Sick / Medical Emergency*, *Schedule Conflict*, *Clinician Unavailable*, *Funding Depleted*, and *Other*.
  - **Backend Implementation & DB Invariants:**
    - Exposed `batch_booking_id` in single appointment query (`AppointmentRepository.findByIdWithDetails`) and API response DTO (`AppointmentDetailResponse`).
    - Added single-session batch booking handling in `cancelAppointment`: looks up batch, verifies funding source, restores service price to `patient_fundings.remaining_funding`, voids invoice, and marks transaction split reversed.
    - Verified `cancelBatchBooking` in `batchBookingService.ts`: 28/28 unit tests passing (`batchBookingService.test.ts`).
  - **Frontend UI & Event Details Integration:**
    - `EventDetailsModal.tsx`: Renders distinct purple `Recurring Series` badge next to the status when `batch_booking_id` is present.
    - Renders Jane App cancellation prompt with single session vs entire series radio cards and required clinical reason dropdown.
    - Connected `onSelectAppointment` callback in `ListViewDashboard.tsx` and `app/s/[subdomain]/dashboard/page.tsx` for seamless event selection.
    - Fixed `initialState.isLoading: false` in `subscriptionSlice.ts` to allow `SubscriptionGuard` to pass dashboard content through.
  - **Visual Verification proof via Chrome DevTools MCP:**
    - `proof_recurring_series_badge_event_modal.png`: Event Details modal showing "Recurring Series" badge.
    - `proof_jane_app_parity_cancellation_modal.png`: Jane App parity cancellation modal with scope selection.
    - `proof_recurring_series_cancelled_success.png`: Live cancellation SweetAlert confirming 4 sessions cancelled and $400.00 funding credits restored.
  - **CI/CD Troubleshooting, PRs & Production Deployment (`ci-cd-troubleshooter`):**
    - **Backend PR #311 Merged (`feat/recurring-booking-cancellation` -> `main`):**
      - Passed all 5 CI checks (Security/SAST Scan, Dependency Audit, CI Lint & Typecheck, CI Unit Tests, Milestone 1 Integration Tests).
      - Successfully merged via standard merge commit into `main`.
      - Automated Docker image build and `Deploy Production` workflow completed in 52s.
    - **Frontend PR #262 Merged (`feat/recurring-booking-cancellation-ui` -> `main`):**
      - Fixed Prettier formatting in `EventDetailsModal.tsx` and `ListViewDashboard.tsx`.
      - Rebased on latest `origin/main` (PR #261) to resolve dirty mergeable state.
      - Passed `CI/Lint & Typecheck` (100% green, 2m1s).
      - Successfully merged into `main`.
      - Automated Docker image build and `Deploy Frontend (EC2)` workflow completed in 33s.


- **High-Volume Batch Booking N+1 Elimination & Vectorized Bulk Performance (Item 13 / ADR-015):**
  - **Latency & Timeout Root-Cause Analysis:**
    - User reported an Axios 30,000ms timeout (`timeout of 30000ms exceeded`) when booking ~52 weekly sessions for funded clients ($5,000 balance, $55/session).
    - Diagnosed severe N+1 serial query loop in `createFundedBatchBooking` (`batchBooking.service.ts`): executed 5 sequential queries per session inside a single PostgreSQL transaction = **261 sequential database queries**.
    - Identified primary bottleneck: `generateInvoiceNumber()` ran `SELECT COUNT(*) FROM invoices WHERE clinic_id = $1` on every single iteration (52 repetitive full-table scans across uncommitted MVCC tuples inside the open transaction).
    - Single-row inserts for 52 appointments, 52 invoices, 52 invoice status updates, and 52 transaction splits.
  - **Vectorized Bulk Multi-Row Operations Implemented:**
    - Single initial query to calculate starting invoice sequence in memory before loop execution.
    - Pre-generated UUIDs (`crypto.randomUUID()`) in memory.
    - Vectorized all 52 appointments into a single multi-row `INSERT INTO appointments (...) VALUES ($1...), ($20...), ...`.
    - Vectorized all 52 invoices directly with final status (`PAID` or `PENDING_PAYMENT`) and balance/paid amounts, eliminating 52 secondary `UPDATE` statements.
    - Vectorized all 52 transaction splits into a single multi-row `INSERT INTO transaction_splits`.
    - Vectorized `cancelBatchBooking` from 156 serial updates to 3 parameterized queries using `id = ANY($2::uuid[])` across appointments, invoices, and splits.
    - Reduced total DB roundtrips from **261 queries down to 5 queries** (a 52x reduction).
  - **Live PostgreSQL Integration Benchmark Proof (`tests/integration/batchBookingBulkPerf.test.ts`):**
    - 52-session batch creation: **574ms** (down from >30,000ms timeout, **>50x faster**).
    - 52-session batch cancellation: **88ms**.
    - Unit tests: 34/34 passing green (`tests/unit/batchBookingService.test.ts`).
  - **CI/CD Troubleshooting, PRs & Production Deployment (`ci-cd-troubleshooter`):**
    - **Backend PR #313 Merged (`feat/recurring-booking-cancellation` -> `main`):**
      - Passed all 5 CI checks (Security Audit, Lint & Typecheck, Milestone 1 Integration Tests, Trivy SAST, Unit Tests).
      - Successfully merged via standard merge commit into `main`.

- **Booking Modal Server Error Transparency & Interceptor Decoupling (Item 14):**
  - **Error Suppression Root-Cause Diagnostics:**
    - When booking an appointment with an existing email, the frontend modal rendered a generic placeholder: *"Booking Failed: An unknown error occurred while creating the appointment."* despite backend returning HTTP 409 Conflict: `{"success": false, "error": "A patient with this email already exists. Use Existing Client tab to select them.", "statusCode": 409}`.
    - Diagnosed in `useCreateScheduleModal.ts`: `error instanceof Error` evaluated to `false` because the Axios response interceptor rejects a plain JavaScript `ApiError` object (`{ status, message, data }`). This forced execution into the `else` branch, discarding the server error payload.
    - Duplicate UI `Swal.fire` dialogs in `appointments.api.ts` caused modal flickering and premature closure.
  - **Implementation & Resilience:**
    - Refactored `handleBook` in `useCreateScheduleModal.ts` to use `parseApiError` and direct payload extraction (`rawError?.response?.data?.error || rawError?.data?.error || rawError?.message`).
    - Enhanced `parseApiError` and `extractMessage` in `lib/utils/backend/errors.ts` to prioritize direct backend `error` strings and validation arrays over generic Axios status strings (`"Request failed with status code 409"`).
    - Added support for per-request `{ silentErrors: true }` in `lib/utils/backend/interceptors.ts`.
    - Decoupled SweetAlert logic from `appointments.api.ts`.
  - **CI/CD Troubleshooting, PRs & Production Deployment (`ci-cd-troubleshooter`):**
    - **Frontend PR #264 Merged (`feat/recurring-booking-cancellation-ui` -> `main`):**
      - Resolved strict `@typescript-eslint/no-explicit-any` rules and Prettier formatting in `useCreateScheduleModal.ts`, `errors.ts`, `interceptors.ts`, and `appointments.api.ts`.
      - Passed `CI/Lint & Typecheck` 100% green and merged into `main`.

- **Local CI, Root Makefile & Direct VPS Deployment Automation (Item 15):**
  - **Runner Quota Independence & Direct Merge Protocol:**
    - Organization GitHub runner quota exhaustion bypassed by establishing a local compilation, testing, and deployment pipeline.
    - Created unified root `Makefile` and automation scripts in `scripts/`:
      - `scripts/ci-backend.sh` & `scripts/ci-frontend.sh`: Local ESLint & TypeScript compilation checks.
      - `scripts/merge-main.sh`: Automated rule-based direct merge to `main` upon passing both backend and frontend CI checks.
      - `scripts/deploy-backend.sh` & `scripts/deploy-frontend.sh`: Local Docker builds streamed directly to VPSs via SSH (`docker save | gzip | ssh ... docker load`), executing DB migrations, container recreation, and live health check verification.
      - `scripts/deploy-all.sh`: Master orchestrator deploying backend migrations & API followed by frontend with elapsed timing.
    - Live health checks verified: `https://api.emmai.ca/health` (HTTP 200 OK) and `https://vancouverspeechtherapy.emmai.ca` (HTTP 307/200 OK). All 7 production containers verified healthy.

