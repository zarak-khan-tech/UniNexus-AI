"""
English: Small helper to create notifications from anywhere in the code.
Roman Urdu: Chhota helper jo kahin se bhi notification create kare.
"""
import logging
from typing import Optional
from backend.app.core.database import SessionLocal
from backend.app.models.notification import Notification

logger = logging.getLogger(__name__)


def create_notification(
    tenant_id: int,
    user_id: int,
    kind: str,
    title: str,
    body: str,
    action_url: Optional[str] = None,
) -> Optional[int]:
    if not tenant_id or not user_id:
        return None
    db = SessionLocal()
    try:
        n = Notification(
            tenant_id=tenant_id,
            user_id=user_id,
            kind=kind,
            title=title,
            body=body,
            action_url=action_url,
            is_read=False,
        )
        db.add(n)
        db.commit()
        db.refresh(n)
        return n.id
    except Exception as e:
        logger.error(f'Failed to create notification: {e}')
        return None
    finally:
        db.close()
