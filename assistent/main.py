import os
import google.generativeai as genai
from ze import config

genai.configure(api_key=config("API_KEY"))

# Exibi os modelos disponíveis
# for model in genai.list_models():
#     if "generateContent" in model.supported_generation_methods:
#         print(model.name)

model = genai.GenerativeModel("gemini-2.0-flash")

prompt = input()

response = model.generate_content(prompt)
print(response.text)
