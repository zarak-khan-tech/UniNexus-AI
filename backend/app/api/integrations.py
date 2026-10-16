# English: Integrations API — list registered integrations with honest status.
# Roman Urdu: Integrations API — registered integrations honest status ke saath list karo.

from fastapi import APIRouter, Depends
from backend.app.api.roles import require_role, ADMIN_ROLES
from backend.app.models.user import User
from backend.app.integrations.registry import registry

router = APIRouter(prefix='/integrations', tags=['Integrations'])


@router.get('')
def list_integrations(current_user: User = Depends(require_role(*ADMIN_ROLES))):
    """
    English: Return all registered integrations. Each entry carries an honest
    status (implemented / locally_simulated / architecture_ready / planned).
    Roman Urdu: Saare registered integrations return karo. Har entry ke saath
    honest status (implemented / locally_simulated / architecture_ready / planned).
    """
    infos = registry.list()
    return {
        'count': len(infos),
        'integrations': [
            {
                'name': i.name,
                'display_name': i.display_name,
                'status': i.status.value,
                'description': i.description,
                'capabilities': i.capabilities,
                'requires_credentials': i.requires_credentials,
                'docs_url': i.docs_url,
            }
            for i in infos
        ],
    }


@router.post('/{name}/test')
def test_integration(name: str, current_user: User = Depends(require_role(*ADMIN_ROLES))):
    """
    English: Ask an integration to test its connection. Honest adapters return
    ok=False when not configured; they never fake a success.
    Roman Urdu: Integration ko connection test karne ko kaho. Honest adapters
    ok=False return karte hain jab configured na hon; kabhi fake success nahi.
    """
    adapter = registry.get(name)
    if not adapter:
        return {'ok': False, 'message': f"Integration '{name}' not registered."}
    try:
        return adapter.test_connection()
    except NotImplementedError as e:
        return {'ok': False, 'message': str(e)}
