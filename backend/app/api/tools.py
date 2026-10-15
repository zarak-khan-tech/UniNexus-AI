"""
English: Tools registry API — reads from DB, falls back to class-level 
registry if the tenant has no rows yet (e.g. before migration).
Roman Urdu: Tools registry API — DB se padhta hai, agar tenant ke rows 
na hon to class-level registry fallback.
"""
from fastapi import APIRouter, Depends
from backend.app.api.deps import get_current_active_user
from backend.app.models.user import User
from backend.app.services.tool_definitions import (
    list_tool_definitions,
    count_tools_by_permission,
)
from backend.app.tools import tool_registry

router = APIRouter(prefix='/tools', tags=['Tools'])


@router.get('')
def list_tools(current_user: User = Depends(get_current_active_user)):
    # English: Prefer DB rows; fall back to class registry if none exist.
    # Roman Urdu: DB rows prefer karo; agar koi na ho to class registry.
    db_tools = list_tool_definitions(current_user.tenant_id, active_only=False)
    if db_tools:
        tools = db_tools
    else:
        tools = tool_registry.list()

    counts = count_tools_by_permission(current_user.tenant_id)
    if counts.get('total', 0) == 0:
        # English: Fallback counts from class registry.
        # Roman Urdu: Fallback counts class registry se.
        counts = {
            'total': len(tools),
            'read': sum(1 for t in tools if t['permission'] == 'read'),
            'write_low': sum(1 for t in tools if t['permission'] == 'write_low'),
            'write_high': sum(1 for t in tools if t['permission'] == 'write_high'),
        }
    return {'counts': counts, 'tools': tools}
