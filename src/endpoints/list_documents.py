from fastapi import APIRouter, HTTPException
from src.services.vector_store_service import list_all_document_ids

router = APIRouter()

@router.get("/documents")
def list_documents():
    try:
        ids = list_all_document_ids()
        return {"count": len(ids), "document_ids": ids}
    except NotImplementedError as e:
        return {"count": 0, "document_ids": [], "note": str(e)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
