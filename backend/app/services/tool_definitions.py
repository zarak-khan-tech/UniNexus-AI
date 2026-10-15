"""
English: Service helpers for tool definitions — DB read + update.
Roman Urdu: Tool definitions ke services helpers — DB read + update.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from backend.app.core.database import SessionLocal
from backend.app.models.tool_definition import ToolDefinition

logger = logging.getLogger(__name__)


def _to_dict(row: ToolDefinition) -> Dict[str, Any]:
    try:
        schema = json.loads(row.input_schema_json or '{}')
    except Exception:
        schema = {}
    return {
        'name': row.name,
        'description': row.description,
        'permission': row.permission,
        'input_schema': schema,
        'version': row.version,
        'is_active': row.is_active,
    }


def list_tool_definitions(tenant_id: int, active_only: bool = True) -> List[Dict[str, Any]]:
    """English: Return all tool definitions for a tenant.
    Roman Urdu: Tenant ke saare tool definitions return karo."""
    db = SessionLocal()
    try:
        q = db.query(ToolDefinition).filter(ToolDefinition.tenant_id == tenant_id)
        if active_only:
            q = q.filter(ToolDefinition.is_active == True)
        return [_to_dict(r) for r in q.order_by(ToolDefinition.name).all()]
    finally:
        db.close()


def update_tool_definition(tenant_id: int, name: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """English: Update description/permission/is_active/version for one tool.
    Roman Urdu: Ek tool ka description/permission/is_active/version update karo."""
    db = SessionLocal()
    try:
        row = db.query(ToolDefinition).filter(
            ToolDefinition.tenant_id == tenant_id,
            ToolDefinition.name == name,
        ).first()
        if not row:
            return None
        if 'description' in updates and updates['description'] is not None:
            row.description = str(updates['description'])
        if 'permission' in updates and updates['permission'] is not None:
            row.permission = str(updates['permission'])
        if 'input_schema' in updates and isinstance(updates['input_schema'], dict):
            row.input_schema_json = json.dumps(updates['input_schema'])
        if 'version' in updates and updates['version'] is not None:
            row.version = str(updates['version'])
        if 'is_active' in updates and isinstance(updates['is_active'], bool):
            row.is_active = updates['is_active']
        db.commit()
        db.refresh(row)
        return _to_dict(row)
    finally:
        db.close()


def count_tools_by_permission(tenant_id: int) -> Dict[str, int]:
    """English: Return counts per permission level for a tenant.
    Roman Urdu: Tenant ke liye permission level wise counts."""
    db = SessionLocal()
    try:
        rows = db.query(ToolDefinition).filter(ToolDefinition.tenant_id == tenant_id).all()
        out = {'total': len(rows), 'read': 0, 'write_low': 0, 'write_high': 0}
        for r in rows:
            if r.permission in out:
                out[r.permission] += 1
        return out
    finally:
        db.close()
