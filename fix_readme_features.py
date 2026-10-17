"""
English: Add new feature sections to README.md under the Workflow Automation section.
Roman Urdu: README.md ke Workflow Automation section ke baad naye features add karo.
"""
path = "README.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

anchor = "### Workflow Automation"
if anchor not in content:
    print("ERROR: '### Workflow Automation' anchor not found in README")
    raise SystemExit(1)

new_sections = """### Event Architecture
- Lightweight in-process pub/sub event bus
- Real-time event history API for administrators
- Auto-triggering workflows based on system events (e.g., DocumentUploaded)

### Integrations Architecture
- Honest integration interface (no fake connections)
- Pluggable adapters (Generic REST architecture-ready)
- Admin UI to view integration status and test connections

### Error Handling
- Consistent JSON error envelope across the entire API
- Proper validation error mapping (422)
- Graceful 500 fallback without exposing stack traces

### Workflow Automation"""

content = content.replace(anchor, new_sections, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: Added Event, Integrations, and Error Handling to README")
