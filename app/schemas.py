from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models import TicketPriority, TicketStatus


class CommentCreate(BaseModel):
    author: str = Field(min_length=2, max_length=60)
    body: str = Field(min_length=1, max_length=2_000)


class CommentRead(CommentCreate):
    created_at: datetime


class TicketCreate(BaseModel):
    title: str = Field(min_length=4, max_length=120)
    description: str = Field(min_length=8, max_length=4_000)
    reporter: str = Field(min_length=2, max_length=60)
    priority: TicketPriority = TicketPriority.medium
    assignee: Optional[str] = Field(default=None, max_length=60)
    tags: list[str] = Field(default_factory=list)


class TicketUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=4, max_length=120)
    description: Optional[str] = Field(default=None, min_length=8, max_length=4_000)
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    assignee: Optional[str] = Field(default=None, max_length=60)
    tags: Optional[list[str]] = None


class AssignTicketRequest(BaseModel):
    assignee: str = Field(min_length=2, max_length=60)


class TransitionStatusRequest(BaseModel):
    target_status: TicketStatus


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
