# English: Events API — read-only view of the in-process event history.
# Roman Urdu: Events API — in-process event history ka read-only view.

from fastapi import APIRouter, Depends, Query
from typing import Optional
from backend.app.api.roles import require_role, ADMIN_ROLES
from backend.app.models.user import User
from backend.app.core.events import event_bus

router = APIRouter(prefix='/events', tags=['Events'])


@router.get('/history')
def get_event_history(
    event_type: Optional[str] = Query(None, description='Filter by event type'),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(require_role(*ADMIN_ROLES)),
):
    """
    English: Return recent events for the current tenant, optionally filtered by type.
    Roman Urdu: Current tenant ke recent events return karo, optionally type se filter.
    """
    events = event_bus.get_history(
        event_type=event_type,
        tenant_id=current_user.tenant_id,
        limit=limit,
    )
    return {
        'count': len(events),
        'events': [
            {
                'event_type': e.event_type,
                'tenant_id': e.tenant_id,
                'payload': e.payload,
                'timestamp': e.timestamp,
            }
            for e in events
        ],
    }
