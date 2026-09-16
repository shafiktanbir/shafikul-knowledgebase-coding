# ADR-009: Owner-Only Email Update + FusionAuth SSO Sync

**Date:** 2026-09-15  
**Status:** Accepted  
**Deciders:** Shafikul Islam  
**Related:** ADR-004 (Dynamic RBAC), ADR-005 (Jane Migration Engine)

---

## Context

The clinic app uses FusionAuth as its centralized SSO/identity provider. During login,
`loginWithFusionAuthCode()` fetches the email from FusionAuth's `/oauth2/userinfo` endpoint
and uses it as the lookup key against our PostgreSQL `users` table:

```
findByEmailAndClinic("email_from_fusionauth", clinicId)
```

**The problem discovered (2026-09-15):** When the clinic owner updated a staff member's
email via `PUT /api/users/:id/profile`, the code updated only the local PostgreSQL record
but did NOT call the FusionAuth Admin API to update the corresponding identity. This caused:

- FusionAuth: `old@email.com` (unchanged)
- PostgreSQL: `new@email.com` (updated)
- Next login by the affected staff: FusionAuth sends `old@email.com` → DB lookup fails → **HTTP 403 "not registered" — user locked out**

---

## Decision

### 1. Owner-Only Email Gate (Hard Role Gate — Not a Permission Override)

Email updates are gated by `roleName === 'owner'` at the controller level. This is a
**non-configurable hard gate**, not a CASL permission that admins can be granted via
`user_permission_overrides`. The rationale: email is the login identity anchor; allowing
admins to change it without FusionAuth sync awareness creates a login lockout attack vector.

### 2. Atomic FA-First Email Sync Pattern

The email update sequence in `user.controller.ts` is now atomic:

1. **PATCH FusionAuth** `/api/user/:userId` with `{ user: { email: newEmail } }` — **FIRST**
2. If FA fails → abort with HTTP 502. PostgreSQL **unchanged**. User can retry.
3. If FA succeeds → **UPDATE PostgreSQL** `users.email`
4. If PostgreSQL fails → best-effort revert FA email (`revertUserEmail()`). Log split-brain if revert also fails.

### 3. New `fusionAuthClient.ts` Service

A dedicated FusionAuth Admin API client (`src/services/fusionAuthClient.ts`) with:
- `updateUserEmail(userId, newEmail)` — PATCH FA user
- `revertUserEmail(userId, originalEmail)` — best-effort rollback
- Graceful no-op if FusionAuth is unconfigured (dev environments)

### 4. Migration Route Permission Tightening

Jane migration `execute` and `rollback` endpoints upgraded from `requireRole('owner', 'admin')`
to `requireRole('owner')` only. These endpoints write email fields to user records during
staff upsert, which must be owner-gated for the same reason as the profile update path.

Defense-in-depth assertions added inside `executeMigration()` and `rollback()` controller methods.

### 5. USERS_UPDATE_EMAIL Permission

Added `USERS_UPDATE_EMAIL = 'users:update:email'` to `PatientPermission` enum. Owner-only
by default (`owner: Object.values(PatientPermission)`). Not grantable via overrides to
other roles. Registered in module entries for RBAC UI visibility.

---

## Consequences

### Positive
- Staff can no longer be locked out by owner email changes
- Clear split-brain detection via structured `logger.error` output
- All email changes are audit-logged with actor/target/from/to fields
- Admin cannot trigger email-bearing migration writes

### Negative / Tradeoffs
- Email change has a dependency on FusionAuth availability. If FA is down, the owner
  cannot change emails until FA is restored. This is acceptable — the alternative (silent
  out-of-sync) is worse.
- If a split-brain occurs (FA updated, DB update fails, revert fails), manual correction
  in the FusionAuth admin console is required. This is logged at ERROR level.

### Files Changed
| File | Change |
|---|---|
| `src/services/fusionAuthClient.ts` | **NEW** — FusionAuth Admin API client |
| `src/controllers/user.controller.ts` | Atomic FA-first email sync, audit log |
| `src/permissions/patients.permissions.ts` | `USERS_UPDATE_EMAIL` enum entry |
| `src/routes/v1/dataMigration.routes.ts` | execute + rollback → owner-only |
| `src/controllers/dataMigration.controller.ts` | Defense-in-depth owner assertions |
| `components/features/data-migration/ActiveRollbackCard.tsx` | `isOwner` prop gate |
| `app/.../data-migration/DataMigrationClient.tsx` | `isOwner` derived, passed down |
