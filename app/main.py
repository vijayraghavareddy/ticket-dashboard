from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes.integrations import router as integrations_router
from app.api.routes.reports import router as reports_router
from app.api.routes.tickets import router as tickets_router

app = FastAPI(
    title="Ticket Dashboard",
    version="0.1.0",
    description=(
        "A lightweight ticketing REST API with intentionally unimplemented features "
        "to demonstrate GitHub MCP, Jira MCP, and TestRail MCP workflows."
    ),
    contact={"name": "Ticket Dashboard Team"},
    openapi_tags=[
        {"name": "System", "description": "Service health and runtime availability endpoints."},
        {"name": "Tickets", "description": "Ticket lifecycle operations including CRUD, comments, assignment, and transitions."},
        {"name": "Integrations", "description": "Planned integration endpoints that intentionally return 501 for MCP workflows."},
        {"name": "Reports", "description": "Planned reporting endpoints exposed for future implementation."},
    ],
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/ui", StaticFiles(directory=STATIC_DIR), name="ui")


@app.get(
    "/health",
    tags=["System"],
    summary="Health check",
    description="Returns service availability for uptime checks.",
)
def health() -> dict:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.include_router(tickets_router)
app.include_router(integrations_router)
app.include_router(reports_router)
