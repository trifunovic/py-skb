import openai

def generate_embedding(content: str):
    """
    Generate embeddings using OpenAI's text-embedding-ada-002 model.
    """
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=content
    )
    return response["data"][0]["embedding"]
