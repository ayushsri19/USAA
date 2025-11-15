import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Listing models...\n")
models = genai.list_models()

for m in models:
    print(m.name)
