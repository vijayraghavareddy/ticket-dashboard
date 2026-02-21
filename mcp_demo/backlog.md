# MCP Demo Backlog

Use these as example work items to create/manage with MCP.

## Jira MCP candidates

### JIRA-1: Implement Jira sync endpoint
- Endpoint: `POST /integrations/jira/sync/{ticket_id}`
- Acceptance criteria:
  - Retrieves ticket by ID
  - Creates/updates Jira issue with mapped fields
  - Saves external reference (`jira_issue_key`) back to ticket
  - Handles transient errors with retries

### JIRA-2: SLA breach report
- Endpoint: `GET /reports/sla-breaches`
- Acceptance criteria:
  - Calculates breached tickets using priority-based SLA matrix
  - Returns grouped output by assignee and priority
  - Includes date-range filtering

## GitHub MCP candidates

### GH-1: Create GitHub issue from ticket
- Endpoint: `POST /integrations/github/create-issue/{ticket_id}`
- Acceptance criteria:
  - Opens GitHub issue with title/body from ticket fields
  - Adds labels from tags
  - Stores `github_issue_url` in ticket metadata

### GH-2: Add persistent storage
- Replace in-memory repository with SQLite/PostgreSQL.

## TestRail MCP candidates

### TR-1: Push ticket test case to TestRail
- Endpoint: `POST /integrations/testrail/push/{ticket_id}`
- Acceptance criteria:
  - Creates/updates test case in TestRail
  - Links case to ticket ID
  - Returns external case ID in response

### TR-2: Add endpoint for test run status
- New endpoint proposal: `GET /integrations/testrail/run-status/{ticket_id}`
