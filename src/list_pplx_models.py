import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    print("❌ No PERPLEXITY_API_KEY found in .env")
    exit()

url = "https://api.perplexity.ai/models"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

print("\n=====================================")
print("      FETCHING AVAILABLE MODELS")
print("=====================================\n")

try:
    resp = requests.get(url, headers=headers)
    print("HTTP Status:", resp.status_code)

    try:
        data = resp.json()
    except:
        print("❌ Failed to decode JSON")
        print(resp.text)
        exit()

    print("\n=== RAW RESPONSE ===")
    print(json.dumps(data, indent=2))

except Exception as e:
    print("❌ Network error:", e)
