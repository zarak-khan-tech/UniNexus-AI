"""
English: Tools registry API — reads from DB, supports admin toggle.
Roman Urdu: Tools registry API — DB se padhta hai, admin toggle support.
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.app.api.deps import get_current_active_user
from backend.app.api.roles import require_role, ADMIN_ROLES
from backend.app.models.user import User
from backend.app.services.tool_definitions import (
    list_tool_definitions,
    count_tools_by_permission,
    update_tool_definition,
)
from backend.app.tools import tool_registry

router = APIRouter(prefix='/tools', tags=['Tools'])


class ToolDefinitionUpdate(BaseModel):
    description: Optional[str] = None
    permission: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None


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
        counts = {
            'total': len(tools),
            'read': sum(1 for t in tools if t['permission'] == 'read'),
            'write_low': sum(1 for t in tools if t['permission'] == 'write_low'),
            'write_high': sum(1 for t in tools if t['permission'] == 'write_high'),
        }
    return {'counts': counts, 'tools': tools}


@router.patch('/definitions/{tool_name}')
def patch_tool_definition(
    tool_name: str,
    body: ToolDefinitionUpdate,
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
):
    updates = {k: v for k, v in body.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail='No fields to update')
    row = update_tool_definition(current_user.tenant_id, tool_name, updates)
    if not row:
        raise HTTPException(status_code=404, detail=f'Tool definition not found: {tool_name}')
    return {'ok': True, 'definition': row}
