# Runbook

## Start/Stop
- Start DB: docker compose up -d
- Stop DB: docker compose down
- Logs: docker compose logs -f

## Health checks
- API: GET /health
- Swagger: /docs

## Common issues
- Port 5432 in use: change compose port mapping to 5433:5432 and update DATABASE_URL
