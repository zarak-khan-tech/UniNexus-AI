"""
English: Test multi-turn conversation memory in the reasoning loop.
Roman Urdu: Reasoning loop mein multi-turn memory test karo.
"""
from backend.app.core.reasoning import reason

print("=" * 70)
print("TURN 1: show me students with low attendance")
print("=" * 70)
r1 = reason("show me students with low attendance")
print(r1.get("answer"))
print(f"(iterations: {r1.get('iterations')}, tools: {len(r1.get('tool_calls', []))})")
print()

history = [
    {"role": "user", "content": "show me students with low attendance"},
    {"role": "assistant", "content": r1.get("answer", "")},
]

print("=" * 70)
print("TURN 2: which of THEM might fail?  (uses 'them' — needs memory)")
print("=" * 70)
r2 = reason("which of them might fail?", history=history)
print(r2.get("answer"))
print(f"(iterations: {r2.get('iterations')}, tools: {len(r2.get('tool_calls', []))})")
print()

print("=" * 70)
print("TURN 3: how does that compare to the minimum threshold?  (uses 'that')")
print("=" * 70)
history.append({"role": "user", "content": "which of them might fail?"})
history.append({"role": "assistant", "content": r2.get("answer", "")})
r3 = reason("how does that compare to the minimum threshold?", history=history)
print(r3.get("answer"))
