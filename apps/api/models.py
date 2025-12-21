from sqlalchemy import Column, DateTime, Integer, String, Text, func
from .db import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(1024), unique=True, index=True, nullable=True)
    source = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
