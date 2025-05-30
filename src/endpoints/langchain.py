from fastapi import APIRouter, HTTPException
from src.langchain.rag_chain import run_qa

router = APIRouter()

@router.post("/ask/")
async def ask_question(payload: dict):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")

    try:
        answer = run_qa(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
