"""
English: Verify events publish from document upload + show up in history API.
Roman Urdu: Document upload se events publish hote hain + history API mein aate hain verify karo.
"""
import json
import requests
from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import create_access_token

db = SessionLocal()
u = db.query(User).filter(User.role == 'admin').first()
token = create_access_token(data={'sub': u.email, 'role': u.role, 'tenant_id': u.tenant_id})
db.close()
h = {'Authorization': 'Bearer ' + token}

print("=" * 60)
print("Test 1: History before upload")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/events/history', headers=h)
print(f"Status: {r.status_code}")
print(f"Count: {r.json().get('count')}")

print()
print("=" * 60)
print("Test 2: Upload a document -> event should publish")
print("=" * 60)
unique_title = "Event Test Doc 1"

# Delete previous if exists (direct DB)
import sqlite3
try:
    conn = sqlite3.connect('uninexus.db')
    conn.execute("DELETE FROM documents WHERE title = ?", (unique_title,))
    conn.commit()
    conn.close()
except Exception as e:
    print(f"(DB cleanup skipped: {e})")

policy_text = "Event test policy. This document verifies the event bus works."
files = {'file': ('event_test.txt', policy_text, 'text/plain')}
data = {'title': unique_title, 'category': 'Policy'}
r = requests.post(
    'http://127.0.0.1:8000/documents/upload',
    headers=h, files=files, data=data,
)
print(f"Upload status: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)}")

print()
print("=" * 60)
print("Test 3: History now shows DocumentUploaded")
print("=" * 60)
r = requests.get('http://127.0.0.1:8000/events/history', headers=h)
data = r.json()
print(f"Count: {data.get('count')}")
for e in data.get('events', []):
    print(f"  - {e['event_type']} | tenant={e['tenant_id']} | payload_keys={list(e['payload'].keys())}")
