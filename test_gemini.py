import os
from dotenv import load_dotenv
from google import genai

# English: Load .env and send a tiny prompt to verify Gemini works with the correct model.
# Roman Urdu: .env load karo aur chhota prompt bhejo taake confirm ho ke Gemini sahi model ke saath chal rahi hai.

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print('FAIL: GEMINI_API_KEY not found in .env')
    raise SystemExit(1)

print('Key loaded. First 12 chars:', api_key[:12] + '...')
print('Trying Gemini models (newest first)...')

client = genai.Client(api_key=api_key)

# English: Try newest stable flash models in order.
# Roman Urdu: Sab se naye stable flash models try karo order mein.
models_to_try = [
    'gemini-3.8-flash',
    'gemini-3.5-flash',
    'gemini-flash-latest',
]

success = False
for model_name in models_to_try:
    try:
        response = client.models.generate_content(
            model=model_name,
            contents='Reply with exactly: UniNexus OK'
        )
        print('SUCCESS using', model_name)
        print('Gemini reply:', response.text.strip())
        success = True
        break
    except Exception as e:
        msg = str(e)
        print('  ' + model_name + ' failed:', msg[:200])

if not success:
    print('ALL MODELS FAILED. Check key / quota / internet.')
