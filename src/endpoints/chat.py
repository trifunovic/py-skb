from fastapi import APIRouter, HTTPException
from src.models.request_models import ChatRequest
from src.models.response_models import ChatResponseModel
from src.langchain.rag_chain import run_rag_chain

router = APIRouter()

@router.post("/chat/", response_model=ChatResponseModel)
async def chat(req: ChatRequest):
    try:
        session_id = req.session_id
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id is required.")

        result = run_rag_chain(session_id=session_id, user_input=req.message)

        return ChatResponseModel(
            answer=result["answer"],
            session_id=session_id,
            sources=result["source_documents"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
