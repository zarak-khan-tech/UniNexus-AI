"""
English: Test the human-approval flow with a high-risk action.
Roman Urdu: Human-approval flow test karo high-risk action ke saath.
"""
from backend.app.core.reasoning import reason

print("=" * 70)
print("TEST: High-risk action (grade update)")
print("=" * 70)
r = reason(
    "Change Ali Khan's MATH101 grade to A+",
    user_id=1,
    user_email="admin@demo.university.edu",
    tenant_id=1,
)
print("Answer:", r.get("answer"))
print()
print("Tool calls:")
for tc in r.get("tool_calls", []):
    print(f"  [{tc['iteration']}] {tc['tool']}({tc['args']})")
    print(f"    queued_for_approval: {tc['summary'].get('queued_for_approval', False)}")
    print(f"    approval_id: {tc['summary'].get('approval_id', '-')}")
print()
print("Pending approval ID:", r.get("pending_approval_id"))
