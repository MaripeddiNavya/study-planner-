from google.generativeai import configure, list_models

configure(api_key="AIzaSyBDiJXHgpKJ6YxApdp8dGzBrMkf-BYQeo8")  # Replace with your actual API key

models = list_models()
for model in models:
    print(model.name)