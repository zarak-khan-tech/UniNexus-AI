"""
English: Quick fix — /agents/list returns ALL agents (active + paused) so the UI
         can display disabled ones with a Paused state.
Roman Urdu: Fix — /agents/list saare agents return kare (active + paused) taake
            UI disabled ko Paused state mein dikha sake.
"""
# Read, modify, write agents.py in one pass.
path = "backend/app/api/agents.py"
with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()

old = '''@router.get('/list')
def list_registered_agents(
    current_user: User = Depends(get_current_active_user),
):
    # English: Read from DB, not hardcoded class list.
    # Roman Urdu: DB se padho, hardcoded class list nahi.
    return {'agents': list_agent_definitions(current_user.tenant_id, active_only=True)}'''

new = '''@router.get('/list')
def list_registered_agents(
    include_inactive: bool = True,
    current_user: User = Depends(get_current_active_user),
):
    # English: Return all agents by default so the UI can show disabled ones
    #          with a "Paused" state. Callers can pass ?include_inactive=false
    #          to filter to only active.
    # Roman Urdu: Default mein saare agents return karo taake UI disabled ko
    #             "Paused" state mein dikha sake. Filter ke liye
    #             ?include_inactive=false pass karo.
    return {'agents': list_agent_definitions(current_user.tenant_id, active_only=not include_inactive)}'''

if old not in content:
    print("ERROR: pattern not found in agents.py — the file may have changed.")
    raise SystemExit(1)

content = content.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: /agents/list now includes inactive agents by default")
