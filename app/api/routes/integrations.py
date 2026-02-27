from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/integrations", tags=["Integrations"])


@router.post(
    "/jira/sync/{ticket_id}",
    summary="Sync ticket to Jira (planned)",
    description="Placeholder endpoint for future Jira synchronization. Returns 501 by design.",
    responses={501: {"description": "Not implemented"}},
)
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


@router.post(
    "/testrail/push/{ticket_id}",
    summary="Push ticket to TestRail (planned)",
    description="Placeholder endpoint for future TestRail synchronization. Returns 501 by design.",
    responses={501: {"description": "Not implemented"}},
)
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


@router.post(
    "/github/create-issue/{ticket_id}",
    summary="Create GitHub issue from ticket (planned)",
    description="Placeholder endpoint for future GitHub issue creation. Returns 501 by design.",
    responses={501: {"description": "Not implemented"}},
)
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
