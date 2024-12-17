from fastapi import APIRouter
import openai
from config import Config

router = APIRouter()
config = Config()

@router.get("/test-openai")
async def test_openai():
    """
    Test endpoint to verify OpenAI API integration with chat models.
    """
    try:
        # Use the ChatCompletion endpoint with an improved prompt
        response = openai.ChatCompletion.create(
            model=config.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Your task is to confirm that you are operational "
                        "and capable of responding to queries. If you are functional, reply with a simple confirmation."
                    ),
                },
                {
                    "role": "user",
                    "content": "Can you confirm that the OpenAI API integration is working?",
                },
            ],
            max_tokens=50
        )
        return {"status": "success", "response": response.choices[0].message["content"]}
    except Exception as e:
        return {"status": "error", "details": str(e)}
