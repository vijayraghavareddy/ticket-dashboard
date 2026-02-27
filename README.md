# Ticket Dashboard

Python REST API for a ticketing system, intentionally designed with a few **Not Implemented** features so you can demonstrate:
- GitHub MCP
- Jira MCP
- TestRail MCP

## Stack
- FastAPI
- Pydantic
- Uvicorn
- In-memory repository (no database yet)

## Quick Start

### WSL prerequisite (Ubuntu)

If `start.ps1` fails with missing `venv`/`pip`, install once in WSL:

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip
```

### 1) Create virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

### 2) Run API

```bash
uvicorn app.main:app --reload
```

### One-command start (Windows + WSL)

From PowerShell in project root:

```powershell
.\scripts\start.ps1
```

This script:
- creates `.venv` if missing
- installs dependencies (unless `-SkipInstall` is passed)
- starts API in WSL on `http://127.0.0.1:8000`
- **auto-selects the next free port** if port 8000 is already occupied
- opens the UI in your browser

Use `-Port` to specify a custom port:

```powershell
.\scripts\start.ps1 -Port 9000
```

Stop it with:

```powershell
.\scripts\stop.ps1
```

### Linux / WSL-only

Start the API:

```bash
bash scripts/start.sh          # default port 8000
bash scripts/start.sh 9000     # custom port
```

If the default port is occupied by another process, the script automatically
picks the next available port (8001–8020) and prints the URL.

Stop the API:

```bash
bash scripts/stop.sh
```

### Port conflicts

Both start scripts detect when the target port is already in use and
automatically fall back to a nearby free port. The actual URL is printed
to the terminal. If you need to free the default port manually:

```bash
# Find the process occupying port 8000
ss -tlnp 'sport = :8000'
# or
lsof -i :8000

# Kill it (replace <PID> with actual PID)
kill <PID>
```

### 3) Open API docs
- UI: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## UI Features
- Create tickets
- List and filter tickets by status
- Add comments, assign users, and transition status from each ticket card
- Trigger MCP placeholder integration endpoints and inspect `501` responses in the response panel

## Implemented Endpoints

### System
- `GET /health`

### Tickets
- `POST /tickets` - Create ticket
- `GET /tickets` - List tickets (`?status=` filter available)
- `GET /tickets/{ticket_id}` - Get one ticket
- `PATCH /tickets/{ticket_id}` - Update ticket fields
- `POST /tickets/{ticket_id}/comments` - Add comment
- `POST /tickets/{ticket_id}/assign` - Assign ticket owner
- `POST /tickets/{ticket_id}/transition` - Move through workflow statuses

## Intentionally Not Implemented (for MCP workflows)

These endpoints return `501 Not Implemented` by design:

- `POST /integrations/jira/sync/{ticket_id}`
- `POST /integrations/testrail/push/{ticket_id}`
- `POST /integrations/github/create-issue/{ticket_id}`
- `GET /reports/sla-breaches`

See [backlog/backlog.md](backlog/backlog.md) for suggested tasks.

## Example Requests

Create a ticket:

```bash
curl -X POST http://127.0.0.1:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Checkout fails for EU cards",
    "description": "Payments fail with a 500 when using EU-issued cards in staging",
    "reporter": "qa.lead",
    "priority": "high",
    "tags": ["payments", "staging"]
  }'
```

Transition status:

```bash
curl -X POST http://127.0.0.1:8000/tickets/<ticket_id>/transition \
  -H "Content-Type: application/json" \
  -d '{"target_status": "in_progress"}'
```

Trigger a not-yet-implemented endpoint:

```bash
curl -X POST http://127.0.0.1:8000/integrations/jira/sync/<ticket_id>
```

## Suggested MCP Workflow

1. Create a ticket in this API.
2. Call `POST /integrations/jira/sync/{ticket_id}` and show `501` response.
3. Use Jira MCP to create a Jira issue from this gap.
4. Use GitHub MCP to create a GitHub issue and/or PR task tied to Jira.
5. Use TestRail MCP to create test artifacts for acceptance criteria.
6. Implement the feature and close linked tasks.

## Notes
- Persistence is currently in-memory and resets on restart.
- Auth, audit history, attachments, SLA engine, and external integrations are left out intentionally for MCP workflows.

## Additional Documentation

- Swagger/OpenAPI guide: [docs/SWAGGER.md](docs/SWAGGER.md)
- API sequence diagram: [docs/SEQUENCE_DIAGRAM.md](docs/SEQUENCE_DIAGRAM.md)

To export a tracked OpenAPI snapshot file:

```bash
python scripts/export_openapi.py
```
