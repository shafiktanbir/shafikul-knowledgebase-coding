# Knowledge Base — Research Playground Loop

> **Universal Context & Knowledge Graph Index for AI Agents and Engineers**

Welcome to the root Knowledge Base for the `research-playground-loop` monorepo workspace. This directory serves as the canonical source of structural understanding, architectural relationships, project registries, and state tracking across all sub-projects in this repository.

---

## 📌 Structure & Navigation

This Knowledge Base is organized into structured markdown modules designed for rapid consumption by both AI agents (Antigravity, Claude Code, Cursor, Codex) and human developers:

| File / Directory | Description | Target Audience |
| :--- | :--- | :--- |
| [`KNOWLEDGE_BASE_MASTER_INDEX.md`](KNOWLEDGE_BASE_MASTER_INDEX.md) | **Master Unified KB System**: Central directory for Projects, Areas, Resources, and Archives (PARA + Diátaxis + ADR). | All Developers, AI Agents |
| [`01-projects/`](01-projects/) | **Active Projects & Sprints**: Active task boards (`sprint-board.md`) and ADR decision records. | Developers, Product |
| [`02-areas/`](02-areas/) | **Domain Areas**: Technical guidelines, backend/DevOps architecture, DB rules. | Developers, Architects |
| [`03-resources/`](03-resources/) | **Learning Resources**: Troubleshooting how-to recipes and skill roadmaps. | Developers, Learners |
| [`04-archives/`](04-archives/) | **Archives**: Historical logs and completed sprint records. | All Users |
| [`GRAPH_REPORT.md`](GRAPH_REPORT.md) | **Codebase Knowledge Graph**: Structural breakdown of community clusters, "God Nodes", and dependency relationships. | AI Agents, Architects |
| [`ARCHITECTURE_MAP.md`](ARCHITECTURE_MAP.md) | **System Architecture & Domain Map**: High-level domain boundaries and data flow across all sub-projects. | Developers, Agents |
| [`PROJECT_REGISTRY.md`](PROJECT_REGISTRY.md) | **Complete Project Catalog**: Comprehensive index of every subfolder/application with entry points. | All Users |
| [`MAINTENANCE_GUIDE.md`](MAINTENANCE_GUIDE.md) | **Agent Maintenance Protocol**: Rules for AI agents to maintain and update this Knowledge Base. | AI Agents |

---

## 🔍 How AI Agents Must Use This Knowledge Base

1. **Orientation Phase**: Before initiating code modifications or answering architectural queries, agents MUST inspect [`GRAPH_REPORT.md`](GRAPH_REPORT.md) and [`PROJECT_REGISTRY.md`](PROJECT_REGISTRY.md).
2. **Impact & Blast Radius Check**: When refactoring or introducing new features, consult the dependency graphs in [`GRAPH_REPORT.md`](GRAPH_REPORT.md) to understand impacted components.
3. **Continuous Maintenance**: Whenever creating new modules, altering APIs, or completing learning/feature milestones, agents MUST update the corresponding files in this `knowledgebase/` folder as specified in [`MAINTENANCE_GUIDE.md`](MAINTENANCE_GUIDE.md).

---

## 📁 Sub-Project Knowledge Bases

For deep domain-specific knowledge, refer to sub-project knowledge bases:
- 🎓 **Interview Prep**: [`../interview-prep/knowledgebase/`](../interview-prep/knowledgebase/)
- 💼 **Freelance Consulting Mentor**: [`../freelance mentor/progress.md`](../freelance%20mentor/progress.md)
- 📱 **Android Product Engineer**: [`../product enginer/progress.md`](../product%20enginer/progress.md)
- ⚡ **Coven Authority Layer**: [`../coven/docs/`](../coven/docs/) & [`../coven/specs/`](../coven/specs/)
