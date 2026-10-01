# ADR-014: Client-Side Telemetry, Session Replay & Conversion Funnels for Next.js 16

**Date:** 2026-09-24  
**Status:** Accepted  
**Deciders:** Senior Fullstack & Telemetry Lead (Shafikul Islam, Antigravity)  
**Target Repository:** `/home/shafikul/Documents/coding/shafik-protfolio/` (Next.js 16 App Router, React 19)

---

## 1. Context & Problem Statement
The personal engineering portfolio (`kraken` hosted at `shafiktanbir.com`) required production-grade web telemetry, session recording, and conversion analytics to quantify visitor engagement, audit consultation bookings, and recruiter outreach. 

Key technical requirements:
1. Zero visual or layout regressions: No modifications to existing Tailwind CSS v4 styling, animations, or DOM structure.
2. Next.js App Router route transition tracking: In client-side tab navigation (`?tab=about`, `?tab=book`, `?tab=resume`), standard Next.js full page reloads do not trigger; telemetry must detect both router transitions and query parameter changes.
3. Multi-step conversion funnels: Track drop-offs in the 4-step consultation booking wizard (`BookMeeting.js`) and 2-step contact form (`Contact.js`).

---

## 2. Decision Drivers
* **Driver 1: Zero UI/Styling Impact:** Avoid adding wrapper markup or changing element layout; attach pure `onClick` and form handlers.
* **Driver 2: Robust Schema Architecture:** Centralize event schemas in a reusable client utility (`src/lib/analytics.js`) rather than spreading raw `posthog.capture` calls throughout components.
* **Driver 3: Next.js Client-Side Routing Safety:** Wrap `useSearchParams()` inside `<Suspense fallback={null}>` in `PostHogPageView` to satisfy Next.js CSR bailout requirements.
* **Driver 4: Single-Source Funnel Observability:** Deliver structured event properties (`step_number`, `step_name`, `method`, `link_type`) to configure production funnels in PostHog Insights.

---

## 3. Considered Options
* **Option 1: Rely solely on PostHog Autocapture:**
  - *Pros:* Zero manual event attachment.
  - *Cons:* Extremely fragile. PostHog stores raw CSS selector paths; any class tweak or refactor invalidates historic funnel definitions. Cannot capture semantic business variables (`step_number: 2`, `link_type: 'github'`).
* **Option 2: Centralized Telemetry Utility + Explicit Event Dispatch + Route Listener:**
  - *Pros:* Type-safe event schemas, decoupled from styling; explicit conversion steps enable high-fidelity PostHog funnels; manual `$pageview` emits with full `$current_url`.
  - *Cons:* Requires attaching lightweight handlers to interactive components.

---

## 4. Decision Outcome
Chosen Option: **Option 2 (Centralized Telemetry Utility + Explicit Event Dispatch)**.

### Implementation Architecture:
1. **Provider (`v2/src/app/providers.js`)**:
   - Initializes PostHog client with `person_profiles: 'identified_only'`, `capture_pageleave: true`, and `session_recording: { maskAllInputs: false }`.
   - Embeds `<Suspense fallback={null}><PostHogPageView /></Suspense>` monitoring `usePathname()` and `useSearchParams()`.
2. **Telemetry Module (`v2/src/lib/analytics.js`)**:
   - `trackResumeDownload(location)` ➔ `resume_downloaded`
   - `trackProjectClick(projectName, linkType)` ➔ `project_clicked` (`github` | `live_demo` | `case_study`)
   - `trackSocialClick(platform)` ➔ `social_link_clicked` (`linkedin` | `github` | `email`)
   - `trackContactInitiated(method)` ➔ `contact_initiated` (`form_submit` | `mailto`)
   - `trackBookingStep(stepNumber, stepName, extra)` ➔ `booking_funnel_step` (steps 1–4)
   - `trackTabSwitch(tabName)` ➔ `tab_switched` + manual `$pageview` update
   - `trackContactStep(stepName)` ➔ `contact_form_step` (`form_started` | `form_submitted`)
3. **Component Integration**:
   - `Sidebar.js`: GitHub/LinkedIn social links and email contact.
   - `Footer.js`: Added `'use client'` and social click tracking.
   - `Portfolio.js`: Repository and live deployment tracking in `ProjectCard`.
   - `About.js`: Case study breakdown click tracking.
   - `Navbar.js`: Instant `trackTabSwitch` on client tab selection.
   - `BookMeeting.js`: Date selection (Step 1), time slot selection (Step 2), details form submission (Step 3), and confirmation (Step 4).
   - `Contact.js`: Form focus interaction (`form_started`) and dispatch (`form_submitted`).

---

## 5. Consequences & Trade-offs
* **Positive:**
  - 100% build pass under Turbopack (`bun run build` exit code 0).
  - High-precision conversion funnels live in PostHog (`Pageview (tab=book) ➔ contact_initiated`).
  - Full session replay allows video playback of user interactions.
  - Zero styling drift or layout modifications.
* **Negative:**
  - Requires maintaining `lib/analytics.js` if new conversion actions are introduced in future sections.
