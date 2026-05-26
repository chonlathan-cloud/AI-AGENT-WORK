import vertexai
from vertexai.generative_models import GenerativeModel
import os
import sys

PROJECT_ID = "ai-manee-son"
LOCATION = "us-central1"

print(f"Initializing Vertex AI for project {PROJECT_ID} in {LOCATION}...")
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print("Vertex AI initialized.")
except Exception as e:
    print(f"Error initializing Vertex AI: {e}")
    sys.exit(1)

model_name = "gemini-3.1-pro-preview"
print(f"Loading model: {model_name}...")
try:
    model = GenerativeModel(model_name)
    response = model.generate_content("Hello")
    print(f"Response: {response.text}")
    print("Model test successful.")
except Exception as e:
    print(f"Error with model generation: {e}")
