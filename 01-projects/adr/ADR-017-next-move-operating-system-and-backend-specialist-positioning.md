# ADR-017: Next Move Operating System & Backend Specialist Portfolio Repositioning

* **Status:** Accepted  
* **Date:** 2026-10-01  
* **Authors:** Shafikul Islam, Senior Product Engineer & Technical Consultant  
* **Context:** Personal Portfolio & Career Transition (`shafik-protfolio` / `shafiktanbir.com`)  

---

## 🎯 Context & Problem Statement

Employment termination was confirmed for October 2026 due to company-wide layoffs. To avoid total dependence on a single traditional job search, a **Dual-Track Revenue Engine** was required:
1. **Track 1:** High-value remote Senior Backend / Software Engineer job search.
2. **Track 2:** Independent technical consulting & freelancing service layer (API performance audits, database optimization, backend architecture design, monthly retainers).

The existing portfolio website (`shafiktanbir.com`) was formatted as a generalist "Fullstack Engineer" profile, diluting pricing power and conversion rates for high-intent B2B consulting leads. Additionally, there was no daily execution manual to guide daily outbound lead generation, job applications, or sales calls.

---

## 💡 Decision Drivers

* **Specialist Pricing Power:** Generalist "fullstack developers for hire" compete on low hourly rates. Backend & performance specialists command fixed-fee audit pricing ($500 – $2,500/project).
* **Frictionless Daily Execution:** Eliminating daily decision fatigue by establishing a structured `/next-move/` operating manual with 31 daily action guides.
* **Conversion Optimization:** Preserving Next.js 16 / React 19 / Tailwind v4 tech stack while restoring direct contact pathways alongside the 4-step calendar booking wizard.

---

## 🏛️ Architecture & System Changes

### 1. `/next-move/` Operating System Folder
Created a complete 19-file execution system in `/home/shafikul/Documents/coding/shafik-protfolio/next-move/`:
* `00-current-state-audit.md` — Complete 12-section portfolio audit.
* `01-strategy.md` — Dual-track transition blueprint.
* `02-positioning.md` — Specialist brand framing & anti-positioning rules.
* `03-offers.md` — Productized consulting service ladder (Performance Audit, Optimization Sprint, Custom SaaS Backend, Retainer).
* `04-target-client.md` — Ideal Customer Profile (ICP) for Bootstrapped/Seed SaaS founders and agencies.
* `05-lead-generation.md` — 11-step lead generation pipeline & qualification rules.
* `06-outreach-system.md` — Multi-channel outreach cadence and follow-up SOP.
* `07-sales-process.md` — 20-minute technical discovery call framework and 1-page proposal structure.
* `08-consulting-delivery.md` — 48-hour audit execution SOP & client onboarding protocol.
* `09-case-study-system.md` — Technical proof engine for converting engineering wins into case studies.
* `10-job-search-system.md` — Daily remote job search engine (3–5 applications/day).
* `11-financial-survival-plan.md` — Baseline survival expenses, runway calculation, and revenue target models.
* `12-metrics-dashboard.md` — Weekly KPI conversion tracking sheet.
* `13-scripts.md` — 11 word-for-word outreach, discovery, proposal, and referral scripts.
* `14-weekly-review.md` — Sunday review protocol and pivot triggers.
* `lead-sheet-template.md` & `case-study-template.md` — Standard templates.
* `NEEDS-USER-INPUT.md` — Categorized personal inputs queue (CRITICAL / HIGH / OPTIONAL).
* `daily/day-01.md` through `daily/day-31.md` — 31 concrete daily execution guides.

### 2. Live Portfolio Codebase Refactoring (`v2/`)
* **Positioning Alignment:** Updated `Sidebar.js` and `About.js` hero copy to frame expertise around **Senior Backend & Performance Specialist** (Node.js/TypeScript, Go, PostgreSQL query tuning, Redis caching, Docker, Cloud Infra).
* **Navigation Restored:** Re-enabled `Contact` tab alongside `Book` meeting wizard in `page.js` and `Navbar.js`.
* **Build Verification:** Tested Next.js production compiler (`npm run build`) — exit code 0 (`✓ Compiled successfully`).

---

## 📊 Consequences & Validation

* **Positive:**
  - Clear daily execution path eliminates guesswork.
  - Positioning as a Backend Specialist creates higher authority for remote jobs and client proposals.
  - Zero build regressions in Next.js production bundle.
* **Negative:**
  - Requires disciplined execution of daily job applications and outreach.

---

## 🔗 Related References
* Portfolio Workspace: `/home/shafikul/Documents/coding/shafik-protfolio/`
* Operating System Manual: [`/next-move/README.md`](file:///home/shafikul/Documents/coding/shafik-protfolio/next-move/README.md)
* Audit Document: [`/next-move/00-current-state-audit.md`](file:///home/shafikul/Documents/coding/shafik-protfolio/next-move/00-current-state-audit.md)
