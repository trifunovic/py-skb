from fastapi import APIRouter
from src.models.request_models import ChatRequest
from src.langchain.rag_chain import run_rag_chain
import uuid

router = APIRouter()

@router.post("/chat/")
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    result = run_rag_chain(session_id=session_id, user_input=req.message)

    return {
        "answer": result["answer"],
        "session_id": session_id,
        "sources": result.get("source_documents", [])
    }
