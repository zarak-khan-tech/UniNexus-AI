# English: Read-modify-write — only replace the specific function so we don't
#          rewrite the whole file by hand.
# Roman Urdu: Read-modify-write — sirf target function replace karo, poori file nahi.

path = "backend/app/api/agents.py"
with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()

# 1. Add the import for require_role + ADMIN_ROLES
old_import = "from backend.app.api.deps import get_current_active_user\n"
new_import = (
    "from backend.app.api.deps import get_current_active_user\n"
    "from backend.app.api.roles import require_role, ADMIN_ROLES\n"
)
if old_import not in content:
    print("ERROR: deps import line not found")
    raise SystemExit(1)
content = content.replace(old_import, new_import, 1)

# 2. Replace the PATCH endpoint signature to require admin role
old_endpoint = """@router.patch('/definitions/{agent_name}')
def patch_agent_definition(
    agent_name: str,
    body: AgentDefinitionUpdate,
    current_user: User = Depends(get_current_active_user),
):"""

new_endpoint = """@router.patch('/definitions/{agent_name}')
def patch_agent_definition(
    agent_name: str,
    body: AgentDefinitionUpdate,
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
):"""

if old_endpoint not in content:
    print("ERROR: PATCH endpoint signature not found")
    raise SystemExit(1)
content = content.replace(old_endpoint, new_endpoint, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK: agents.py updated — PATCH now requires admin role")
