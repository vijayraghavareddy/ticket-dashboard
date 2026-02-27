from fastapi import APIRouter, HTTPException, status

from app.models import TicketStatus
from app.repository import TicketNotFoundError
from app.schemas import TestRailRunStatusRead
from app.state import repo

router = APIRouter(prefix="/integrations", tags=["Integrations"])


RUN_STATUS_BY_TICKET_STATUS: dict[TicketStatus, str] = {
    TicketStatus.open: "not_ready",
    TicketStatus.in_progress: "queued",
    TicketStatus.blocked: "blocked",
    TicketStatus.resolved: "completed",
    TicketStatus.closed: "completed",
}


def _has_testrail_link(ticket_tags: list[str]) -> bool:
    return any(tag.lower() == "testrail" for tag in ticket_tags)


@router.get("/testrail/run-status/{ticket_id}", response_model=TestRailRunStatusRead)
def get_testrail_run_status(ticket_id: str) -> TestRailRunStatusRead:
    try:
        ticket = repo.get_ticket(ticket_id)
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    linked = _has_testrail_link(ticket.tags)
    run_status = RUN_STATUS_BY_TICKET_STATUS[ticket.status] if linked else "not_linked"
    run_id = f"TRUN-{ticket.id[:8]}" if linked else None
    next_action = (
        "Add 'testrail' tag to ticket and push to TestRail integration"
        if not linked
        else "No action required"
    )

    return TestRailRunStatusRead(
        ticket_id=ticket.id,
        ticket_status=ticket.status,
        testrail_linked=linked,
        run_status=run_status,
        run_id=run_id,
        next_action=next_action,
    )


@router.post("/jira/sync/{ticket_id}")
def sync_ticket_to_jira(ticket_id: str) -> dict:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "feature": "jira_sync",
            "ticket_id": ticket_id,
            "message": "Not implemented by design for Jira MCP workflow. Use MCP to create and complete this feature.",
            "suggested_next_step": "Create Jira issue + GitHub issue and track implementation using MCP tools.",
        },
    )


@router.post("/testrail/push/{ticket_id}")
def push_ticket_to_testrail(ticket_id: str) -> dict:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "feature": "testrail_push",
            "ticket_id": ticket_id,
            "message": "Not implemented by design for TestRail MCP workflow.",
            "suggested_next_step": "Create TestRail test case from ticket acceptance criteria via MCP.",
        },
    )


@router.post("/github/create-issue/{ticket_id}")
def create_github_issue_for_ticket(ticket_id: str) -> dict:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "feature": "github_issue_sync",
            "ticket_id": ticket_id,
            "message": "Not implemented by design for GitHub MCP workflow.",
            "suggested_next_step": "Use GitHub MCP issue tools to open tracking issue and link back to ticket.",
        },
    )
