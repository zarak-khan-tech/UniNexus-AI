# English: Patch NAV_GROUPS to add Import under Operations (admin only).
# Roman Urdu: NAV_GROUPS mein Import add karo Operations ke neeche (sirf admin).
path = "src/components/Layout.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """  {
    label: 'Operations',
    items: [
      { name: 'Notifications', path: '/notifications' },
      { name: 'Audit Logs', path: '/audit', roles: ['admin', 'super_admin', 'faculty'] },
      { name: 'Settings', path: '/settings', roles: ['admin', 'super_admin'] },
    ],
  },"""

new = """  {
    label: 'Operations',
    items: [
      { name: 'Notifications', path: '/notifications' },
      { name: 'Audit Logs', path: '/audit', roles: ['admin', 'super_admin', 'faculty'] },
      { name: 'Import', path: '/import', roles: ['admin', 'super_admin'] },
      { name: 'Settings', path: '/settings', roles: ['admin', 'super_admin'] },
    ],
  },"""

if old not in content:
    print("ERROR: Operations block not found in Layout.jsx")
    raise SystemExit(1)

content = content.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: Layout.jsx updated with Import link")
