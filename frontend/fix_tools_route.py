"""
English: Fix the broken /tools route line — missing closing tags.
Roman Urdu: Tooti hui /tools route line fix karo — closing tags missing hain.
"""
path = "src/App.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

broken = """<Route path="/tools" element={<Guarded roles={['admin', 'super_admin', 'faculty']}><Tools />"""
fixed = """<Route path="/tools" element={<Guarded roles={['admin', 'super_admin', 'faculty']}><Tools /></Guarded>} />"""

if fixed in content:
    print("SKIP: /tools route already correct")
elif broken in content:
    content = content.replace(broken, fixed, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("FIXED: /tools route closing tags restored")
else:
    print("ERROR: broken /tools line not found — paste App.jsx lines 48-52")
