"""
English: Tools registry API — read-only listing of all registered tools.
Roman Urdu: Tools registry API — sab registered tools ki read-only listing.
"""
from fastapi import APIRouter, Depends
from backend.app.api.deps import get_current_active_user
from backend.app.models.user import User
from backend.app.tools import tool_registry
from backend.app.tools.base import PermissionLevel

router = APIRouter(prefix='/tools', tags=['Tools'])


@router.get('')
def list_tools(current_user: User = Depends(get_current_active_user)):
    """English: List every tool with its permission level and schema.
    Roman Urdu: Har tool ko permission level aur schema ke saath list karo."""
    all_tools = tool_registry.list()
    counts = {
        'total': len(all_tools),
        'read': sum(1 for t in all_tools if t['permission'] == PermissionLevel.READ.value),
        'write_low': sum(1 for t in all_tools if t['permission'] == PermissionLevel.WRITE_LOW.value),
        'write_high': sum(1 for t in all_tools if t['permission'] == PermissionLevel.WRITE_HIGH.value),
    }
    return {'counts': counts, 'tools': all_tools}
