from pydantic import BaseModel, Field
from typing import List, Optional
from src.models.document import Document

class RebuildIndexRequest(BaseModel):
    documents: List[Document]

class IdsRequest(BaseModel):
    ids: List[str]

class AddDocumentRequest(Document):
    pass

class BulkAddDocumentsRequest(BaseModel):
    documents: List[Document]

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class AskRequestModel(BaseModel):
    question: str
    top_k: Optional[int] = None

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
