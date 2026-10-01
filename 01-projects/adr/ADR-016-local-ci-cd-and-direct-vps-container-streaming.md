# ADR-016: Local CI/CD Quality Gates & Direct SSH Container Streaming for Zero-Quota Deployment Resilience

**Date:** 2026-09-25  
**Status:** Accepted  
**Deciders:** Principal Full-Stack Architect, Senior DevOps Engineer, Engineering Manager  
**Primary Target:** Meta-workspace root `Makefile`, `scripts/deploy-backend.sh`, `scripts/deploy-frontend.sh`, `scripts/merge-main.sh`

---

## 1. Context & Problem Statement

The organization-level GitHub Actions runner quota on `Cansoft-Technologies` was exhausted, triggering the failure notification:
> *"The job was not started because recent account payments have failed or your spending limit needs to be increased."*

This unexpected external billing lock disrupted automated CI testing, pull request verifications, and deployments across both the backend (`clinic-booking-app-backend`) and frontend (`clinic-booking-app-frontend`) repositories.

### Operational Risks:
1. **Developer Blockage:** Teams could not merge feature branches into `main` because automated GitHub workflows were blocked.
2. **Configuration Drift & Deployment Regression:** Ad-hoc manual SSH deployments risk bypassing linting, typechecking, running database migrations improperly, or failing to verify container health post-deploy.
3. **Registry Dependency:** Pushing to GitHub Container Registry (`ghcr.io`) required fine-grained PAT scopes (`write:packages`) which are not universally accessible to all developers or could also be throttled.

---

## 2. Decision Drivers

- **Zero External Runner Quota Dependency:** Developers must be able to run complete CI suites, build production containers, and deploy to live servers without consuming cloud runner minutes.
- **Strict Quality Invariants:** Every deployment must strictly enforce ESLint, TypeScript compilation (`tsc --noEmit`), and integration tests prior to deployment.
- **Automated Direct-to-Main Merges:** If and only if all local CI checks pass, the active branch should be merged directly into `main` and pushed to `origin/main`.
- **Registry-Independent Container Delivery:** Docker images must transfer directly from the build host to the target VPS instances with minimal overhead and zero reliance on intermediary image registries.
- **Automated Database Migrations & Health Gates:** The deployment pipeline must automatically execute pre-migration backups, apply SQL migrations, restart services with `--remove-orphans`, and assert `HTTP 200 OK` on public health endpoints before declaring success.

---

## 3. Decision Outcome

### 1. Unified Command Center (`Makefile`)
A root `Makefile` was established at the meta-workspace level (`/home/shafikul/Documents/office_work/clinic-app/Makefile`) providing intuitive, colored targets:
- `make ci`: Parallel/sequential execution of backend and frontend CI checks.
- `make merge-main`: Safety-gated merge of active branches into `main`.
- `make deploy`: End-to-end deployment (CI -> Merge -> Build -> Stream -> Migrate -> Health check).
- `make status` & `make health`: Real-time inspection of live VPS containers and public endpoints.
- `make logs-backend` & `make logs-frontend`: Real-time streaming log tails from production containers.

### 2. Direct-to-Main Fast Merging (`scripts/merge-main.sh`)
- Evaluates the active branch.
- Executes `scripts/ci-backend.sh` and `scripts/ci-frontend.sh`.
- If CI succeeds:
  1. Automatically stages and commits uncommitted changes.
  2. Checks out `main` and pulls latest `origin/main`.
  3. Merges the branch cleanly (`git merge <branch> --no-edit`).
  4. Pushes `main` directly to `origin/main`.
  5. Restores original branch context.
- If CI fails: immediately halts execution and prevents merging into `main`.

### 3. Direct SSH Image Streaming (`docker save | gzip | ssh ... docker load`)
Rather than relying on `ghcr.io` or Docker Hub:
```bash
docker save "${IMAGE_NAME}" | gzip -c | ssh -i "${SSH_KEY}" "${VPS_USER}@${VPS_HOST}" "gunzip -c | docker load"
```
- **Transfer Speeds:**
  - Backend image (571 MB uncompressed, ~150 MB compressed): streamed in ~20-30s.
  - Frontend image (212 MB uncompressed, ~60 MB compressed): streamed in ~10-15s.
- Eliminates third-party bandwidth charges, rate limits, and authentication token expiration.

### 4. Automated VPS Migration & Health Assertions
On the remote VPS over SSH:
- Pre-migration database backup (`scripts/db-backup.sh`).
- Containerized migration execution: `docker compose run --rm clinic-app node scripts/migrate.js up`.
- Container recreation: `docker compose up -d --force-recreate --remove-orphans <service>`.
- Reverse proxy hot reload: `docker compose exec nginx nginx -s reload`.
- Public endpoint health polling:
  - Backend: `https://api.emmai.ca/health` (HTTP 200 OK required).
  - Frontend: `https://vancouverspeechtherapy.emmai.ca` (HTTP 200/307 required).

---

## 4. Consequences & Tradeoffs

### Positive:
- **Total Quota Immunity:** Zero billing or runner quota failures can block deployments.
- **Fast Feedback Loop:** Local compilation leverages multicore CPU caches, cutting build times significantly compared to cold cloud runner VMs.
- **Preserved Rigor:** Enforces the same strict linting, typechecking, and test validation as GitHub Actions.
- **Zero Cost:** No cloud compute minutes or registry storage fees.

### Tradeoffs & Mitigation:
- **Local Machine Compute:** Building Docker images locally consumes developer CPU and memory.
  - *Mitigation:* Multi-stage Docker caching and `buildx` keep incremental rebuilds under 30 seconds.
- **Upload Bandwidth:** Direct streaming transfers the compressed image over SSH.
  - *Mitigation:* `gzip` compression reduces image payload by >70%; subsequent layer caching minimizes transfer overhead.
