# ADR-011: Group & Funded Batch Bookings with Backup Credit Card Guarantee

**Date:** 2026-09-23  
**Status:** Accepted  
**Deciders:** Senior Full Stack Architect, Practice Management Lead  
**Primary Target / Migration:** `clinic-booking-app-backend` (`batchBooking.service.ts`), `clinic-booking-app-frontend` (`BatchBookingModal.tsx`), Migration `00131_add_max_advance_booking_days_to_clinics.js`

---

## 1. Context & Problem Statement
In multidisciplinary clinics (e.g., Speech-Language Pathology, Occupational Therapy, Physiotherapy), pediatric and rehabilitation patients receive recurring therapy allocations from government or private grants (MCFD Autism Funding, Jordan's Principle, Pacific Blue Cross). Patients need to block out recurring weekly therapy time-slots across multiple months.
However, two critical failure modes existed:
1. **Unfunded / Zero-Funded Booking Overhang:** When funding was exhausted or absent, booking recurring sessions in advance risked uncollected accounts receivable (AR).
2. **Booking Deadlock:** Patients with active grant programs or cards on file could not schedule beyond immediate balances without clinic authorization, leading to slot loss and administrative friction.

---

## 2. Decision Drivers
- **Financial Risk Protection:** Guarantee that zero-funded or funding-exceeded sessions are backed by a valid credit card on file that is automatically charged upon completion.
- **Configurable Horizon:** Allow clinic administrators to configure advance scheduling limits (`max_advance_booking_days`) in Clinic Settings > Preferences (e.g., 30, 45, or 60 days).
- **Split Billing Integration:** Atomically allocate funded portions to `patient_fundings` (marked `PAID` via grant claim) and overage/card-guaranteed sessions to `transaction_splits` (marked `PENDING_PAYMENT` for auto-charge).
- **Sub-Second Preview Calculation:** Eliminate sequential N+1 database queries when previewing 50+ prospective weekly dates by using single-query lookahead windows and in-memory conflict detection.

---

## 3. Decision Outcome
Chosen Solution: **Two-Tier Balance & Card Guarantee Engine with Single-Window Lookahead**.

### Architectural Components:
1. **Clinic Advance Horizon Column:** Added `max_advance_booking_days INT DEFAULT 30 CHECK (max_advance_booking_days BETWEEN 1 AND 365)` to `clinics` table.
2. **Card Detection & Auto-Guarantor:**
   - Detects saved payment cards in both `patient_payment_methods` and `patients.payment_card` JSONB.
   - For zero-funded patients with a saved card, automatically enables the backup card guarantee and unlocks recurring bookings up to `clinicMaxAdvanceDays`.
3. **Optimized Lookahead Query:** Pre-fetches all practitioner appointments within the multi-week batch window in a single indexed query (`appointment_start_at < $4 AND appointment_end_at > $3`), resolving prospective date conflicts in-memory in under 20ms (down from 30+ seconds).
4. **Atomic Multi-Session Reservation:** Wrapped inside PostgreSQL `transaction()`, creating appointment records, funding deductions (`remaining_funding = remaining_funding - cost`), and invoice splits with full ACID guarantees.

---

## 4. Consequences & Trade-offs
- **Positive:** Eliminates scheduling overages; enables frictionless multi-month batch scheduling for grant patients; provides bulletproof credit card guarantee for unfunded sessions.
- **Positive:** Fast preview (<50ms) across 52 prospective weekly dates without database timeouts.
- **Negative:** Non-funded sessions remain in `PENDING_PAYMENT` until post-session completion triggers the Stripe automated charge workflow.
