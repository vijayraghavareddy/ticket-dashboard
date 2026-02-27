# Ticket Dashboard — Service Documentation

## Overview

Ticket Dashboard is a lightweight **ticketing REST API** built with Python and [FastAPI](https://fastapi.tiangolo.com/). It provides a complete CRUD interface for managing support/engineering tickets, including comments, assignments, and status-workflow transitions. The service also exposes stub integration endpoints for Jira, GitHub, and TestRail that are intentionally left unimplemented so they can be built out as part of MCP (Model Context Protocol) workflows.

The project ships with a browser-based UI served as static files and auto-generated OpenAPI (Swagger) documentation.

## Architecture

```
┌────────────────────────────────────────────────────┐
│                   FastAPI App                      │
│                  (app/main.py)                     │
├──────────┬──────────────┬─────────────┬────────────┤
│ Tickets  │ Integrations │   Reports   │   System   │
│  Router  │    Router    │   Router    │  (health)  │
│ /tickets │/integrations │  /reports   │  /health   │
├──────────┴──────────────┴─────────────┴────────────┤
│              Pydantic Schemas (schemas.py)          │
├────────────────────────────────────────────────────┤
│          In-Memory Repository (repository.py)      │
├────────────────────────────────────────────────────┤
│            Domain Models (models.py)               │
└────────────────────────────────────────────────────┘
```

### Key Modules

| Module | Path | Purpose |
|--------|------|---------|
| **App entry** | `app/main.py` | Creates the FastAPI application, mounts static files, includes routers |
| **Models** | `app/models.py` | Domain dataclasses: `Ticket`, `Comment`, plus `TicketStatus` and `TicketPriority` enums |
| **Schemas** | `app/schemas.py` | Pydantic request/response models for API validation and serialization |
| **Repository** | `app/repository.py` | Thread-safe in-memory store for tickets (dict + `RLock`) |
| **Ticket routes** | `app/api/routes/tickets.py` | Full CRUD + comment, assign, and transition endpoints |
| **Integration routes** | `app/api/routes/integrations.py` | Stub endpoints for Jira sync, TestRail push, and GitHub issue creation (all return 501) |
| **Report routes** | `app/api/routes/reports.py` | Stub endpoint for SLA breach reports (returns 501) |
| **Static UI** | `app/static/` | Single-page HTML/CSS/JS dashboard for interacting with the API |

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Web framework | FastAPI | 0.116.1 |
| ASGI server | Uvicorn | 0.35.0 |
| Validation | Pydantic | 2.11.7 |
| Multipart support | python-multipart | 0.0.20 |
| Runtime | Python | 3.10+ |

## Data Model

### Ticket

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `str (UUID)` | Auto-generated | Unique identifier |
| `title` | `str` | — | Short summary (4–120 chars) |
| `description` | `str` | — | Detailed description (8–4000 chars) |
| `reporter` | `str` | — | Who raised the ticket |
| `priority` | `TicketPriority` | `medium` | `low`, `medium`, `high`, `critical` |
| `status` | `TicketStatus` | `open` | `open`, `in_progress`, `blocked`, `resolved`, `closed` |
| `assignee` | `str \| null` | `null` | Current owner |
| `tags` | `list[str]` | `[]` | Freeform labels |
| `created_at` | `datetime` | Now (UTC) | Creation timestamp |
| `updated_at` | `datetime` | Now (UTC) | Last-modified timestamp |
| `comments` | `list[Comment]` | `[]` | Threaded discussion |

### Comment

| Field | Type | Description |
|-------|------|-------------|
| `author` | `str` | Comment author name |
| `body` | `str` | Comment content (1–2000 chars) |
| `created_at` | `datetime` | When the comment was posted |

### Status Workflow

The ticket status machine enforces the following transitions:

```
open ──► in_progress ──► resolved ──► closed
  │          │  ▲            │
  │          ▼  │            ▼
  │        blocked       in_progress
  │          │
  ▼          ▼
closed     closed
```

Allowed transitions:
- **open** → `in_progress`, `blocked`, `closed`
- **in_progress** → `blocked`, `resolved`, `open`
- **blocked** → `in_progress`, `closed`
- **resolved** → `closed`, `in_progress`
- **closed** → *(terminal — no further transitions)*

## API Reference

### System

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check — returns `{"status": "ok"}` |

### Tickets

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/tickets` | Create a new ticket |
| `GET` | `/tickets` | List all tickets (optional `?status=` filter) |
| `GET` | `/tickets/{ticket_id}` | Get a ticket by ID |
| `PATCH` | `/tickets/{ticket_id}` | Partially update ticket fields |
| `POST` | `/tickets/{ticket_id}/comments` | Add a comment to a ticket |
| `POST` | `/tickets/{ticket_id}/assign` | Assign a ticket to a user |
| `POST` | `/tickets/{ticket_id}/transition` | Transition ticket status |

### Integrations (Stub — 501 Not Implemented)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/integrations/jira/sync/{ticket_id}` | Sync ticket to Jira |
| `POST` | `/integrations/testrail/push/{ticket_id}` | Push ticket to TestRail |
| `POST` | `/integrations/github/create-issue/{ticket_id}` | Create GitHub issue from ticket |

### Reports (Stub — 501 Not Implemented)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/reports/sla-breaches` | List tickets that breached SLA |

## Running the Service

### Prerequisites

- Python 3.10+
- `pip` and `venv`

### Quick Start

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Convenience Scripts

| Script | Platform | Usage |
|--------|----------|-------|
| `scripts/start.sh` | Linux / WSL | `bash scripts/start.sh [port]` |
| `scripts/start.ps1` | PowerShell | `.\scripts\start.ps1 [-Port 9000]` |
| `scripts/stop.sh` | Linux / WSL | `bash scripts/stop.sh` |
| `scripts/stop.ps1` | PowerShell | `.\scripts\stop.ps1` |

Both start scripts auto-detect port conflicts and fall back to a nearby free port.

### Interactive Documentation

Once running, browse to:
- **Dashboard UI**: http://127.0.0.1:8000/
- **Swagger (OpenAPI)**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Storage

All data is kept **in-memory** using a thread-safe Python dictionary. Data is lost when the server restarts. A persistent database backend is planned (see Jira story [TD-10](https://circuitmind.atlassian.net/browse/TD-10)).

## Planned Work

The following implementation stories are tracked in Jira (project `TD`, assigned to Circuit Mind):

| Jira Key | Summary |
|----------|---------|
| [TD-12](https://circuitmind.atlassian.net/browse/TD-12) | Implement Jira Sync Integration Endpoint |
| [TD-8](https://circuitmind.atlassian.net/browse/TD-8) | Implement TestRail Push Integration Endpoint |
| [TD-7](https://circuitmind.atlassian.net/browse/TD-7) | Implement GitHub Issue Sync Integration Endpoint |
| [TD-9](https://circuitmind.atlassian.net/browse/TD-9) | Implement SLA Breaches Report Endpoint |
| [TD-10](https://circuitmind.atlassian.net/browse/TD-10) | Add Persistent Database Storage |
| [TD-11](https://circuitmind.atlassian.net/browse/TD-11) | Add Authentication and Authorization |

## Documentation Links

- Swagger/OpenAPI guide: [SWAGGER.md](SWAGGER.md)
- Sequence diagram: [SEQUENCE_DIAGRAM.md](SEQUENCE_DIAGRAM.md)

## Design Decisions

- **In-memory storage by choice** — keeps setup friction near zero; ideal for demos and local development.
- **Intentional 501 stubs** — integration and report endpoints exist in the routing layer but return `501 Not Implemented`. This makes them visible in Swagger docs and lets teams use MCP tooling to plan, implement, and test the features end-to-end.
- **Status transition guard** — the `ALLOWED_TRANSITIONS` dict prevents invalid workflow jumps (e.g., you cannot reopen a `closed` ticket).
- **No database ORM yet** — the `TicketRepository` interface is designed so a database-backed implementation can be swapped in without changing the route layer.
- **Static UI co-hosted** — the single-page dashboard is mounted at `/ui` and also served at `/` for convenience, keeping deployment to a single process.
