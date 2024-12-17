import os
from some_library import validate_openai-api-key

# Set API Key
os.environ["openai-api-key"] = "your_openai-api-key"
embed_model.api_key = os.getenv("openai-api-key")

# Validate API Key
try:
    validate_openai_api_key(embed_model.api_key)  # type: ignore
    print("API Key is valid!")
except Exception as e:
    print(f"API Key validation failed: {e}")

    import os
os.environ["openai-api-key"] = "your_openai-api-key"


import os

key = os.getenv("KNOWLEDGE_API_KEY")
if key:
    print(f"API Key found: {key}")
else:
    print("API Key not found.")