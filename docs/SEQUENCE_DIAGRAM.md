# Ticket API Sequence Diagram

This diagram describes a typical ticket lifecycle through the current API.

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Ticket Dashboard UI
    participant API as FastAPI Routes
    participant Repo as TicketRepository (in-memory)

    User->>UI: Fill ticket form and submit
    UI->>API: POST /tickets
    API->>Repo: create_ticket(ticket)
    Repo-->>API: created ticket
    API-->>UI: 201 TicketRead

    User->>UI: Assign owner
    UI->>API: POST /tickets/{id}/assign
    API->>Repo: update_ticket(id, assignee)
    Repo-->>API: updated ticket
    API-->>UI: 200 TicketRead

    User->>UI: Move status to in_progress
    UI->>API: POST /tickets/{id}/transition
    API->>Repo: get_ticket(id)
    Repo-->>API: current ticket
    API->>API: validate transition against ALLOWED_TRANSITIONS
    API->>Repo: update_ticket(id, status)
    Repo-->>API: updated ticket
    API-->>UI: 200 TicketRead

    User->>UI: Add comment
    UI->>API: POST /tickets/{id}/comments
    API->>Repo: add_comment(id, comment)
    Repo-->>API: updated ticket
    API-->>UI: 200 TicketRead
```

## Alternate path: invalid transition

If a transition is not allowed by the workflow matrix, the API responds with:

- `400 Bad Request`
- Message: `Invalid transition from <current> to <target>`
