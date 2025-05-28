from pydantic import BaseModel
from typing import List  # ✅ obavezno

class Document(BaseModel):
    id: str
    content: str
    metadata: dict
