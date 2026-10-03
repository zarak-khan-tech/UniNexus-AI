"""
English: Tenant settings API — read and update university-level configuration.
Roman Urdu: Tenant settings API — university-level configuration read/update.
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.tenant import Tenant

router = APIRouter(prefix='/tenant', tags=['Tenant'])


@router.get('/settings')
def get_settings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    t = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if not t:
        raise HTTPException(status_code=404, detail='Tenant not found')
    try:
        settings = json.loads(t.settings_json or '{}')
    except Exception:
        settings = {}
    return {
        'tenant_id': t.id,
        'name': t.name,
        'domain': t.domain,
        'settings': settings,
    }


class SettingsUpdate(BaseModel):
    settings: dict


@router.put('/settings')
def update_settings(
    body: SettingsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    t = db.query(Tenant).filter(Tenant.id == current_user.tenant_id).first()
    if not t:
        raise HTTPException(status_code=404, detail='Tenant not found')
    try:
        current = json.loads(t.settings_json or '{}')
    except Exception:
        current = {}
    current.update(body.settings or {})
    t.settings_json = json.dumps(current)
    db.commit()
    return {'ok': True, 'settings': current}
