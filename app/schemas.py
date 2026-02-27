from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models import TicketPriority, TicketStatus


class CommentCreate(BaseModel):
    author: str = Field(min_length=2, max_length=60)
    body: str = Field(min_length=1, max_length=2_000)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "author": "qa.lead",
                "body": "Observed intermittent timeout when retrying checkout flow.",
            }
        }
    )


class CommentRead(CommentCreate):
    created_at: datetime


class TicketCreate(BaseModel):
    title: str = Field(min_length=4, max_length=120)
    description: str = Field(min_length=8, max_length=4_000)
    reporter: str = Field(min_length=2, max_length=60)
    priority: TicketPriority = TicketPriority.medium
    assignee: Optional[str] = Field(default=None, max_length=60)
    tags: list[str] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Checkout fails for EU cards",
                "description": "Payments fail with a 500 when using EU-issued cards in staging.",
                "reporter": "qa.lead",
                "priority": "high",
                "assignee": "backend.dev",
                "tags": ["payments", "staging"],
            }
        }
    )


class TicketUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=4, max_length=120)
    description: Optional[str] = Field(default=None, min_length=8, max_length=4_000)
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    assignee: Optional[str] = Field(default=None, max_length=60)
    tags: Optional[list[str]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "priority": "critical",
                "assignee": "payments.oncall",
                "tags": ["payments", "incident"],
            }
        }
    )


class AssignTicketRequest(BaseModel):
    assignee: str = Field(min_length=2, max_length=60)

    model_config = ConfigDict(json_schema_extra={"example": {"assignee": "sre.engineer"}})


class TransitionStatusRequest(BaseModel):
    target_status: TicketStatus

    model_config = ConfigDict(json_schema_extra={"example": {"target_status": "in_progress"}})


class TicketRead(BaseModel):
    id: str
    title: str
    description: str
    reporter: str
    priority: TicketPriority
    status: TicketStatus
    assignee: Optional[str]
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    comments: list[CommentRead]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "4c312f79-4ee8-4613-9f67-5bc320bf1b74",
                "title": "Checkout fails for EU cards",
                "description": "Payments fail with a 500 when using EU-issued cards in staging.",
                "reporter": "qa.lead",
                "priority": "high",
                "status": "in_progress",
                "assignee": "backend.dev",
                "tags": ["payments", "staging"],
                "created_at": "2026-02-26T09:00:00Z",
                "updated_at": "2026-02-26T09:05:00Z",
                "comments": [
                    {
                        "author": "qa.lead",
                        "body": "Issue reproduced consistently in staging.",
                        "created_at": "2026-02-26T09:03:00Z",
                    }
                ],
            }
        }
    )
