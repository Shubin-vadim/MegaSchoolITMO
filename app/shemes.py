from pydantic import BaseModel
from typing import Optional, List

class Query(BaseModel):
    query: str
    id: int

class Response(BaseModel):
    id: int
    answer: Optional[int]
    reasoning: str
    sources: List[str]