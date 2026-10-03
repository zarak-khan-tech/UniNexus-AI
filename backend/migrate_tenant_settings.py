"""
English: One-time migration — add settings_json column to tenants table.
Roman Urdu: Ek dafa ka migration — tenants table mein settings_json column add karo.
"""
import json
from sqlalchemy import inspect, text
from backend.app.core.database import engine, SessionLocal
from backend.app.models.tenant import Tenant

DEFAULT_SETTINGS = {
    'university_name': 'Demo University',
    'attendance_threshold': 75,
    'risk_high_threshold': 60,
    'risk_medium_threshold': 75,
    'enabled_agents': [
        'AttendanceAgent', 'PolicyAgent', 'RiskAgent', 'KnowledgeAgent',
    ],
    'enabled_tools': [
        'student_lookup', 'list_students', 'attendance_query',
        'list_enrollments', 'semantic_search',
        'send_student_notification', 'update_student_grade',
    ],
}

inspector = inspect(engine)
cols = [c['name'] for c in inspector.get_columns('tenants')]

if 'settings_json' not in cols:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE tenants ADD COLUMN settings_json TEXT NOT NULL DEFAULT '{}'"))
        conn.commit()
    print("OK: added settings_json column")
else:
    print("SKIP: settings_json column already exists")

db = SessionLocal()
try:
    updated = 0
    for t in db.query(Tenant).all():
        if not t.settings_json or t.settings_json.strip() in ('', '{}'):
            t.settings_json = json.dumps(DEFAULT_SETTINGS)
            updated += 1
    db.commit()
    print(f"OK: backfilled defaults for {updated} tenant(s)")
    print(f"Total tenants: {db.query(Tenant).count()}")
finally:
    db.close()
