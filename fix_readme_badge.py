"""
English: Update tests badge in README from 20 to 48.
Roman Urdu: README mein tests badge ko 20 se 48 karo.
"""
path = "README.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_badge = "tests-20%20passing-brightgreen"
new_badge = "tests-48%20passing-brightgreen"

if new_badge in content:
    print("SKIP: tests badge already updated to 48")
elif old_badge in content:
    content = content.replace(old_badge, new_badge, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("FIXED: tests badge updated to 48 passing")
else:
    print("ERROR: tests badge not found — check README.md top lines")
