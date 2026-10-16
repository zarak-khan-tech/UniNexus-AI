"""
English: Add Integrations link to sidebar, right after Settings.
Roman Urdu: Settings ke baad sidebar mein Integrations link add karo.
"""
path = "src/components/Layout.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "{ name: 'Settings', path: '/settings', roles: ['admin', 'super_admin'] },"
new = old + "\n      { name: 'Integrations', path: '/integrations', roles: ['admin', 'super_admin'] },"

if "/integrations" in content:
    print("SKIP: integrations link already present")
else:
    if old not in content:
        print("ERROR: Settings nav item anchor not found")
        raise SystemExit(1)
    content = content.replace(old, new, 1)
    print("FIXED: Integrations link added to sidebar")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
