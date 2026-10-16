"""
English: Fix corrupted /integrations route line — replace with proper Guarded route.
Roman Urdu: Corrupted /integrations route line fix karo — proper Guarded route ke saath.
"""
path = "src/App.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Broken line produced by the previous patch
broken = '<Route path="/integrations" element={<Integrations />} /></Guarded>} />'
fixed = '<Route path="/integrations" element={<Guarded roles={[\'admin\', \'super_admin\']}><Integrations /></Guarded>} />'

if broken in content:
    content = content.replace(broken, fixed, 1)
    print("FIXED: corrupted integrations route replaced")
elif fixed in content:
    print("SKIP: route already correct")
else:
    print("ERROR: neither broken nor fixed route found — paste App.jsx line 45-60")
    raise SystemExit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
