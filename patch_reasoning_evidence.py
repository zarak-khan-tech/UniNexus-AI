# English: Patch BASE_PROMPT to add evidence-quality handling rules.
# Roman Urdu: BASE_PROMPT mein evidence-quality handling rules add karo.
path = "backend/app/core/reasoning.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''ANTI-HALLUCINATION:
- If a fact is NOT in the tool results, DO NOT invent it.
- When stating a policy, QUOTE or closely paraphrase the actual text.
- Always cite the source by title.'''

new_block = '''ANTI-HALLUCINATION:
- If a fact is NOT in the tool results, DO NOT invent it.
- When stating a policy, QUOTE or closely paraphrase the actual text.
- Always cite the source by title.

EVIDENCE QUALITY (from semantic_search results):
Every semantic_search result includes an "evidence_quality" field:
- "strong"  → answer confidently, quote directly, cite the document.
- "weak"    → answer cautiously: "Based on related material, it appears that... 
              but I could not find a document that directly addresses this. 
              Please verify with the registrar."
- "none"    → do NOT answer from general knowledge. Say: "I could not find 
              relevant information in the university's knowledge base. 
              Please check with the appropriate office."
NEVER invent policies or rules when evidence is weak or missing.'''

if old_block not in content:
    print("ERROR: anchor block not found in reasoning.py")
    raise SystemExit(1)

content = content.replace(old_block, new_block, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: reasoning.py BASE_PROMPT updated with evidence-quality rules")
