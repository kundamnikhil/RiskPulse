from fastapi import FastAPI
from .db import Base, engine
from dotenv import load_dotenv
load_dotenv()
from .routes.articles import router as articles_router
from .routes import signals
from .routes import articles, stats
from .routes.articles import router as articles_router
from .routes.stats import router as stats_router
from sqlalchemy import text
from .db import Base, engine


app = FastAPI(title="RiskPulse", version="0.1.0")

# Create tables (v0 simple; later we can add migrations)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def _startup_db_check():
    # Create tables (lightweight MVP bootstrap)
    Base.metadata.create_all(bind=engine)

    # Verify connectivity early with a simple query
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


app.include_router(articles_router)
app.include_router(signals.router)
app.include_router(articles.router)
app.include_router(stats.router)
