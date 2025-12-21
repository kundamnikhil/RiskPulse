# RiskPulse

RiskPulse extracts structured risk/event signals from unstructured text (news, filings) and surfaces trends via an interactive dashboard.

## Today (MVP v0)
- FastAPI service
- Postgres via Docker
- Articles ingestion + listing

## Run locally
### Start DB
docker compose up -d

### Run API
uvicorn apps.api.main:app --reload --port 8000

Open:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health
