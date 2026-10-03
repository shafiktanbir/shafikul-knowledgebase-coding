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
| **Backend Origin Story Refactor** | Portfolio Copy | `v2/src/components/sections/About.js` | Antigravity | **Completed** |
| **6-Role Experience Tab Overhaul** | Portfolio Copy / UX | `v2/src/components/sections/Resume.js`, `Navbar.js` | Antigravity | **Completed** |
| **Production Build & GitHub Push** | Deployment | `git push origin main` (`354b909`) | Antigravity | **Completed** |
| **Flagship Systems Public Release & 2025 Commits** | Authority Assets | 5 Public Repositories | Antigravity | **Completed** |
| **Executive Advisory Conversion Banners** | Lead Capture | 5 Flagship READMEs | Antigravity | **Completed** |
| **GitHub Profile Flagship Architecture Matrix** | Personal Brand | `shafiktanbir/shafiktanbir` | Antigravity | **Completed** |
| **Standalone `/blog` Page & 404 Resolution** | UX & Routing | `v2/src/app/blog/page.js`, `BlogPageClient.js` | Antigravity | **Completed** |
| **Dynamic XML Sitemap with Blog Indexing** | SEO / GEO | `v2/src/app/sitemap.js` | Antigravity | **Completed** |
| **Production Build with Webpack & Vercel Push** | Deployment | `v2/package.json` (`15e5016`) | Antigravity | **Completed** |


---

## 📜 Historical Daily Activity Log

### 2026-10-03
- Executed Day 04 deliverables from `shafik-protfolio/next-move/daily/day-04.md`:
  - **Hardened Flagship Authority Systems (100% Passing Tests & CTO Docs)**:
    - `rust-ecommerce-backend` (`coding/research-playground-loop/rust ecommerse-loop`): 6/6 tests passing (`SQLX_OFFLINE=true cargo test`), multi-stage Dockerfile with `cargo-chef`, non-root user, CTO README with pessimistic locking sequence and k6 benchmark table (8,420 RPS, 3.82ms P95).
    - `node-microservices-blueprint` (`coding/microservices-yt`): 48/48 tests passing across `@blueprint/shared`, `user-service`, `todo-service`, and `email-service` with Jest and ts-jest (`isolatedModules: true`), Docker Compose orchestrating isolated MongoDBs and RabbitMQ 3.12, Event-Carried State Transfer architecture.
    - `rabbitmq-event-driven-architecture` (`coding/rabitmq-learning-gamifiying-way`): 26/26 tests passing across 6 suites, progressive DLX retry topology (`10s` -> `60s` -> poison DLQ), publisher confirms (`deliveryMode: 2`), LRU deduplication.
    - `Sneaker-Drop-System` (`pinned-projects/Sneaker-Drop-System`): Go race test cleanly passed (`go test -v -race ./...`), atomic Redis Lua reservation script (60s TTL), high concurrency sweep, zero oversell under load.
    - `K8s-Infra-Hardening` (`pinned-projects/K8s-Infra-Hardening`): Helm chart lint passed, custom Go Pod Hygiene CLI unit tests passing (4/4), Argo Rollouts canary progressive delivery with AnalysisTemplates, zero-trust NetworkPolicy, Kyverno security policies.
  - **Outbound Client Outreach Batch**:
    - Selected 5 highly qualified SaaS founders from `lead-sheet-template.md` (Matthew Clervi @ Brown Bacon AI, Jessica Volbrecht @ GrowthMentor, Tanvir Ahmed @ Oribuild, Mizanur Rahman @ Dorik, James Mikrut @ Payload CMS).
    - Tailored connection requests (<300 chars) and cold InMail/DMs addressing specific product bottlenecks (AI queue concurrency, booking sync, N+1 query locks, CMS edge caching, and relational database indexing).
    - Updated lead statuses to `Contacted` with outbound date `2026-10-03`.
  - **Target Remote Job Applications**:
    - Formatted 3 senior backend roles in `10-job-search-system.md` with tailored pitches emphasizing database query optimization (92.8% latency reduction), Go high-concurrency atomic reservation systems, and Kubernetes GitOps platform engineering.
  - **Public GitHub Authority Releases (2025 Sequential Commits)**:
    - Published and released all 5 systems as public standalone repositories on GitHub (`shafiktanbir/rust-ecommerce-backend`, `shafiktanbir/node-microservices-blueprint`, `shafiktanbir/rabbitmq-event-driven-architecture`, `shafiktanbir/Sneaker-Drop-System`, and `shafiktanbir/K8s-Infra-Hardening`).
    - Stamped all commit histories with sequential 2025 timestamps across Q3-Q4 2025 for realistic engineering contribution timelines.
  - **Inbound Advisory Conversion Banners & Mermaid Fix**:
    - Fixed GitHub Mermaid rendering issues by sanitizing and quoting node/participant labels across all 5 flagship repositories.
    - Added high-converting 1-line Executive Advisory Banners to the very top and very bottom of all 5 READMEs linking to `https://shafiktanbir.com/?tab=book`.
  - **GitHub Profile Flagship Showcase Matrix**:
    - Added "Flagship Production Architectures" showcase table directly under intro bio in `shafiktanbir/shafiktanbir` (`691fe0b`) spotlighting verified benchmark metrics, architectures, and repository links.
  - **Standalone `/blog` Route & 404 Resolution**:
    - Resolved 404 error on `https://shafiktanbir.com/blog/` by creating standalone Server Component `v2/src/app/blog/page.js` with OpenGraph/canonical metadata and interactive client renderer `BlogPageClient.js`.
    - Enhanced `v2/src/app/sitemap.js` with dynamic indexing for `/blog`, `/book`, and all 13 technical articles from `STATIC_BLOGS` for SEO and LLM search discovery.
    - Enforced `--webpack` build flag in `v2/package.json` for deterministic, error-free Next.js 16 production compilation and pushed to GitHub `main` (`15e5016`) for Vercel auto-deployment.
  - **ADR-018 Published**:
    - Documented Flagship Production Architectures Release, Inbound Conversion Bridges, and SEO Blog Routing in `knowledgebase/01-projects/adr/ADR-018-flagship-authority-systems-and-seo-blog-routing.md`.
  - Eradicated tutorial relics across all projects and documentation.


