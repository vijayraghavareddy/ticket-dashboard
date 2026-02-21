from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes.integrations import router as integrations_router
from app.api.routes.reports import router as reports_router
from app.api.routes.tickets import router as tickets_router

app = FastAPI(
    title="Ticketing API (MCP Demo)",
    version="0.1.0",
    description=(
        "A lightweight ticketing REST API with intentionally unimplemented features "
        "to demonstrate GitHub MCP, Jira MCP, and TestRail MCP workflows."
    ),
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/ui", StaticFiles(directory=STATIC_DIR), name="ui")


@app.get("/health", tags=["System"])
def health() -> dict:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.include_router(tickets_router)
app.include_router(integrations_router)
app.include_router(reports_router)
