import os

# English: Read key from a prompt that will appear — paste when asked.
# Roman Urdu: Prompt se key lo — jab puche tab paste karo.
print("Paste your Groq key below, then press Enter:")
print("(It will NOT be echoed, that is normal.)")
key = input("> ").strip()

if not key:
    print("FAIL: No key entered.")
    raise SystemExit(1)

if not key.startswith("gsk_"):
    print(f"WARNING: Key starts with '{key[:4]}', not 'gsk_'. Check if you copied the whole thing.")

def upsert(path, k, v):
    lines, found = [], False
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                if line.startswith(f"{k}="):
                    lines.append(f"{k}={v}")
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"{k}={v}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

upsert(".env", "GROQ_API_KEY", key)
upsert(".env", "GROQ_MODEL", "llama-3.3-70b-versatile")
upsert(".env", "LLM_PROVIDER", "groq")

print()
print("OK: GROQ_API_KEY saved (length:", len(key), "chars)")
print("OK: GROQ_MODEL=llama-3.3-70b-versatile")
print("OK: LLM_PROVIDER=groq")
