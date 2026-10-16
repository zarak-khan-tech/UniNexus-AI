# English: Insert a small stats row in each agent card.
# Roman Urdu: Har agent card mein chhota stats row add karo.
path = "src/pages/Agents.jsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """      {/* Footer */}
      <div className="pt-4 border-t border-ink-100 flex items-center justify-between gap-3">"""
new = """      {/* Health Stats */}
      {(() => {
        const h = health[agent.name];
        if (!h || h.runs === 0) {
          return (
            <div className="text-[11px] text-ink-400 italic mb-3">
              No executions yet
            </div>
          );
        }
        return (
          <div className="grid grid-cols-3 gap-2 mb-4 pt-3 border-t border-ink-100">
            <div>
              <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-0.5">Runs</div>
              <div className="text-sm font-mono font-bold text-ink-900">{h.runs}</div>
            </div>
            <div>
              <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-0.5">Success</div>
              <div className={`text-sm font-mono font-bold ${h.success_rate >= 95 ? 'text-emerald-700' : h.success_rate >= 80 ? 'text-amber-700' : 'text-red-700'}`}>
                {h.success_rate}%
              </div>
            </div>
            <div>
              <div className="text-[10px] uppercase tracking-widest text-ink-500 font-bold mb-0.5">Last used</div>
              <div className="text-[11px] text-ink-700 truncate">
                {h.last_used ? new Date(h.last_used).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '—'}
              </div>
            </div>
          </div>
        );
      })()}

      {/* Footer */}
      <div className="pt-4 border-t border-ink-100 flex items-center justify-between gap-3">"""
if old not in content:
    print("ERROR: Footer anchor not found")
    raise SystemExit(1)
content = content.replace(old, new, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: agent cards now display health stats")
