from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/sla-breaches")
def get_sla_breaches() -> dict:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "feature": "sla_breaches_report",
            "message": "Planned feature intentionally left for MCP workflow.",
            "suggested_next_step": "Use GitHub MCP to create implementation task and add acceptance criteria.",
        },
    )
