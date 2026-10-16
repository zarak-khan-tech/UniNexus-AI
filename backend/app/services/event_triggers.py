# English: Event → Workflow bridge. Listens to every event and fires any
# active workflow whose trigger_type == 'event' and config.event_type matches.
# Roman Urdu: Event → Workflow bridge. Har event ko sunta hai aur un active
# workflows ko fire karta hai jinka trigger_type == 'event' aur config.event_type match kare.

import json
import logging

from backend.app.core.events import Event, event_bus

logger = logging.getLogger(__name__)


def _run_matching_workflows(event: Event) -> int:
    """
    English: Find active event-triggered workflows for this tenant, match on
    trigger_config_json['event_type'], and run them.
    Roman Urdu: Is tenant ke active event-triggered workflows dhoondo,
    trigger_config_json['event_type'] se match karo, aur unhe run karo.
    """
    # English: Imports inside function to avoid circulars at module load.
    # Roman Urdu: Imports function ke andar — module load pe circulars se bachne ke liye.
    from backend.app.core.database import SessionLocal
    from backend.app.models.workflow import Workflow
    from backend.app.services.workflow_engine import run_workflow

    db = SessionLocal()
    triggered = 0
    try:
        workflows = (
            db.query(Workflow)
            .filter(
                Workflow.tenant_id == event.tenant_id,
                Workflow.is_active == True,  # noqa: E712
                Workflow.trigger_type == 'event',
            )
            .all()
        )
        for wf in workflows:
            try:
                cfg = json.loads(wf.trigger_config_json or '{}')
            except Exception:
                cfg = {}
            if cfg.get('event_type') != event.event_type:
                continue
            # English: Inject event payload into the workflow config so the
            # engine can pass it through to the action.
            # Roman Urdu: Event payload workflow config mein daalo taake engine
            # action tak pass kar sake.
            cfg['event_payload'] = event.payload
            wf.trigger_config_json = json.dumps(cfg)
            try:
                run_workflow(wf)
                triggered += 1
            except Exception as e:
                logger.error(f"[event_triggers] workflow {wf.id} failed: {e}")
    finally:
        db.close()

    logger.info(
        f"[event_triggers] event={event.event_type} tenant={event.tenant_id} "
        f"triggered={triggered}"
    )
    return triggered


def register_event_triggers() -> None:
    """
    English: Subscribe the workflow-matching handler to every event. Called once
    during app startup.
    Roman Urdu: Workflow-matching handler ko har event pe subscribe karo.
    Startup pe ek dafa call hota hai.
    """
    def handler(event: Event) -> None:
        _run_matching_workflows(event)

    # English: '*' subscribes to all event types.
    # Roman Urdu: '*' sab event types pe subscribe karta hai.
    event_bus.subscribe('*', handler)
    logger.info("[event_triggers] workflow auto-trigger registered on '*'")
