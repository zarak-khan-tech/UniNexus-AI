# English: Add /audit/:id route.
# Roman Urdu: /audit/:id route add karo.
path = "src/App.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Import
old_imp = "import AuditLogs from './pages/AuditLogs';"
new_imp = "import AuditLogs from './pages/AuditLogs';\nimport ExecutionDetail from './pages/ExecutionDetail';"
if old_imp not in content:
    print("ERROR: AuditLogs import anchor not found")
    raise SystemExit(1)
content = content.replace(old_imp, new_imp, 1)

# Route — after /audit route
old_route = '<Route path="/audit" element={<Guarded roles={[\'admin\', \'super_admin\', \'faculty\']}><AuditLogs /></Guarded>} />'
new_route = old_route + '\n          <Route path="/audit/:id" element={<Guarded roles={[\'admin\', \'super_admin\', \'faculty\']}><ExecutionDetail /></Guarded>} />'
if old_route not in content:
    print("ERROR: /audit route anchor not found")
    raise SystemExit(1)
content = content.replace(old_route, new_route, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: App.jsx route /audit/:id added")
