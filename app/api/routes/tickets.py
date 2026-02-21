from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from app.models import Comment, Ticket, TicketStatus
from app.repository import TicketNotFoundError, TicketRepository
from app.schemas import (
    AssignTicketRequest,
    CommentCreate,
    TicketCreate,
    TicketRead,
    TicketUpdate,
    TransitionStatusRequest,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])
repo = TicketRepository()

ALLOWED_TRANSITIONS: dict[TicketStatus, set[TicketStatus]] = {
    TicketStatus.open: {TicketStatus.in_progress, TicketStatus.blocked, TicketStatus.closed},
    TicketStatus.in_progress: {TicketStatus.blocked, TicketStatus.resolved, TicketStatus.open},
    TicketStatus.blocked: {TicketStatus.in_progress, TicketStatus.closed},
    TicketStatus.resolved: {TicketStatus.closed, TicketStatus.in_progress},
    TicketStatus.closed: set(),
}


def _to_ticket_read(ticket: Ticket) -> TicketRead:
    return TicketRead(
        id=ticket.id,
        title=ticket.title,
        description=ticket.description,
        reporter=ticket.reporter,
        priority=ticket.priority,
        status=ticket.status,
        assignee=ticket.assignee,
        tags=ticket.tags,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        comments=[
            {"author": comment.author, "body": comment.body, "created_at": comment.created_at}
            for comment in ticket.comments
        ],
    )


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate) -> TicketRead:
    ticket = Ticket(**payload.model_dump())
    created = repo.create_ticket(ticket)
    return _to_ticket_read(created)


@router.get("", response_model=list[TicketRead])
def list_tickets(status_filter: str | None = Query(default=None, alias="status")) -> list[TicketRead]:
    tickets = repo.list_tickets(status=status_filter)
    return [_to_ticket_read(ticket) for ticket in tickets]


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: str) -> TicketRead:
    try:
        ticket = repo.get_ticket(ticket_id)
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return _to_ticket_read(ticket)


@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(ticket_id: str, payload: TicketUpdate) -> TicketRead:
    try:
        updated = repo.update_ticket(ticket_id, **payload.model_dump(exclude_unset=True))
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return _to_ticket_read(updated)


@router.post("/{ticket_id}/comments", response_model=TicketRead)
def add_comment(ticket_id: str, payload: CommentCreate) -> TicketRead:
    try:
        ticket = repo.add_comment(ticket_id, Comment(**payload.model_dump()))
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return _to_ticket_read(ticket)


@router.post("/{ticket_id}/assign", response_model=TicketRead)
def assign_ticket(ticket_id: str, payload: AssignTicketRequest) -> TicketRead:
    try:
        ticket = repo.update_ticket(ticket_id, assignee=payload.assignee)
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return _to_ticket_read(ticket)


@router.post("/{ticket_id}/transition", response_model=TicketRead)
def transition_ticket(ticket_id: str, payload: TransitionStatusRequest) -> TicketRead:
    try:
        current = repo.get_ticket(ticket_id)
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    if payload.target_status not in ALLOWED_TRANSITIONS[current.status]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid transition from {current.status.value} to {payload.target_status.value}",
        )

    updated = repo.update_ticket(ticket_id, status=payload.target_status)
    return _to_ticket_read(updated)
