from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..db import get_db
from ..models import Article
from ..schemas import DailyCountOut, SourceCountOut

from fastapi import APIRouter
router = APIRouter(prefix="/stats", tags=["stats"])



@router.get("/daily", response_model=list[DailyCountOut])
def stats_daily(
    days: int = Query(14, ge=1, le=365),
    source: str | None = None,
    db: Session = Depends(get_db),
):
    since = datetime.now(timezone.utc) - timedelta(days=days)

    q = (
        db.query(
            func.date(Article.created_at).label("day"),
            func.count(Article.id).label("count"),
        )
        .filter(Article.created_at >= since)
    )

    if source:
        q = q.filter(Article.source == source)

    rows = q.group_by("day").order_by("day").all()

    return [DailyCountOut(day=r.day, count=r.count) for r in rows]


@router.get("/sources", response_model=list[SourceCountOut])
def stats_sources(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    since = datetime.now(timezone.utc) - timedelta(days=days)

    rows = (
        db.query(
            Article.source.label("source"),
            func.count(Article.id).label("count"),
        )
        .filter(Article.created_at >= since)
        .group_by(Article.source)
        .order_by(func.count(Article.id).desc())
        .all()
    )

    return [SourceCountOut(source=r.source, count=r.count) for r in rows]
