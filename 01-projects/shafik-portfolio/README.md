# Shafikul Islam Portfolio & B2B Telemetry Architecture (`shafik-portfolio`)

> **Host Workspace Path:** `/home/shafikul/Documents/coding/shafik-protfolio/`  
> **Production URL:** [`https://shafiktanbir.com`](https://shafiktanbir.com) / [`https://kraken.nesohq.org/`](https://kraken.nesohq.org/)  
> **Tech Stack:** Next.js 16 (Turbopack, App Router), React 19, Tailwind CSS v4, MongoDB, Docker, PostHog Analytics

---

## 🏛️ Architecture & System Design

```mermaid
flowchart TD
    subgraph Client["Next.js 16 App Router (React 19)"]
        A["RootLayout (app/layout.js)"] --> B["PostHogProvider (app/providers.js)"]
        B --> C["PostHogPageView (<Suspense>)"]
        B --> D["Client Components & Sections"]
        D --> E["BookMeeting.js (4-Step Wizard)"]
        D --> F["Contact.js (B2B Form)"]
        D --> G["Portfolio.js & About.js (Case Studies)"]
        D --> H["Sidebar.js & Footer.js (Socials/Outreach)"]
    end

    subgraph Telemetry["Centralized Analytics (src/lib/analytics.js)"]
        E -->|trackBookingStep| T1["booking_funnel_step"]
        E -->|trackContactInitiated| T2["contact_initiated"]
        F -->|trackContactStep| T3["contact_form_step"]
        G -->|trackProjectClick| T4["project_clicked"]
        H -->|trackSocialClick| T5["social_link_clicked"]
        D -->|trackTabSwitch| T6["tab_switched & $pageview"]
    end

    subgraph Ingestion["PostHog Cloud (us.i.posthog.com)"]
        T1 & T2 & T3 & T4 & T5 & T6 --> P1["PostHog Ingestion Pipeline"]
        P1 --> P2["Session Replay Recordings"]
        P1 --> P3["Conversion Funnel Insights"]
        P1 --> P4["Live Events Activity Stream"]
    end
```

---

## 🎯 Conversion Funnel Map

### 1. Consultation Booking Funnel
- **Step 1:** `$pageview` where `Current URL contains tab=book`
- **Step 2:** `booking_funnel_step` (`step_name = date_selected`)
- **Step 3:** `booking_funnel_step` (`step_name = time_slot_selected`)
- **Step 4:** `booking_funnel_step` (`step_name = details_submitted`)
- **Step 5:** `booking_funnel_step` (`step_name = booking_confirmed`) / `contact_initiated` (`method = form_submit`)

### 2. Contact Form Engagement Funnel
- **Step 1:** `contact_form_step` (`step_name = form_started` on input focus)
- **Step 2:** `contact_form_step` (`step_name = form_submitted` on API success)

### 3. Recruiter Outreach Funnel
- **Step 1:** `$pageview` on `/` or `tab=resume`
- **Step 2:** `resume_downloaded` or `project_clicked`
- **Step 3:** `social_link_clicked` (`platform: linkedin` or `email`)

---

## 📂 Key Architecture Files
- **Layout Provider:** [`v2/src/app/providers.js`](file:///home/shafikul/Documents/coding/shafik-protfolio/v2/src/app/providers.js)
- **Telemetry Schema:** [`v2/src/lib/analytics.js`](file:///home/shafikul/Documents/coding/shafik-protfolio/v2/src/lib/analytics.js)
- **ADR Reference:** [`knowledgebase/01-projects/adr/ADR-014-client-side-telemetry-posthog-conversion-funnels.md`](file:///home/shafikul/Documents/coding/research-playground-loop/knowledgebase/01-projects/adr/ADR-014-client-side-telemetry-posthog-conversion-funnels.md)
