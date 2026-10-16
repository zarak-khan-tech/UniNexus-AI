# English: Add health stats fetching and display to Agents page.
# Roman Urdu: Agents page pe health stats fetch aur display add karo.
path = "src/pages/Agents.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add health state
old_state = "  const [agents, setAgents] = useState([]);"
new_state = "  const [agents, setAgents] = useState([]);\n  const [health, setHealth] = useState({});"
if old_state not in content:
    print("ERROR: agents state anchor not found")
    raise SystemExit(1)
content = content.replace(old_state, new_state, 1)

# 2. Fetch health in same function as fetchAgents
old_fetch = """      const response = await api.get('/agents/list');
      setAgents(response.data.agents || []);"""
new_fetch = """      const [listRes, healthRes] = await Promise.all([
        api.get('/agents/list'),
        api.get('/agents/health').catch(() => ({ data: { agents: [] } })),
      ]);
      setAgents(listRes.data.agents || []);
      const hMap = {};
      (healthRes.data.agents || []).forEach((h) => { hMap[h.agent] = h; });
      setHealth(hMap);"""
if old_fetch not in content:
    print("ERROR: fetch block anchor not found")
    raise SystemExit(1)
content = content.replace(old_fetch, new_fetch, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: Agents.jsx health stats wired")
