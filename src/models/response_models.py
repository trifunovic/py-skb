from pydantic import BaseModel
from typing import Optional, List
from src.models.document import Document

class BaseResponse(BaseModel):
    hasErrors: bool = False
    error: Optional[str] = None

class GetAllDocumentsResponse(BaseResponse):
    documents: List[Document]

class RebuildIndexResponse(BaseResponse):
    message: str

class AddDocumentResponse(BaseResponse):
    id: str
    status: str

class AddDocumentsResponse(BaseResponse):
    inserted: List[dict]  # može biti lista statusa po dokumentu

class SearchResult(BaseModel):
    document_id: str
    relevance_score: float
    short_answer: str
    details: dict

class SearchResponse(BaseResponse):
    query: str
    results: List[SearchResult]

class RetrievedDocModel(BaseModel):
    id: str
    content: str
    metadata: dict

class AskResponseModel(BaseModel):
    query: str
    answer: str
    retrieved_docs: Optional[List[RetrievedDocModel]]
