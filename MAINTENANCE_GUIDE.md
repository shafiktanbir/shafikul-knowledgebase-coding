# MAINTENANCE_GUIDE.md — Agent & Workspace Knowledge Graph Maintenance Protocol

> **Mandatory Workflow for AI Agents and Human Engineers to Maintain and Query the Codebase Knowledge Graph**

---

## 🤖 Codebase Knowledge Graph Directives

This workspace utilizes **Graphify** to parse local code syntax structures into a queryable knowledge graph. All AI agents (Antigravity, Cursor, Claude Code) and developers operating inside `research-playground-loop` must follow these rules to consult and keep the graph synchronized.

### 1. Pre-Task Inspection (Mandatory Read)
Before starting work on any task or responding to architectural queries, agents MUST inspect:
1. [`knowledgebase/PROJECT_REGISTRY.md`](PROJECT_REGISTRY.md) to locate relevant sub-projects and tech stacks.
2. [`knowledgebase/GRAPH_REPORT.md`](GRAPH_REPORT.md) (which links to the active Graphify output) to understand module relationships, God nodes, and dependency blast radius.

---

## 🔄 Daily CLI Use Cases & Cheat Sheet

The following commands are available on your system to query and interact with the codebase graph locally:

### 1. Identify Blast Radius & Dependency Routes (Shortest Path)
Find exactly how changes to file/module A will flow downstream to affect file/module B:
```bash
graphify path "coven/crates/coven-cli" "npm/@opencoven/cli"
```

### 2. Explain a Component and its Neighbors
Generates a structural, plain-language description of a code entity and its immediate call graph:
```bash
graphify explain "backend-playground/file-uploader-system"
```

### 3. Ask Natural Language Questions Over the Code Graph
Queries the graph database using a Breadth-First Search traversal to resolve architectural questions:
```bash
graphify query "Which modules depend on Redis or BullMQ queue?"
```

### 4. Update/Rebuild the Index after Code Changes
Run this command locally after creating new files, classes, or modifying core interfaces to update the index. This command runs entirely locally, takes only seconds, and incurs **zero LLM API token costs**:
```bash
graphify update ./
```

### 5. View the Interactive Visual Collapsible Tree
Open this generated D3-based collapsible tree in your browser to drill down and explore the directory/code hierarchies visually:
- Link: [GRAPH_TREE.html](file:///home/shafikul/Documents/coding/research-playground-loop/knowledgebase/GRAPH_TREE.html)
- Command to regenerate:
  ```bash
  graphify tree --output graphify-out/GRAPH_TREE.html --label "Research Playground Loop"
  ```

---

## 📁 Repository Scoping and Ignore Rules
To maintain indexing speed and prevent memory exhaustion:
* All large external upstream repositories (such as the cloned [`kubernetes/`](../kubernetes/) repository), dependency folders (`node_modules/`), and build output folders are ignored via [`.graphifyignore`](../.graphifyignore).
* The generated database and report assets reside inside `graphify-out/` (which is excluded in `.gitignore` to prevent committing massive files to Git). The `knowledgebase/` folder links to these files via symbolic links.

---

## 🛠️ When to Re-Index the Graph
Agents and developers MUST trigger a graph update:
1. **New Projects/Folders Created**: When introducing a new subdirectory or module.
2. **Major Refactoring / Deletions**: When changing service endpoints, interfaces, or deleting folders (use the `--force` flag on `graphify update` if nodes are deleted).
3. **Daily Sync**: It is recommended to run `graphify update ./` as a post-checkout or pre-commit hook to keep the local graph current.
