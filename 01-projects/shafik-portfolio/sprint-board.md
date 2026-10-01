# Shafikul Islam Portfolio — Sprint Board & Task Tracker

> **Host Workspace Path:** `/home/shafikul/Documents/coding/shafik-protfolio/`  
> **Production Deployment:** Vercel (Auto-deploy on `main` push)  
> **Live Domains:** `https://shafiktanbir.com` / `https://kraken.nesohq.org/`  
> **Status:** Active / Production  

---

## 🎯 Sprint Objectives

1. **PostHog Telemetry & Session Replay:**
   - [x] Client-side initialization in `app/providers.js` with `person_profiles: 'identified_only'` and session recording (`maskAllInputs: false`).
   - [x] Route-change and tab transition tracking via `<Suspense><PostHogPageView /></Suspense>`.
   - [x] Centralized typed event schemas in `src/lib/analytics.js`.

2. **Conversion Funnels & Event Wiring:**
   - [x] 4-stage booking consultation wizard tracking in `BookMeeting.js` (`date_selected`, `time_slot_selected`, `details_submitted`, `booking_confirmed`).
   - [x] 2-stage contact form engagement tracking in `Contact.js` (`form_started`, `form_submitted`).
   - [x] Project and case study click attribution in `Portfolio.js` and `About.js`.
   - [x] Social profile and mailto click attribution in `Sidebar.js` and `Footer.js`.

3. **Production Verification & Analytics Dashboard:**
   - [x] Verify Turbopack production build (`bun run build` exit code 0).
   - [x] Push commits `0eb41fb` and `606bce6` to GitHub `main` for Vercel deployment.
   - [x] Register custom event definitions in PostHog ingestion catalog.
   - [x] Create and pin "Consultation Booking Funnel" to PostHog Product Analytics Dashboard.

---

## 📊 Sprint Task Matrix

| Task / Milestone | Category | Target File / Area | Assignee | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Telemetry Provider & Route Transitions** | Telemetry | `v2/src/app/providers.js` | Antigravity | **Completed** |
| **Centralized Analytics Helpers** | Core Lib | `v2/src/lib/analytics.js` | Antigravity | **Completed** |
| **Consultation Booking Funnel** | Conversion | `v2/src/components/sections/BookMeeting.js` | Antigravity | **Completed** |
| **Social & Contact Telemetry** | Conversion | `Sidebar.js`, `Footer.js`, `Contact.js` | Antigravity | **Completed** |
| **Production Build & Vercel Push** | Deployment | `git push origin main` | Antigravity | **Completed** |
| **PostHog Dashboard Insight Setup** | Analytics | `us.posthog.com` Dashboard | Shafikul | **Completed** |
| **Next Move Operating System** | Strategy / Manual | `/next-move/` (19 files + 31 daily plans) | Antigravity | **Completed** |
| **Backend Specialist Repositioning** | Portfolio Copy | `v2/src/components/Sidebar.js`, `About.js` | Antigravity | **Completed** |
| **Navigation Restored (Contact Tab)** | UX / Conversion | `v2/src/app/page.js`, `Navbar.js` | Antigravity | **Completed** |
| **Production Build Verification** | Compiler | `npm run build` | Antigravity | **Completed** |

---

## 📜 Historical Daily Activity Log

### 2026-10-01
- Completed Phase 1 Current State Audit (`/next-move/00-current-state-audit.md`) with a 12-section diagnostic of website architecture, conversion bottlenecks, and positioning strengths.
- Built the complete `/next-move/` personal operating manual and execution blueprint containing 19 core strategy/system files + 31 daily execution guides (`daily/day-01.md` through `daily/day-31.md`).
- Repositioned portfolio copy in `Sidebar.js` and `About.js` strictly around **Senior Backend & Performance Specialist** (Node.js/TypeScript, Go, PostgreSQL, Redis, Docker, Cloud Infra).
- Restored direct `Contact` tab alongside 4-step calendar booking wizard in `page.js` and `Navbar.js`.
- Verified production build cleanliness via `npm run build` (exit code 0, static generation 21/21 pages).
- Registered `ADR-017` in canonical master knowledge base.

### 2026-09-24
- Implemented full PostHog telemetry, session replay, and conversion analytics in Next.js 16 (`shafik-protfolio` `v2`).
- Wrapped Next.js App Router route transitions inside `PostHogPageView` with `<Suspense fallback={null}>`.
- Designed and dispatched multi-stage conversion events across all core portfolio interactions:
  - `booking_funnel_step` (steps 1–4)
  - `contact_initiated` (`form_submit` / `mailto`)
  - `contact_form_step` (`form_started` / `form_submitted`)
  - `project_clicked` (`github` / `live_demo` / `case_study`)
  - `social_link_clicked` (`linkedin` / `github` / `email`)
  - `tab_switched` (client-side tab pageviews)
- Verified zero CSS/layout regressions; verified clean Turbopack build in 34.0s (`bun run build`).
- Created and registered `ADR-014` in the canonical master knowledge base.
- Configured and pinned the production conversion funnel in the live PostHog dashboard.
