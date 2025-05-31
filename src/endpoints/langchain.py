from fastapi import APIRouter, HTTPException
from src.langchain.rag_chain import run_rag_chain
from src.models.request_models import AskRequest  # ← importuj model

router = APIRouter()

@router.post("/ask/")
async def ask_question(request: AskRequest):  # ← koristi model
    if not request.question:
        raise HTTPException(status_code=400, detail="Question is required.")

    try:
        answer = run_rag_chain(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
