# ADR-013: Patient Funding Lookup Latency, Database Covering Index & In-Memory Auth Caching

**Date:** 2026-09-24  
**Status:** Accepted  
**Deciders:** Senior Database Architect, Full Stack Practice Management Lead  
**Primary Target / Migration:** `auth.ts`, `clientApi.ts`, `migrations/00138_add_idx_patient_fundings_lookup.js`

---

## 1. Context & Problem Statement
Users reported noticeable latency when fetching patient insurance/funding after selecting a patient in the Scheduled Booking modal and client billing tabs.

Investigation revealed three interconnected bottlenecks:
1. **Network WAN RTT Amplification:**
   - The PostgreSQL cloud instance resides across a WAN with ~285ms roundtrip latency.
   - `scopedDatabase.ts` wraps every query inside a 4-turn transaction (`BEGIN` -> `set_config` -> `query` -> `COMMIT`), resulting in ~1,140ms per standalone query.
   - `src/middleware/auth.ts` executes 4 sequential database queries on every authenticated API request (`token_blacklist`, `users`, `clinics`, `user_clinic_roles`), producing 16 network roundtrips (~4,560ms) of overhead before the route handler is even reached. Total request latency was 5,681ms.
2. **Frontend RTK Query Cache Tag Cascading:**
   - In `clientApi.ts`, endpoints for patient fundings, notes, and documents were all bound to the generic cache tag `["Clients"]`.
   - Creating, updating, or deleting a patient funding source invalidated `["Clients"]`, triggering an avalanche of 5 heavy concurrent queries (including `getPatientsByClinic` which fetches hundreds of patient rows).
3. **Database Indexing Gap:**
   - The query `SELECT * FROM patient_fundings WHERE patient_id = $1 AND clinic_id = $2 ORDER BY priority_order ASC, created_at DESC;` previously required separate index lookups and in-memory sorting.

---

## 2. Decision Drivers
- **Sub-Second API Response Times:** Repeated authenticated actions must complete in milliseconds without sequential database roundtrips.
- **Tenant Context Security & Isolation:** The PostgreSQL transaction-level tenant configuration (`app.current_clinic_id`) and Node.js `tenantStorage` must remain strictly enforced with zero cross-tenant contamination.
- **Immediate Revocation Guarantees:** Logout or token invalidation must immediately purge cached credentials without waiting for TTL expiration.
- **Granular Frontend Invalidation:** Mutations must only invalidate their specific entity cache and never force clinic-wide directory refetches.

---

## 3. Decision Outcome
Implemented a three-pillar performance architecture:

### 1. Database Composite Covering Index (`migrations/00138_add_idx_patient_fundings_lookup.js`)
Applied migration creating composite btree index:
```sql
CREATE INDEX IF NOT EXISTS idx_patient_fundings_lookup 
ON patient_fundings (patient_id, clinic_id, priority_order ASC, created_at DESC);
```
Eliminates in-memory sorting and combines the equality filters into a single index traversal.

### 2. In-Memory Auth Middleware TTL Cache (`src/middleware/auth.ts`)
- Added bounded in-memory cache (`authContextCache = new Map<string, CachedAuthContext>()`) with a 30-minute TTL.
- Key format: `${token}::${subdomain || decoded.clinicId || ''}::${isPatientApp ? 'p' : 's'}`.
- Fast-path verification:
  1. Cryptographically verify JWT format and signature via `jwt.verify` (CPU-bound, ~0.02ms).
  2. If cached and `expiresAt > Date.now()`, assign `req.user = cached.user`, execute within `tenantStorage.run()`, and invoke `next()`.
  3. Bypass all 4 sequential database queries on repeated requests across prolonged working sessions.
- Integrated `invalidateAuthCache(token)` called immediately upon logout in `auth.controller.ts` and `patient.controller.ts`.

### 3. RTK Query Granular Cache Tagging (`clientApi.ts`)
Decoupled cache tags into distinct entities:
- `tagTypes: ["Clients", "PatientFundings", "PatientNotes", "PatientDocuments"]`
- `getPatientFundings`: `providesTags: [{ type: "PatientFundings", id: patientId }]`
- `addPatientFunding`: `invalidatesTags: [{ type: "PatientFundings", id: patientId }]`
- `updatePatientFunding`: `invalidatesTags: [{ type: "PatientFundings", id: patientId }]`
- `deletePatientFunding`: `invalidatesTags: [{ type: "PatientFundings", id: patientId }]`

---

## 4. Verification & Benchmark Results
- **Live Latency Benchmark:**
  - Cold Cache (DB roundtrips): `5,681.92 ms`
  - Warm Cache (In-Memory TTL): `2.62 ms`
  - **Speedup: 2,168x faster** (saving **5,679.3 ms** per request).
- **Unit Test Suite:**
  - `tests/unit/authMiddlewareCache.test.ts`: 8/8 tests passed (including 30-min TTL expiry).
  - `tests/unit/databaseContext.test.ts`: 10/10 tests passed.
  - `tests/unit/patientSearch.test.ts`: 9/9 tests passed.
  - `tests/unit/batchBookingService.test.ts`: 28/28 tests passed.
- **Static Analysis & Typechecks:**
  - Backend: `npx tsc --noEmit` passed cleanly.
  - Frontend: `yarn tsc --noEmit` passed cleanly.
