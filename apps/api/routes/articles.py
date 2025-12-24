from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

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
def list_articles(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    source: Optional[str] = Query(None),
    q: Optional[str] = Query(None, description="Search in title/content"),
    since: Optional[datetime] = Query(None, description="created_at >= since (ISO-8601)"),
):
    query = db.query(Article)

    if source:
        query = query.filter(Article.source == source)

    if since:
        query = query.filter(Article.created_at >= since)

    if q:
        like = f"%{q}%"
        query = query.filter(or_(Article.title.ilike(like), Article.content.ilike(like)))

    return (
        query.order_by(Article.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

