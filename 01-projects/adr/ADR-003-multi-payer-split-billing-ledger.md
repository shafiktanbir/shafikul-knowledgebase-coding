# ADR-003: Multi-Payer Split Billing & Transaction Split Ledger

**Date:** September 2026  
**Status:** Accepted (Implemented in EPIC-08, Migrations `00101` & `00102`)  
**Context Source:** `clinic-app/ai-toolkit/funding-and-insurance-epic.md` & `invoice-lifecycle-state-machine-v1.md`  

---

## 1. Context & Problem Statement
Therapy clinics (Speech, OT, Physio) frequently bill appointments across multiple payers simultaneously:
e.g. A $150 appointment is split into **$100 covered by Autism Block Funding**, **$30 covered by Private Insurance**, and **$20 paid by Patient Credit Card**. Legacy systems with a single `payments` table could not model multi-payer adjudication or partial refunds.

---

## 2. Decision Outcome
We introduced a **Mandatory 1:1 Invoicing Architecture** with **1:N Multi-Payer Transaction Splits**:

```sql
-- Mandatory Invoice bound 1:1 to appointment
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID NOT NULL UNIQUE REFERENCES appointments(id),
    clinic_id UUID NOT NULL REFERENCES clinics(id),
    patient_id UUID NOT NULL REFERENCES patients(id),
    total_amount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    total_covered_by_funding NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    total_patient_responsibility NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    balance_due NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    invoice_status VARCHAR(50) NOT NULL DEFAULT 'UNPAID'
);

-- 1:N Transaction Splits for multi-payer adjudication
CREATE TABLE transaction_splits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID NOT NULL REFERENCES invoices(id),
    appointment_id UUID NOT NULL REFERENCES appointments(id),
    patient_funding_id UUID REFERENCES patient_fundings(id),
    payer_type VARCHAR(50) NOT NULL, -- 'insurance', 'credit_card', 'cash', 'e_transfer'
    covered_amount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    payment_status VARCHAR(50) NOT NULL DEFAULT 'pending'
);
```

---

## 3. Consequences & Benefits
- **Audit-Ready Accounts Receivable:** Tracks exact claims, adjudication rejections, and copay balances per payer.
- **Partial Refund Support:** Allows targeting refunds to specific transaction splits (e.g. refunding patient card without touching insurance payouts).
