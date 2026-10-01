# ADR-012: Patient Funding Lifecycle Visibility & Backup Card Checking Resilience

**Date:** 2026-09-24  
**Status:** Accepted  
**Deciders:** Senior Full Stack Practice Management Architect, Clinical Systems Lead  
**Primary Target / Migration:** `BatchBookingModal.tsx`, `clientApi.ts`, `invoice.service.ts`, `batchBooking.service.ts`

---

## 1. Context & Problem Statement
During operational clinic testing on Vancouver Speech Therapy, two high-priority UX and state resolution flaws were uncovered in the Scheduled Booking workflow:

1. **Approved Funding Source (Grant / Government) Vanishing Issue:**
   - Clinic staff created an approved funding source for a patient (`Abdul Kader`), allocating a $5,000 grant (`funding_name: "jordan"`).
   - In `AddFundingSourceDrawer.tsx`, newly registered funding sources default to `signed_status = "not_signed"` pending patient/guardian signature or verification.
   - In `BatchBookingModal.tsx`, the UI condition `hasNeitherFundingNorCard` was evaluated *before* checking `fundingSources.length > 0`. Because `hasFundingCredits` required `signed_status === 'confirmed' || signed_status === 'signed'`, `hasFundingCredits` was `false`.
   - Because the patient had no card on file, the modal falsely triggered a red alert box: *"Booking Blocked: No Funding or Saved Card. No funding source or saved card on file"*.
   - This completely suppressed and hid the newly created funding source from clinic staff, misleading them into believing the record did not exist.

2. **Card Checking & Guarantee Verification for Zero-Funded Patients:**
   - Need for seamless detection and verification of on-file payment cards (`patient_payment_methods` and Stripe JSONB) for clients without grant funding.
   - For zero-funded patients with a saved card, the modal must automatically activate the **Backup Credit Card Guarantee**, calculate extended recurring sessions up to the clinic's configured horizon (e.g., 30 days), and enable instant booking.

---

## 2. Decision Drivers
- **Zero Hidden Records Principle:** Clinic staff must never have valid on-file funding sources hidden or masked by secondary business rule gates. All registered funding sources must be visible in the selection grid.
- **In-Modal Lifecycle Advancement:** If a funding policy requires signature or approval (`signed_status = "not_signed"`), staff must have a clear visual badge (`Not Signed / Awaiting Approval`) and a one-click **"Approve & Select"** action directly within the Scheduled Booking modal without having to navigate away to the patient profile.
- **Card-Backed Zero-Funding Parity:** Patients with no funding but with a valid saved payment card on file must receive an informative amber guidance banner (*"No Active Funding Sources — Backup Card Available"*), auto-engage the card guarantee toggle, and successfully preview and book recurring sessions up to the clinic's configurable horizon.

---

## 3. Decision Outcome
Chosen Solution: **Hierarchical Funding Evaluation with In-Modal Approval Mutation & Dual-Card Sourcing**.

### 1. UI Evaluation Hierarchy in `BatchBookingModal.tsx`:
```tsx
// 1. Loading state
{fundingsLoading ? (
  <LoadingSkeleton />
) : fundingSources.length === 0 ? (
  // 2. Zero funding on file: Check for saved credit card
  hasCardOnFile ? (
    <AmberBanner title="No Active Funding Sources — Backup Card Available">
      Extended recurring sessions can be scheduled using Backup Credit Card Guarantee.
    </AmberBanner>
  ) : (
    <RedBanner title="Booking Blocked: No Funding or Saved Card">
      Please add a payment card or funding source to continue.
    </RedBanner>
  )
) : (
  // 3. Funding on file: ALWAYS render the full funding source grid
  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
    {fundingSources.map(funding => (
      <FundingCard key={funding.id} funding={funding} ... />
    ))}
  </div>
)}
```

### 2. In-Modal Approval Mutation:
Integrated `useUpdatePatientFundingMutation` from `@/lib/features/client/clientApi`. When an unsigned funding source is encountered:
- Displays amber badge `Not Signed`.
- Renders `[Approve & Select]` action button.
- Updates database record via `PUT /api/v1/patients/:patientId/fundings/:id` with `{ signed_status: 'confirmed' }`, invalidates the RTK Query cache tag `['Clients']`, and auto-selects the funding source to immediately compute batch session previews.

### 3. Card Checking & Auto-Guarantee Pipeline:
- Evaluates `paymentMethodsResponse` from `GET /api/v1/invoices/payment-methods/:patientId` (checking `patient_payment_methods` and `patients.payment_card`).
- If `hasCardOnFile && !hasFundingCredits`, auto-toggles `useBackupCard = true`.
- Renders green badge: `Card on File: [Brand] •••• [last4]`.
- Displays advance limit insight (`Advance Limit Active: Bookings permitted up to X days in advance`).
- Previews and creates 100% card-guaranteed appointments and `PENDING_PAYMENT` transaction splits.

---

## 4. Verification & Evidence
1. **Abdul Kader ($5,000 Jordan's Principle Grant):**
   - Verified funding source `jordan` renders with Emerald `CONFIRMED` badge.
   - Automatically computed and previewed **50 weekly sessions** ($5,000 balance).
   - Visual Evidence: `proof_abdul_kader_funding_confirmed_and_preview.png`.
2. **Client 1: Maya GrantFunded ($3,000 Autism Funding Program):**
   - Created test patient `Maya GrantFunded` with $3,000 active grant.
   - Selected in modal; rendered `Autism Funding Program` card with policy `BC-AUT-8821` and `CONFIRMED` badge.
   - Visual Evidence: `proof_maya_grant_funded_client.png`.
3. **Client 2: Leo CardBacked (Visa Ending in 4242, Zero Funding):**
   - Created test patient `Leo CardBacked` with Visa ending in 4242 and 0 funding.
   - Selected in modal; displayed amber banner *"No Active Funding Sources — Backup Card Available"*.
   - Backup Credit Card Guarantee auto-enabled with `Card on File: VISA •••• 4242` badge.
   - Computed batch session preview up to 30-day clinic limit.
   - Confirmed SweetAlert2 modal *"Confirm Batch Booking (Card Guaranteed)?"* with note: *"Backup card (VISA ending in 4242) will be charged automatically after each non-funded session is completed."*
   - Successfully created appointment on calendar and `PENDING_PAYMENT` split in direct database.
   - Visual Evidence:
     - `proof_leo_card_backed_top_banner.png`
     - `proof_leo_card_backed_guarantee_and_preview.png`
     - `proof_leo_confirm_card_guaranteed_modal.png`
     - `proof_leo_batch_booking_created_success.png`