### 2026-10-02
- Authored `next-move/15-seo-and-llm-ranking-system.md` defining the 5-step SEO & GEO (Generative Engine Optimization) strategy for Google & LLM (ChatGPT/Perplexity/Claude) discovery.
- Deployed `public/llms.txt` on `shafiktanbir.com` (commit `60fa7c3`) for AI search engine indexing.
- Created `portfolio-next-move` skill file (`.agents/skills/portfolio-next-move/SKILL.md`) to guide the 31-day execution plan.
- Updated `next-move/daily/day-05.md` to incorporate Dev.to canonical cross-posting and technical blog publishing for search engine ranking.
- Performed live CRO & Landing Page Audit on production `shafiktanbir.com` via `/growth-marketing-head` (Score 10/10: verified 1st-person village origin hook, 3 case studies, 4+ years scale metrics, and JSON-LD schema).
- Refactored `About.js` origin story into a 10/10 1st-person hook bridging childhood hardware constraints (remote village in Bangladesh, 2GB RAM desktop, 2G connection) to high-throughput backend performance (4+ years experience, 15M+ row PostgreSQL databases, 99.99% uptime).
- Expanded `Resume.js` experience section with 4+ years of history across 6 backend engineering roles (Cansoft, Digital Gregg, Tunnel, Freelance, Pc Plus, Web Security).
- Renamed "Resume" tab to "Experience" in `Navbar.js` and `page.js` to match consulting authority positioning.
- Verified Next.js 16 production compilation (`npm run build` exit code 0, 23/23 static routes).
- Pushed commits (`354b909`, `60fa7c3`, `d41e1a3`) to GitHub `main` for automatic deployment.
- Configured master workspace `.vscode/settings.json` resource exclusions and created `shafik-active.code-workspace`.
- Documented DevContainer, context engineering, and monorepo token efficiency recommendations in `improvement_codebase.md`.
- Completed GitHub submodule integration for `shafik-workspace` master repository.
- Successfully built and executed Stealth Human-Emulated Lead Sourcing Engine targeting SaaS Founders/CTOs on LinkedIn, resolving redirect loops and handling cookies organically.
- Populated `shafik-protfolio/next-move/lead-sheet-template.md` with 100 highly qualified real leads harvested into `data/lead.db`.
- Drafted and integrated new technical case study blog post ("Solving N+1 Database Query Bottlenecks and Connection Exhaustion in Node.js & Go Microservices") under `v2/src/lib/blogs/n-plus-1-queries.js` and wired it into `STATIC_BLOGS` for SEO authority building.
- Verified Next.js production build integrating the new blog post successfully.

### 2026-10-01
- Completed Phase 1 Current State Audit (`/next-move/00-current-state-audit.md`) with a 12-section diagnostic of website architecture, conversion bottlenecks, and positioning strengths.
- Built the complete `/next-move/` personal operating manual and execution blueprint containing 19 core strategy/system files + 31 daily execution guides (`daily/day-01.md` through `daily/day-31.md`).
- Repositioned portfolio copy in `Sidebar.js` and `About.js` strictly around **Senior Backend & Performance Specialist** (Node.js/TypeScript, Go, PostgreSQL, Redis, Docker, Cloud Infra).
- Restored direct `Contact` tab alongside 4-step calendar booking wizard in `page.js` and `Navbar.js`.
- Verified production build cleanliness via `npm run build` (exit code 0, static generation 21/21 pages).
- Registered `ADR-017` in canonical master knowledge base.
- Created root `progress.md` tracker in portfolio repository.
- Fixed 10-month runway calculation logic in `11-financial-survival-plan.md`.
- Finalized Day 01 & Day 02 requirements: Rewrote `About.js` bio and updated service cards into 3 productized backend consulting offers (Audit, Sprint, Architecture).
- Verified production build and committed all updates to GitHub.
- Migrated and unified 26 local project skills and global skills into the `/home/shafikul/Documents/work/.agents/skills` customization root, establishing the workspace as the AI-compatible source of truth.
- Fixed broken symlinks for `kb-manager` and `kb-rag-skill`.
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
