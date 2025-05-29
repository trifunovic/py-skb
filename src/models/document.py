from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Document(BaseModel):
    id: str
    content: str
    metadata: Optional[Dict[str, Any]] = {}
