# ADR-007: Enterprise COSS "Contribute-to-Hire" Strategy & Hybrid OLTP/OLAP Architecture

**Date:** 2026-09-13  
**Status:** Accepted  
**Deciders:** Shafikul Islam (Full Stack & Distributed Systems Engineer), AI Technical Architect  

---

## 1. Context & Problem Statement
Traditional engineering hiring (cold resumes, automated keyword filters) has high friction and low conversion for senior remote backend and cloud roles. Simultaneously, modern high-throughput developer platforms face architectural bottlenecks when forcing standard relational databases (PostgreSQL) to handle analytical event aggregation at scale.

We need:
1. A repeatable, high-leverage mechanism to establish technical credibility and secure remote engineering employment at tier-1 enterprise and venture-backed tech companies.
2. A codified architectural blueprint for designing high-throughput backends that manage both ACID-compliant business state and billion-row analytical queries without performance degradation.

---

## 2. Decision Drivers
* **Driver 1 (Career ROI):** Direct access to engineering managers and founders by proving production competence in public codebases.
* **Driver 2 (Scalability & Throughput):** Handling billions of analytical events without compromising transactional data integrity.
* **Driver 3 (Stack Synergy):** Direct alignment with core competencies in Python (Django/FastAPI), Go, Kubernetes, Redis, Celery, and Model Context Protocol (MCP).

---

## 3. Considered Options
* **Option 1 (Traditional Job Application):** Standard resume submission on LinkedIn / job boards without public code proof.
* **Option 2 (Casual Open Source):** Sporadic contributions to hobby projects or documentation typo fixes without commercial backing.
* **Option 3 (Strategic Enterprise COSS "Contribute-to-Hire"):** Targeted contributions to venture-backed (YC, Series A-D) and enterprise-backed (CNCF) commercial open-source software (COSS) companies with documented history of hiring community contributors (e.g., PostHog, Dify, Aqua Trivy, Longhorn).

---

## 4. Decision Outcome
Chosen Option: **Option 3 (Strategic Enterprise COSS "Contribute-to-Hire")**.

### Architectural & Strategy Principles:
1. **The 6-Step Funnel:** Repository qualification -> Local Docker/Compose setup -> 48h starter PR (tests/bugs) -> Community Slack/Discord integration -> Core architectural PR (resilience, caching, perf) -> Direct maintainer/EM outreach.
2. **The Hybrid OLTP + OLAP Dual-Database Paradigm:**
   - **Operational State (OLTP):** PostgreSQL via Django ORM for users, organizations, permissions (RBAC), feature flag definitions, and billing.
   - **Analytical Big Data (OLAP):** ClickHouse for high-throughput, columnar, vectorized aggregation (funnels, retention, event streams).
   - **Orchestration Layer:** Django REST Framework (DRF) as the headless API control plane, utilizing Redis token-bucket rate limiters (`token_bucket.py`) and atomic Lua circuit breakers (`db_circuit_breaker.py`).

---

## 5. Consequences & Trade-offs
* **Positive:** Bypasses recruiter screening; provides tangible open-source proof of work in enterprise monorepos (50,000+ files); deepens knowledge of ClickHouse, Kafka, and Redis Lua scripting.
* **Negative:** Requires significant initial effort to clone and navigate large monorepos; PR turnaround times depend on maintainer review bandwidth.
