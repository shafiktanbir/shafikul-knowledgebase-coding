# ADR-010: Automated Operational Lifecycle & Visual Testing Harness

**Date:** 2026-09-20 / 2026-09-21  
**Status:** Accepted  
**Deciders:** Shafikul Islam  
**Related:** ADR-001 (Multi-Tenant User Clinic Roles), ADR-003 (Multi-Payer Split Billing), ADR-004 (Dynamic RBAC)

---

## Context

The multi-tenant Clinic Booking Platform (`clinic-booking-app`) requires end-to-end operational verification spanning the entire clinical lifecycle. Prior to this decision, tests were fragmented into isolated unit tests and ad-hoc integration checks, lacking a cohesive end-to-end operational harness capable of validating:
1. Dynamic clinic onboarding and isolated tenant provisioning.
2. Tenant routing and custom branding resolution.
3. Branch locations and treatment catalog configuration.
4. Administrative staff and practitioner invitation with shift/working hours scheduling.
5. Internal administrative appointment scheduling (bypassing public patient booking).
6. Practitioner daily calendar management and appointment state transitions (`booked` ➔ `in_progress` ➔ `completed`).
7. Clinical charting with rich SOAP notes, cryptographic SHA-256 digital signatures, and tamper-evident sealing.
8. Multi-payer split billing, tax calculations, offline payment logging, and balance reconciliation to $0.00.
9. Cross-tenant isolation boundaries (`x-clinic-subdomain`) and CASL RBAC privilege escalation prevention.

A unified, zero-mock testing harness was needed that operates cleanly in local development (`localhost:3000`, `127.0.0.1:8000`) and CI environments with visual milestone artifact capture.

---

## Decision

### 1. Dedicated E2E Visual Testing Sub-Package
Established an isolated test harness in `clinic-booking-app-frontend/e2e-visual-testing/` with its own configuration (`playwright.config.ts`), test runner (`run-lifecycle-tests.sh`), specs (`specs/01-clinic-lifecycle.spec.ts`), and fixtures (`fixtures/`).

- **Sequential Execution**: Strictly single-worker (`workers: 1`, `fullyParallel: false`) to reflect the real-world operational chronology of a medical practice.
- **Dual-Mode Capability**: Supports headless CI batch execution (average duration ~27s) and interactive headed browser execution (`--headed`) for debugging and demonstration.
- **Artifact Segregation**: Set Playwright internal trace output to `reports/test-artifacts/` and milestone screenshots to `reports/artifacts/` to prevent Playwright's default directory clearing from purging milestone images.

### 2. Direct Administrative Booking Model (No Patient Self-Booking)
In clinical practice management, appointments are predominantly coordinated and scheduled internally by clinic administrators. The harness enforces direct administrative scheduling via `POST /api/appointments`, validating that clinic staff and doctors are fully onboarded with credentials and scheduled working hours **prior** to any appointment creation.

### 3. Cryptographic SOAP Note Signing & Immutability Enforcement
Clinical chart notes authored by practitioners are sealed with a cryptographic SHA-256 digital signature:
$$\text{hash} = \text{SHA256}(\text{patientId} + \text{practitionerId} + \text{SOAP\_content} + \text{timestamp})$$
Once signed and locked (`isLocked: true`, `status: 'signed'`), the backend (`PatientController`) strictly rejects any subsequent modification or deletion attempts with **HTTP 403 Forbidden**, satisfying PIPEDA and HIPAA medical record integrity regulations.

### 4. Split Billing Ledger Reconciliation & Idempotent Finalization
Invoices enforce exact balance reconciliation:
- Evaluates total charge with applicable taxes ($140.00 base + 5% GST $7.00 = $147.00 CAD).
- Allocates exact split payments across distinct payment methods (e.g. $100.00 credit card + $47.00 cash copay).
- Finalization (`POST /api/v1/invoices/:id/finalize`) is idempotent for invoices already in `FINALIZED` or `PAID` status.
- Offline payment logging (`POST /api/v1/invoices/:id/offline-payment`) accepts `credit_card`, `card`, `cash`, `cheque`, and `e_transfer`, strictly reducing balance due to $0.00.
- Foreign key constraints in audit logs are guarded with UUID sanitization (`validUserId = userId && validateUUID(userId) ? userId : null`).

### 5. Multi-Tenant Isolation & CASL Privilege Guardrails
All tenant queries enforce strict boundary checks:
- Authenticated tokens from Tenant A submitted with foreign clinic headers (`x-clinic-subdomain: rogue`) fail closed with **HTTP 403 Forbidden**.
- Cross-tenant resource injections (e.g., branch creation under foreign tenant) are rejected with **HTTP 403**.
- Unprivileged patient tokens attempting administrative user invitations fail closed with **HTTP 403 Forbidden** via CASL RBAC middleware.

### 6. Dynamic State Bootstrapping for Isolated Phase Runs
To enable rapid testing and debugging of individual phases (`./run-lifecycle-tests.sh --phase <1-9>`), the test harness implements `ensurePhaseBootstrap(targetPhase, request)`. This automatically discovers or provisions baseline clinic context, owner JWT tokens, branches, services, and appointments if the phase is executed in isolation.

---

## Consequences

### Positive
- **100% Pass Rate**: Entire 9-phase operational practice lifecycle passes cleanly in 27.6s (exit code 0).
- **Visual Verifiability**: 9 milestone PNG screenshots (>31 KB each) prove visual rendering across each stage of the practice workflow.
- **Zero Mock Shortcuts**: Uses authentic HMAC-SHA256 JWT tokens, genuine PostgreSQL database rows, and live API endpoints.
- **Production Defect Remediation**: Fixed appointment status permissions, offline payment method validations, audit log foreign keys, and SOAP note immutability.

### Tradeoffs / Considerations
- **Local Service Dependency**: Running the test harness requires local backend (`http://127.0.0.1:8000`) and PostgreSQL services to be active. The CLI runner includes health checks to verify availability before execution.

---

## Deliverables & Branch Inventory

| Repository | Branch | Commit | Key Changes |
| :--- | :--- | :--- | :--- |
| `clinic-booking-app-frontend` | `feat/e2e-visual-lifecycle-testing` | `400ca34` | 22 files (+4,775 / -565 lines): E2E test harness, specs, fixtures, visual PNGs, `.lintstagedrc` & ESLint ignores. |
| `clinic-booking-app-backend` | `feat/e2e-lifecycle-backend-hardening` | `d024c7b` | 13 files (+146 / -39 lines): Appointment permissions, sealed note immutability, offline payments, audit log FK safety. |
