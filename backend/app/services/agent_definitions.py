"""
English: Service helpers for agent definitions — DB read + update.
Roman Urdu: Agent definitions ke services helpers — DB read + update.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from backend.app.core.database import SessionLocal
from backend.app.models.agent_definition import AgentDefinition

logger = logging.getLogger(__name__)


def _to_dict(row: AgentDefinition) -> Dict[str, Any]:
    try:
        caps = json.loads(row.capabilities_json or '[]')
    except Exception:
        caps = []
    try:
        tools = json.loads(row.supported_tools_json or '[]')
    except Exception:
        tools = []
    return {
        'name': row.name,
        'description': row.description,
        'capabilities': caps,
        'supported_tools': tools,
        'version': row.version,
        'is_active': row.is_active,
        'status': row.status,
    }


def list_agent_definitions(tenant_id: int, active_only: bool = True) -> List[Dict[str, Any]]:
    """English: Return all agent definitions for a tenant.
    Roman Urdu: Tenant ke saare agent definitions return karo."""
    db = SessionLocal()
    try:
        q = db.query(AgentDefinition).filter(AgentDefinition.tenant_id == tenant_id)
        if active_only:
            q = q.filter(AgentDefinition.is_active == True)
        return [_to_dict(r) for r in q.order_by(AgentDefinition.name).all()]
    finally:
        db.close()


def update_agent_definition(tenant_id: int, name: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """English: Update description/capabilities/is_active/status for one agent.
    Roman Urdu: Ek agent ka description/capabilities/is_active/status update karo."""
    db = SessionLocal()
    try:
        row = db.query(AgentDefinition).filter(
            AgentDefinition.tenant_id == tenant_id,
            AgentDefinition.name == name,
        ).first()
        if not row:
            return None
        if 'description' in updates and updates['description'] is not None:
            row.description = str(updates['description'])
        if 'capabilities' in updates and isinstance(updates['capabilities'], list):
            row.capabilities_json = json.dumps(updates['capabilities'])
        if 'supported_tools' in updates and isinstance(updates['supported_tools'], list):
            row.supported_tools_json = json.dumps(updates['supported_tools'])
        if 'version' in updates and updates['version'] is not None:
            row.version = str(updates['version'])
        if 'is_active' in updates and isinstance(updates['is_active'], bool):
            row.is_active = updates['is_active']
        if 'status' in updates and updates['status'] is not None:
            row.status = str(updates['status'])
        db.commit()
        db.refresh(row)
        return _to_dict(row)
    finally:
        db.close()
