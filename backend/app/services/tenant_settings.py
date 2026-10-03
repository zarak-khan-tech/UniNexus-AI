"""
English: Helper to read a tenant's settings JSON. Returns {} if tenant not found
         or settings are empty. All callers should fall back to sensible defaults.
Roman Urdu: Tenant ki settings JSON padhne ka helper. Agar tenant na mile ya
            settings khali ho to {} return karta hai. Caller ko default use karna chahiye.
"""
import json
import logging
from typing import Dict, Any, Optional
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant

logger = logging.getLogger(__name__)


def get_tenant_settings(tenant_id: Optional[int]) -> Dict[str, Any]:
    """English: Load and parse a tenant's settings JSON.
    Roman Urdu: Tenant ki settings JSON load aur parse karo."""
    if not tenant_id:
        return {}
    db = SessionLocal()
    try:
        t = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not t:
            return {}
        try:
            return json.loads(t.settings_json or '{}')
        except Exception as e:
            logger.error(f'Failed to parse tenant {tenant_id} settings: {e}')
            return {}
    finally:
        db.close()
