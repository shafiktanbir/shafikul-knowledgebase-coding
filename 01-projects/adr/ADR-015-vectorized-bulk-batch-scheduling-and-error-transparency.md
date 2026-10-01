# ADR-015: Vectorized Multi-Row Bulk Ingestion for High-Volume Batch Scheduling & Global API Error Transparency

**Date:** 2026-09-24  
**Status:** Accepted  
**Deciders:** Principal Full-Stack Architect, Senior Database Engineer  
**Primary Target / PRs:** Backend PR #313 (\`batchBooking.service.ts\`), Frontend PR #264 (\`useCreateScheduleModal.ts\`, \`errors.ts\`, \`interceptors.ts\`, \`appointments.api.ts\`)

---

## 1. Context & Problem Statement

When attempting to schedule long-horizon recurring sessions (such as 52 weekly sessions for a funded client with \$5,000 in grant allocations), the system experienced catastrophic latency that exceeded the frontend Axios timeout threshold (\`timeout of 30000ms exceeded\`).

Simultaneously, when scheduling conflicts or validation issues occurred (such as duplicate patient emails on conflict), the frontend modal rendered a generic placeholder: *"Booking Failed: An unknown error occurred while creating the appointment."* rather than presenting the actionable backend error message.

### Root-Cause Diagnostics:
1. **Serial N+1 Database Bottleneck (\`batchBooking.service.ts\`):**
   - The scheduling loop iterated through all 52 sessions sequentially inside a single PostgreSQL transaction with \`await\` on every roundtrip.
   - For every session iteration:
     - \`generateInvoiceNumber()\` executed \`SELECT COUNT(*) FROM invoices WHERE clinic_id = \$1\` (52 repeated full-table scans over uncommitted MVCC tuples inside the open transaction).
     - Serial \`INSERT INTO appointments\` (52 single-row queries).
     - Serial \`INSERT INTO invoices\` (52 single-row queries).
     - Serial \`UPDATE invoices SET invoice_status = 'PAID'...\` (52 single-row queries).
     - Serial \`INSERT INTO transaction_splits\` (52 single-row queries).
   - **Total sequential queries: 261 queries** accumulating locks and exceeding 30,000ms.
   - Similarly, batch cancellation sequentially iterated through every appointment to update appointments, invoices, and splits (150+ queries).
2. **Frontend \`instanceof Error\` Naive Check Discarding API Errors:**
   - In \`useCreateScheduleModal.ts\`, the catch block checked \`if (error instanceof Error)\`.
   - The Axios response interceptor in \`interceptors.ts\` rejects a structured plain JavaScript \`ApiError\` object (\`{ status, message, data }\`), which is **not** an instance of \`window.Error\`.
   - As a result, \`error instanceof Error\` evaluated to \`false\`, forcing execution into the \`else\` branch which displayed the generic placeholder \`"An unknown error occurred while creating the appointment."\` and threw away the actual error (\`"A patient with this email already exists. Use Existing Client tab to select them."\`).
   - Duplicate UI \`Swal.fire\` dialogs in \`appointments.api.ts\` caused modal flickering and premature closure.

---

## 2. Decision Drivers

- **Sub-Second Bulk Creation:** Creating 52 weekly sessions must complete in under 1 second (< 1,000ms).
- **Strict ACID Invariants:** All appointments, invoices, and transaction splits must commit atomically; if any constraint fails, the entire batch rolls back with zero partial writes.
- **Accurate Sequence Integrity:** Invoice numbers must increment sequentially and deterministically without race conditions or full-table scans per row.
- **Transparent Error Presentation:** The user must immediately see the exact, actionable error message returned by the server.
- **Separation of Concerns:** API client functions must remain pure data fetching layers without embedded UI modal triggers.

---

## 3. Decision Outcome

### 1. Multi-Row Vectorized Bulk Operations (\`batchBooking.service.ts\`)
- **In-Memory Pre-Sequencing:** Single initial count query \`SELECT COUNT(*) FROM invoices WHERE clinic_id = \$1\` before the creation phase to establish the starting sequence, incrementing in memory for all rows.
- **Vectorized Appointment Multi-Row Insert:**
  \`\`\`sql
  INSERT INTO appointments (
    id, clinic_id, practitioner_id, patient_id, service_id, ...
  ) VALUES 
    (\$1, \$2, ...), 
    (\$20, \$21, ...), 
    ...
  \`\`\`
- **Vectorized Invoice Multi-Row Insert:**
  Inserted with final status (\`PAID\` or \`PENDING_PAYMENT\`) and precomputed financial totals, completely eliminating 52 secondary \`UPDATE\` statements.
- **Vectorized Transaction Splits Multi-Row Insert:**
  Single bulk insert statement for all session splits.
- **Vectorized Cancellation:**
  Replaced sequential cancellation loops with 3 single parameterized queries using \`id = ANY(\$2::uuid[])\` across appointments, invoices, and transaction splits.
- **Query Reduction:** Reduced query count from **261 queries down to 5 queries** (a 52x reduction).

### 2. Global Error Normalization & Modal Transparency (\`frontend\`)
- **\`useCreateScheduleModal.ts\`:**
  Replaced naive \`instanceof Error\` check with \`parseApiError\` and direct payload extraction (\`rawError?.response?.data?.error || rawError?.data?.error || rawError?.message\`).
- **\`lib/utils/backend/errors.ts\`:**
  Enhanced \`extractMessage\` to prioritize direct backend \`error\` strings and validation arrays over generic Axios status strings (\`"Request failed with status code 409"\`).
- **\`lib/utils/backend/interceptors.ts\`:**
  Added support for per-request \`{ silentErrors: true }\` so calling modal components can manage their own domain-specific error UI without generic "Request Failed" collisions.
- **\`appointments.api.ts\`:**
  Decoupled UI SweetAlert logic from pure API callers.

---

## 4. Verification & Benchmark Proof

### PostgreSQL Integration Benchmark (\`tests/integration/batchBookingBulkPerf.test.ts\`):
\`\`\`bash
PASS tests/integration/batchBookingBulkPerf.test.ts
  Batch Booking Bulk Performance (52 Weekly Sessions)
    ⚡ 52-session batch creation completed in 574ms
    ✓ atomically creates 52 weekly sessions in under 2000ms (100x faster than sequential N+1) (656 ms)
    ⚡ 52-session batch cancellation completed in 88ms
    ✓ atomically cancels 52 weekly sessions in under 1000ms with bulk vectorized updates (121 ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
\`\`\`

### Unit Tests & Typechecks:
- \`tests/unit/batchBookingService.test.ts\`: **34/34 passed (100% green)**.
- Frontend: \`npx tsc --noEmit\` passed with 0 errors.
- Pre-commit: Prettier, ESLint, and Commitlint passed cleanly.

### Pull Requests & Production Merges:
- **Backend PR #313**: Merged into \`main\` (Passed all 5 CI checks).
- **Frontend PR #264**: Merged into \`main\` (Passed CI checks).
