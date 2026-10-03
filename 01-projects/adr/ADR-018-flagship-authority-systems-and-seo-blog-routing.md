# ADR-018: Flagship Production Architectures Release, Inbound Conversion Bridges & SEO Blog Routing

* **Status:** Accepted  
* **Date:** 2026-10-03  
* **Authors:** Shafikul Islam, Senior Backend & Cloud Infrastructure Architect  
* **Context:** Flagship System Upgrades, GitHub Profile Repositioning, Portfolio Blog Routing (`shafiktanbir.com`)  

---

## 🎯 Context & Problem Statement

Following the Day 04 execution directives of the client acquisition roadmap, the engineering portfolio required transition from local development experiments to verifiable, enterprise-grade proof of work:

1. **Lack of Concrete Public Verification:** Earlier repositories contained tutorial/learning artifacts, non-deterministic performance figures, and lacked containerized multi-stage deployments.
2. **"Dead-End" Repository READMEs:** High-intent CTO or recruiter traffic landing on technical repositories had zero clear inbound bridges to technical consultation or architecture audit scheduling.
3. **Portfolio Blog Routing Failure (404 Error):** Direct browser navigation to `https://shafiktanbir.com/blog/` resulted in an unhandled Next.js 404 error because `v2/src/app/blog/page.js` was missing, stranding organic search and LLM crawler traffic.

---

## 💡 Decision Drivers

* **Undeniable Staff-Level Proof:** Provide battle-tested concurrency, high throughput, zero data races, and exact benchmark figures (k6 load testing) across all flagship projects.
* **Inbound Conversion Telemetry:** Every flagship repository must feature prominent, clean Executive Advisory Banners routing traffic to `shafiktanbir.com/?tab=book`.
* **Zero 404 Disruption on Content Routes:** Both standalone `/blog` and dynamic `/blog/[id]` paths must be fully discoverable by search engines (Google) and AI discovery crawlers (SearchGPT, Perplexity, ChatGPT).
* **Stable Next.js Compilation:** Next.js 16 build pipeline must avoid Turbopack font resolution bugs by enforcing `--webpack` in production builds.

---

## 🏛️ Architecture & System Changes

### 1. Hardening 5 Flagship Production Systems
Upgraded and published 5 public repositories with sequential 2025 commit histories and zero beginner relics:
* 🦀 **`rust-ecommerce-backend`**: Axum 0.7, Tokio, SQLx with pessimistic row-level `FOR UPDATE` locking, Redis connection pooling, and multi-stage `cargo-chef` containerization. Verified: **8,420 RPS @ 3.82ms P95 latency** and 0.00% inventory oversell.
* 👟 **`Sneaker-Drop-System`**: High-concurrency Go engine, Redis Lua atomic reservation scripts (`EVALSHA` with 60s TTL), asynchronous PostgreSQL write-behind worker buffer, and WebSocket stock broadcasts. Verified: **0.00% double-booking under 10k users** and 0 data races (`go test -race`).
* ☁️ **`K8s-Infra-Hardening`**: Production Helm chart, ArgoCD GitOps, Argo Rollouts progressive canary delivery with AnalysisTemplates, zero-trust NetworkPolicy, Kyverno admission control, and custom Go Pod Hygiene CLI. Verified: **35% EC2 cluster node savings**.
* 🧩 **`node-microservices-blueprint`**: Decoupled Event-Carried State Transfer architecture using RabbitMQ 3.12 topic exchanges, cryptographic JWT verification, runtime Zod schema validation, and per-service isolated MongoDBs. Verified: **48/48 passing Jest tests**.
* 🐇 **`rabbitmq-event-driven-architecture`**: Progressive Dead-Letter Exchange retry topology (`orders.retry.10s` → `orders.retry.60s` → `orders.poison.dlq`), `ReliablePublisher` with flow-control backpressure and publisher confirms. Verified: **Zero message loss under network partitions**.

### 2. Executive Inbound Advisory Bridges & GitHub Profile Showcase
* Embedded 1-line Executive Consultation Banners at the very top and very bottom of each repository README:
  `> 💡 **Available for Technical Consulting & High-Concurrency Architecture Audits:** [Book a 20-min System Teardown](https://shafiktanbir.com/?tab=book) · [Explore Full Case Studies](https://shafiktanbir.com)`
* Deployed the **Flagship Production Architectures** matrix directly beneath the intro bio on GitHub profile `shafiktanbir/shafiktanbir`.

### 3. Standalone Blog Routing & Enhanced SEO Sitemap (`v2/`)
* **Created Standalone Blog Route:** Added `v2/src/app/blog/page.js` (Server Component with canonical OpenGraph and Twitter metadata) backed by `v2/src/app/blog/BlogPageClient.js` (Client Component hosting interactive tab transitions and the `<Blog />` component).
* **Enhanced XML Sitemap (`app/sitemap.js`):** Dynamically generates sitemap entries for `/blog`, `/book`, and all 13 technical case studies from `STATIC_BLOGS`.
* **Standardized Build Script:** Updated `v2/package.json` to `"build": "rm -rf .next && next build --webpack"` to ensure reliable Google font compilation.

### 4. Interactive State Propagation for Consultation CTAs (`About.js`)
* **Propagated State Callback:** Passed `setActivePage={setActivePage}` from `renderSection()` across `app/page.js`, `app/blog/BlogPageClient.js`, and `app/book/page.js` into child view components.
* **Eliminated Broken Synthetic Events:** Removed non-functioning `window.dispatchEvent(new Event("popstate"))` calls on the "Explore Solution" CTA cards, replacing with direct `setActivePage("book")` state mutation, URL query synchronization (`/?tab=book`), and smooth scroll orchestration.


---

## 📊 Consequences & Validation

* **Positive:**
  - `shafiktanbir.com/blog/` successfully renders the full blog grid without 404 errors.
  - LLMs and search engines index all 13 technical articles via `sitemap.xml` and `llms.txt`.
  - All 5 flagship repositories funnel technical traffic directly to the 20-minute architecture audit booking funnel.
* **Operational Risks & Mitigations:**
  - Build pipeline verified locally with Next.js webpack build completing successfully.
