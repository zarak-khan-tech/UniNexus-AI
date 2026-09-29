"""
English: Notifications API — list, mark-read, unread-count.
Roman Urdu: Notifications API — list, mark-read, unread-count.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.notification import Notification

router = APIRouter(prefix='/notifications', tags=['Notifications'])


@router.get('')
def list_notifications(
    status: str = 'all',
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    q = db.query(Notification).filter(Notification.tenant_id == current_user.tenant_id)
    if status == 'unread':
        q = q.filter(Notification.is_read == False)
    elif status == 'read':
        q = q.filter(Notification.is_read == True)
    rows = q.order_by(Notification.created_at.desc()).limit(limit).all()
    unread = db.query(Notification).filter(
        Notification.tenant_id == current_user.tenant_id,
        Notification.is_read == False,
    ).count()
    return {
        'total': len(rows),
        'unread_count': unread,
        'notifications': [
            {
                'id': r.id,
                'kind': r.kind,
                'title': r.title,
                'body': r.body,
                'action_url': r.action_url,
                'is_read': r.is_read,
                'created_at': r.created_at.isoformat(),
            }
            for r in rows
        ],
    }


@router.get('/unread-count')
def unread_count(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    n = db.query(Notification).filter(
        Notification.tenant_id == current_user.tenant_id,
        Notification.is_read == False,
    ).count()
    return {'unread_count': n}


@router.post('/{notification_id}/read')
def mark_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    n = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.tenant_id == current_user.tenant_id,
    ).first()
    if not n:
        raise HTTPException(status_code=404, detail='Notification not found')
    n.is_read = True
    db.commit()
    return {'ok': True}


@router.post('/read-all')
def mark_all_read(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db.query(Notification).filter(
        Notification.tenant_id == current_user.tenant_id,
        Notification.is_read == False,
    ).update({'is_read': True})
    db.commit()
    return {'ok': True}
