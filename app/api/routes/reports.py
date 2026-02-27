from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get(
    "/sla-breaches",
    summary="List SLA breaches (planned)",
    description="Placeholder endpoint for SLA breach reporting. Returns 501 by design.",
    responses={501: {"description": "Not implemented"}},
)
def get_sla_breaches() -> dict:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "feature": "sla_breaches_report",
            "message": "Planned feature intentionally left for MCP workflow.",
            "suggested_next_step": "Use GitHub MCP to create implementation task and add acceptance criteria.",
        },
    )
