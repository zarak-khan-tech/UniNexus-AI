import os

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

upsert(".env", "GROQ_MODEL", "openai/gpt-oss-120b")
print("OK: GROQ_MODEL=openai/gpt-oss-120b")
