import google.generativeai as genai

# Paste your API key directly here to test
genai.configure(api_key="AIzaSyB-cEawYprfMTPOTKfzuhP8sx66-HLZ5vA")

models = genai.list_models()

for model in models:
    print(model.name, model.supported_generation_methods)
