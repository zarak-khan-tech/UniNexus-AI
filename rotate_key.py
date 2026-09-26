key = input("Paste NEW Groq key: ").strip()
if not key:
    raise SystemExit(1)
lines, found = [], False
with open(".env", "r", encoding="utf-8") as f:
    for line in f.read().splitlines():
        if line.startswith("GROQ_API_KEY="):
            lines.append("GROQ_API_KEY=" + key)
            found = True
        else:
            lines.append(line)
if not found:
    lines.append("GROQ_API_KEY=" + key)
with open(".env", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("OK: new key saved locally")
