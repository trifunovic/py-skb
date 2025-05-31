from fastapi import APIRouter, HTTPException
from src.models.request_models import AskRequestModel
from src.models.response_models import AskResponseModel
from src.langchain.rag_chain import run_rag_chain
from src.config import config  # koristi već postojeći instancirani config

router = APIRouter()

@router.post("/ask/", response_model=AskResponseModel)
async def ask_question(payload: AskRequestModel):
    if not payload.question:
        raise HTTPException(status_code=400, detail="Question is required.")

    try:
        top_k = payload.top_k or config.search_top_k
        result = run_rag_chain(payload.question, top_k=top_k)

        print("🧠 Ask response preview:")
        print(f"Query: {result['query']}")
        print(f"Answer: {result['result']['result']}")
        print(f"Retrieved docs: {len(result['retrieved_docs'])}", flush=True)

        return AskResponseModel(
            query=result["query"],
            answer=result["result"]["result"],
            retrieved_docs=result["retrieved_docs"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
