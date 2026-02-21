from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Optional

from app.models import Comment, Ticket


class TicketNotFoundError(ValueError):
    pass


class TicketRepository:
    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {}
        self._lock = RLock()

    def create_ticket(self, ticket: Ticket) -> Ticket:
        with self._lock:
            self._tickets[ticket.id] = ticket
            return ticket

    def list_tickets(self, status: Optional[str] = None) -> list[Ticket]:
        with self._lock:
            values = list(self._tickets.values())
            if status:
                return [ticket for ticket in values if ticket.status.value == status]
            return values

    def get_ticket(self, ticket_id: str) -> Ticket:
        with self._lock:
            ticket = self._tickets.get(ticket_id)
            if not ticket:
                raise TicketNotFoundError(f"Ticket {ticket_id} not found")
            return ticket

    def update_ticket(self, ticket_id: str, **changes: object) -> Ticket:
        with self._lock:
            ticket = self.get_ticket(ticket_id)
            for field_name, value in changes.items():
                if value is not None:
                    setattr(ticket, field_name, value)
            ticket.updated_at = datetime.now(timezone.utc)
            return ticket

    def add_comment(self, ticket_id: str, comment: Comment) -> Ticket:
        with self._lock:
            ticket = self.get_ticket(ticket_id)
            ticket.comments.append(comment)
            ticket.updated_at = datetime.now(timezone.utc)
            return ticket
