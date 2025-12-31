from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl

class ArticleCreate(BaseModel):
    title: str
    content: str
    url: Optional[HttpUrl] = None
    source: Optional[str] = None

class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    url: Optional[str] = None
    source: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel

class SignalOut(BaseModel):
    type: str
    confidence: float
    keywords: list[str]

