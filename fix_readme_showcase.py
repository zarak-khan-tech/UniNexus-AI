"""
English: Inject the professional project showcase section into README.md.
Roman Urdu: README.md mein professional screenshots wala section add karo.
"""
import os

path = "README.md"
if not os.path.exists(path):
    print("ERROR: README.md not found")
    raise SystemExit(1)

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if "## 📸 Project Showcase" in content:
    print("SKIP: Showcase section already exists in README.md")
    raise SystemExit(0)

showcase_text = """
---

## 📸 Project Showcase

### 🧠 AI Command Center & Reasoning
*Real agentic reasoning with multi-turn memory, tool-calling, and the anti-hallucination guard in action.*

**Agent Workflow Execution:**
![Command Center Workflow](docs/screenshots/Command-Center-Agent-Workflow.png)

**Multi-turn Reasoning & Hallucination Guard:**
![Reasoning Loop](docs/screenshots/Reasoning-Loop.png)

### 📊 Dashboards & Institutional Analytics
*Live snapshots of the multi-agent platform, tracking executions, risk distribution, and agent usage.*

![Dashboard Analytics](docs/screenshots/Dashboard-Analytics.png)
![Dashboard Extras](docs/screenshots/Dashboard-Search-Settings-Import-Integration.png)

### 🤖 Multi-Agent Platform Architecture
*DB-driven agents and tools with live health stats, permission levels, and event-driven workflows.*

![Agents & Workflows](docs/screenshots/Agents-Registry-Workflows.png)
![Tools Registry](docs/screenshots/Tools-Registry.png)

### 📚 Data Management & RAG
*CSV imports, document uploads with auto-chunking, and vector-based semantic search.*

![Students Courses Knowledge Base](docs/screenshots/Students-Courses-KnowledgeBase.png)

### 🔒 Security & Observability
*Full audit trails, human-in-the-loop approvals for WRITE_HIGH actions, and system notifications.*

**Audit Logs & Execution Trace:**
![Audit Logs](docs/screenshots/Audit-Logs.png)

**Approvals & Notifications:**
![Approvals Notifications](docs/screenshots/Approvals-Notifications.png)

---
"""

# English: Try to insert before Features or Architecture, otherwise append to end.
# Roman Urdu: Features ya Architecture se pehle add karo, warna end mein lagao.
anchor = "## Features"
if anchor not in content:
    anchor = "## Architecture"
    
if anchor in content:
    content = content.replace(anchor, showcase_text + "\n" + anchor, 1)
    print("FIXED: Showcase inserted before Features/Architecture.")
else:
    content += showcase_text
    print("FIXED: Showcase appended to the end of README.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
