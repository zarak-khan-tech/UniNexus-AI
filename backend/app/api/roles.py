"""
English: Role-based access helpers. Endpoints declare which roles are allowed.
Roman Urdu: Role-based access helpers. Endpoints batate hain kaunse roles allow hain.
"""
import logging
from typing import List
from fastapi import Depends, HTTPException, status
from backend.app.api.deps import get_current_active_user
from backend.app.models.user import User

logger = logging.getLogger(__name__)

# English: Canonical role names used across the platform.
# Roman Urdu: Platform mein use hone wale canonical role names.
VALID_ROLES = ('super_admin', 'admin', 'faculty', 'student', 'staff')

# English: Which roles are allowed to perform administrative configuration.
# Roman Urdu: Kaunse roles administrative configuration kar sakte hain.
ADMIN_ROLES = ('super_admin', 'admin')


def require_role(*allowed_roles: str):
    """
    English: Returns a FastAPI dependency that blocks the request with 403
             unless the current user's role is in `allowed_roles`.
    Roman Urdu: Ek FastAPI dependency return karta hai jo request ko 403 se
                block karta hai agar user ka role `allowed_roles` mein na ho.

    Usage:
        @router.put('/x', dependencies=[Depends(require_role('admin'))])
        # or
        def endpoint(user: User = Depends(require_role('admin'))): ...
    """
    allowed_set = set(allowed_roles)

    def _checker(current_user: User = Depends(get_current_active_user)) -> User:
        role = (current_user.role or '').lower().strip()
        if role not in allowed_set:
            logger.warning(
                f"Access denied for {current_user.email} (role={role}) — "
                f"needs one of {sorted(allowed_set)}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of these roles: {sorted(allowed_set)}",
            )
        return current_user

    return _checker
