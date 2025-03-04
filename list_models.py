import google.generativeai as genai

GOOGLE_API_KEY = "YOUR_NEW_API_KEY_HERE"
genai.configure(api_key=GOOGLE_API_KEY)

models = genai.list_models()
for model in models:
    print(model.name)
