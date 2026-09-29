"""
English: Test notifications - trigger approval + notification flow.
Roman Urdu: Notifications test karo - approval create karo phir approve karo.
"""
from backend.app.core.reasoning import reason

print("=" * 70)
print("STEP 1: Trigger high-risk action -> approval + notification")
print("=" * 70)
r = reason(
    "Change Sara Ahmed's MATH101 grade to B+",
    user_id=1,
    user_email="admin@demo.university.edu",
    tenant_id=1,
)
print("Answer:", r.get("answer"))
print("Approval ID:", r.get("pending_approval_id"))
print()

print("=" * 70)
print("STEP 2: Check notifications table")
print("=" * 70)
from backend.app.core.database import SessionLocal
from backend.app.models.notification import Notification
db = SessionLocal()
try:
    rows = db.query(Notification).order_by(Notification.created_at.desc()).limit(10).all()
    print(f"Total notifications: {db.query(Notification).count()}")
    for n in rows:
        print(f"  [{n.kind:10}] {n.title}")
        print(f"    {n.body}")
        print(f"    read={n.is_read}  url={n.action_url}")
finally:
    db.close()
