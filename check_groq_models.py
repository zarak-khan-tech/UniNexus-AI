import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=key)

print("Available Groq models:")
print("=" * 60)
models = client.models.list()
for m in models.data:
    print(f"  {m.id}")
