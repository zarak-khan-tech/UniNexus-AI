import os

# English: Prompt for the key, upsert into .env, and enable Gemini as the active provider.
# Roman Urdu: Key pucho, .env mein save karo, aur Gemini ko active provider set karo.
key = input('Paste your Gemini API key (AQ....): ').strip()

if not key:
    print('FAIL: No key entered.')
    raise SystemExit(1)

# English: Read existing .env and remove any old GEMINI_API_KEY / LLM_PROVIDER lines.
# Roman Urdu: Purani .env file parho, aur agar GEMINI_API_KEY ya LLM_PROVIDER pehle se hai to hatao.
lines = []
if os.path.exists('.env'):
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f.read().splitlines():
            if line.startswith('GEMINI_API_KEY=') or line.startswith('LLM_PROVIDER='):
                continue
            lines.append(line)

# English: Append fresh values — Gemini as default provider.
# Roman Urdu: Nayi values add karo — Gemini default provider ke taur pe.
lines.append('')
lines.append('# LLM Provider')
lines.append('# Which provider to use first: "gemini" or "ollama"')
lines.append('LLM_PROVIDER=gemini')
lines.append('')
lines.append('# Google Gemini API Key')
lines.append('# WARNING: NEVER commit this file. It is excluded by .gitignore.')
lines.append('GEMINI_API_KEY=' + key)

with open('.env', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print('OK: GEMINI_API_KEY saved to .env')
print('OK: LLM_PROVIDER set to gemini')
