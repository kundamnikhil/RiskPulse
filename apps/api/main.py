from fastapi import FastAPI
from .db import Base, engine
from dotenv import load_dotenv
load_dotenv()
from .routes.articles import router as articles_router
from .routes import signals
from .routes import articles, stats
from .routes.articles import router as articles_router
from .routes.stats import router as stats_router


app = FastAPI(title="RiskPulse", version="0.1.0")

# Create tables (v0 simple; later we can add migrations)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(articles_router)
app.include_router(signals.router)
app.include_router(articles.router)
app.include_router(stats.router)
