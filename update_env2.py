import os

def upsert_env(path, key, value):
    lines, found = [], False
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.read().splitlines():
                if line.startswith(key + '='):
                    lines.append(f'{key}={value}')
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f'{key}={value}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

upsert_env('.env', 'GEMINI_MODEL', 'gemini-flash-lite-latest')
print('OK: GEMINI_MODEL=gemini-flash-lite-latest')
