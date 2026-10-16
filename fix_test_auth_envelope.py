"""
English: Update test_auth.py to use the new error envelope shape.
Roman Urdu: test_auth.py ko naye error envelope shape ke saath compatible banao.
"""
path = "tests/test_auth.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "assert 'already registered' in response.json()['detail'].lower()"
new = """body = response.json()
    msg = body.get('error', {}).get('message', '') or body.get('detail', '')
    assert 'already registered' in msg.lower()"""

if old not in content:
    print("ERROR: old assertion not found — paste test_auth.py head lines")
    raise SystemExit(1)

content = content.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("FIXED: test_auth.py updated for new error envelope")
