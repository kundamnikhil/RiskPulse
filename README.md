# RiskPulse

RiskPulse extracts structured risk/event signals from unstructured text (news, filings) and surfaces trends via an interactive dashboard.

## Today (MVP v0)
- FastAPI service
- Postgres via Docker
- Articles ingestion + listing + filters (source, q, since, limit, offset)
- Health endpoint

## Run locally

### Prereqs
- Python 3.12+
- Docker Desktop

### 1) Start DB
From the repo root:
```powershell
docker compose up -d
docker ps


### Run API
```powershell
python -m uvicorn apps.api.main:app --reload --host 127.0.0.1 --port 8000
```

Open:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

### Query and paginate articles
```powershell
irm "http://127.0.0.1:8000/articles?source=manual"
irm "http://127.0.0.1:8000/articles?q=sanctions"
irm "http://127.0.0.1:8000/articles?since=2025-12-21T00:00:00Z"
irm "http://127.0.0.1:8000/articles?limit=2&offset=1"
```

### Get an article by id
```powershell
irm "http://127.0.0.1:8000/articles/1"
```

---

## Run and verify locally (fast)
Make sure your API is running:
```powershell
python -m uvicorn apps.api.main:app --reload --host 127.0.0.1 --port 8000
```


