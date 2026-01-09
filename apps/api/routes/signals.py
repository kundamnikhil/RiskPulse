from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Article
from ..schemas import SignalOut
from ..services.signal_extractor import extract_signals

router = APIRouter(tags=["signals"])

@router.get("/articles/{article_id}/signals", response_model=list[SignalOut])
def get_article_signals(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    text = f"{article.title}\n\n{article.content}"
    signals = extract_signals(text)

    return [
        {"type": s.type, "confidence": s.confidence, "keywords": s.keywords}
        for s in signals
    ]
