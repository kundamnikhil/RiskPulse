from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Article
from ..schemas import ArticleCreate, ArticleOut

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("", response_model=ArticleOut)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    url_str = str(payload.url) if payload.url else None

    if url_str:
        existing = db.query(Article).filter(Article.url == url_str).first()
        if existing:
            raise HTTPException(status_code=409, detail="Article with this URL already exists")

    article = Article(
        title=payload.title,
        content=payload.content,
        url=url_str,
        source=payload.source,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.get("", response_model=list[ArticleOut])
def list_articles(limit: int = 20, db: Session = Depends(get_db)):
    return (
        db.query(Article)
        .order_by(Article.created_at.desc())
        .limit(limit)
        .all()
    )
