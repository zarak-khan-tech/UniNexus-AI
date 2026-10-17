"""
English: Update the project structure tree in README to include new modules.
Roman Urdu: README ke project structure tree mein naye modules add karo.
"""
path = "README.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update api/ line
old_api = "│   ├── api/ auth, agents, stats, academic, analytics, approvals, tools, notifications, workflows, tenant, imports, documents"
new_api = "│   ├── api/ auth, agents, stats, academic, analytics, approvals, tools, notifications, workflows, tenant, imports, documents, search, events, integrations"
if old_api in content:
    content = content.replace(old_api, new_api, 1)

# 2. Update core/ line
old_core = "│   ├── core/ config, database, security, llm wrapper, llm_gateway/, embeddings, vector_store, reasoning, safety, rate_limit"
new_core = "│   ├── core/ config, database, security, llm wrapper, llm_gateway/, embeddings, vector_store, reasoning, safety, rate_limit, events, error_handlers"
if old_core in content:
    content = content.replace(old_core, new_core, 1)

# 3. Update services/ line
old_services = "│   ├── services/ notifications, workflow_engine, tool_definitions, agent_definitions, tenant_settings, document_ingest"
new_services = "│   ├── services/ notifications, workflow_engine, tool_definitions, agent_definitions, tenant_settings, document_ingest, event_triggers"
if old_services in content:
    content = content.replace(old_services, new_services, 1)

# 4. Add integrations/ folder line right after models/
old_models = "│   ├── models/ tenant, user, student, course, enrollment, document, agent_execution, approval, notification, workflow, agent_definition, tool_definition"
new_models = old_models + "\n│   ├── integrations/ base, registry, adapters/"
if old_models in content:
    content = content.replace(old_models, new_models, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: Project structure tree updated in README")
