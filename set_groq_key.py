import os

key = input("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: ").strip()
if not key.startswith("gsk_"):
    print("WARNING: Key does not start with 'gsk_'. Continue anyway? (Ctrl+C to abort)")

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
print("OK: GROQ_API_KEY saved")
print("OK: GROQ_MODEL=llama-3.3-70b-versatile")
print("OK: LLM_PROVIDER=groq")
