"""
English: Test the real agentic reasoning loop.
Roman Urdu: Real agentic reasoning loop test karo.
"""
from backend.app.core.reasoning import reason

queries = [
    "what happens if I fail an exam?",
    "how much does a semester cost?",
    "which students have low attendance?",
    "hello, how are you?",
]

for q in queries:
    print()
    print('=' * 70)
    print('QUERY:', q)
    print('=' * 70)
    result = reason(q)
    print(f"Provider: {result.get('provider')} / {result.get('model')}")
    print(f"Iterations: {result.get('iterations')}")
    print(f"Tool calls: {len(result.get('tool_calls', []))}")
    for tc in result.get('tool_calls', []):
        print(f"  [iter {tc['iteration']}] {tc['tool']}({tc['args']})")
        print(f"    reasoning: {tc['reasoning']}")
        print(f"    result: {tc['summary']}")
    print()
    print('FINAL ANSWER:')
    print(result.get('answer'))
    print()
