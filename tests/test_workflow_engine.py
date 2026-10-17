"""
English: Unit tests for the workflow engine.
Roman Urdu: Workflow engine ke liye unit tests.
"""
import json
import pytest
from backend.app.services.workflow_engine import run_workflow
from backend.app.models.workflow import Workflow


def test_workflow_log_only_fires(db_session):
    """A log_only workflow should fire and return ok=True."""
    wf = Workflow(
        tenant_id=1,
        user_id=1,
        name="Test Log Workflow",
        description="test",
        trigger_type="event",
        trigger_config_json=json.dumps({"event_type": "TestEvent"}),
        action_type="log_only",
        action_config_json=json.dumps({}),
        is_active=True,
    )
    db_session.add(wf)
    db_session.commit()
    db_session.refresh(wf)

    result = run_workflow(wf)
    assert result["fired"] is True
    assert result["result"]["ok"] is True
    assert result["result"]["logged"] is True


def test_workflow_unknown_action_fails_gracefully(db_session):
    """An unknown action should return ok=False, not crash."""
    wf = Workflow(
        tenant_id=1,
        user_id=1,
        name="Bad Action Workflow",
        description="test",
        trigger_type="event",
        trigger_config_json=json.dumps({"event_type": "TestEvent"}),
        action_type="does_not_exist",
        action_config_json=json.dumps({}),
        is_active=True,
    )
    db_session.add(wf)
    db_session.commit()
    db_session.refresh(wf)

    result = run_workflow(wf)
    # It should still have "fired": True because the event matched,
    # but the action fails gracefully.
    assert result["fired"] is True
    assert result["result"]["ok"] is False
    assert "Unknown action" in result["result"]["error"]


def test_workflow_unknown_trigger_skips(db_session):
    """An unknown trigger should not fire."""
    wf = Workflow(
        tenant_id=1,
        user_id=1,
        name="Bad Trigger Workflow",
        description="test",
        trigger_type="invalid_trigger_type",
        trigger_config_json=json.dumps({}),
        action_type="log_only",
        action_config_json=json.dumps({}),
        is_active=True,
    )
    db_session.add(wf)
    db_session.commit()
    db_session.refresh(wf)

    result = run_workflow(wf)
    assert result["fired"] is False
    assert "unknown trigger" in result["reason"]
