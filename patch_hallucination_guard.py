# English: Add a hallucination guard — if final_answer cites sources but no 
# sources were collected, force a retry with a nudge.
# Roman Urdu: Hallucination guard add karo — agar final_answer sources cite 
# kare lekin koi source collect na hua ho, to retry karo.
path = "backend/app/core/reasoning.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add helper function before `def reason(`
helper = '''
# English: Detect answers that cite sources even though no tool returned any.
# Roman Urdu: Aisi answers detect karo jo sources cite karein lekin koi tool 
# ne kuch return na kiya ho.
_HALLUCINATION_PHRASES = (
    'according to the',
    'per the university',
    'source:',
    'the university policy states',
    'the policy says',
    'as stated in the',
    'strong evidence',
)


def _looks_like_hallucination(answer: str, collected_sources: list) -> bool:
    """
    English: True if the answer cites sources/policies but we collected none.
    Roman Urdu: True agar answer sources/policies cite kare lekin humne koi 
    collect nahi kiya.
    """
    if collected_sources:
        return False
    lowered = (answer or '').lower()
    return any(p in lowered for p in _HALLUCINATION_PHRASES)


'''

# Insert helper before `def reason(`
marker = "def reason(user_request: str"
if marker not in content:
    print("ERROR: reason() function not found")
    raise SystemExit(1)
content = content.replace(marker, helper + marker, 1)

# Patch the final_answer block to add the guard
old_final = '''        if action == "final_answer":
            answer = (decision.get("answer") or "").strip()
            return {'''

new_final = '''        if action == "final_answer":
            answer = (decision.get("answer") or "").strip()

            # English: Hallucination guard — reject answers that cite 
            # sources when no sources were collected.
            # Roman Urdu: Hallucination guard — agar koi source collect 
            # na hua ho aur answer sources cite kare, to reject karo.
            if _looks_like_hallucination(answer, collected_sources):
                logger.warning(
                    "Hallucination guard triggered at iteration "
                    f"{iteration} — rejecting source-citing answer with no "
                    "collected sources."
                )
                conversation += (
                    "\\n\\n[Correction] Your previous answer cited sources "
                    "or policies, but you did NOT call semantic_search "
                    "(or it returned no results). This is a hallucination. "
                    "You MUST either: (a) call semantic_search to retrieve "
                    "real documents, or (b) reply honestly that the "
                    "information is not in the knowledge base. Do NOT "
                    "invent policies or credentials."
                )
                continue

            return {'''

if old_final not in content:
    print("ERROR: final_answer block not found")
    raise SystemExit(1)

content = content.replace(old_final, new_final, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: hallucination guard added to reasoning.py")
