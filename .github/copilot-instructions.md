# GitHub Copilot Instructions

## MCP Integration Context

### Jira
- **Project Key:** `TD`
- Use `TD` as the Jira project key when searching for or creating issues via MCP tools.

<!-- ### TestRail
- **Project Name:** `ticket-dashboard`
- Use `ticket-dashboard` as the TestRail project when managing test cases, runs, or suites via MCP tools.
 -->
### GitHub
- **Repository:** `ticket-dashboard`
- Use `ticket-dashboard` as the repository name when performing GitHub operations via MCP tools.

## Development Workflow Requirements

- For every new feature, always create and switch to a dedicated feature branch before making code changes.
- Use this branch naming convention for feature work: `feature/TD-<issue-number>-<short-kebab-description>`.
- Use `bugfix/TD-<issue-number>-<short-kebab-description>` for defects and `chore/TD-<issue-number>-<short-kebab-description>` for non-feature maintenance.
- Implement unit tests whenever a new feature is developed.
- Ensure unit tests cover all relevant scenarios for the feature, including expected behavior, edge cases, and failure/error paths.
- Do not consider feature work complete until the corresponding unit tests are present and passing.
- When API routes, request/response schemas, status codes, or tags change, regenerate the repository OpenAPI snapshot by running `python scripts/export_openapi.py`.
- Commit updated `openapi.json` in the same change whenever API contracts are modified.

## Delivery Completeness Checklist

- Keep changes scoped to the issue and avoid unrelated refactors unless explicitly required.
- Update or add documentation (`README.md`, `docs/SERVICE.md`, or route-level docs) whenever behavior, configuration, or API contracts change.
- Run relevant local validation before opening a PR (targeted unit tests first, then broader project checks when applicable).
- For API changes, run `python scripts/export_openapi.py` and verify `openapi.json` reflects the latest contract before opening a PR.
- Ensure error handling is tested and user-facing responses/messages remain consistent with existing API patterns.
- Open PRs with a clear summary, validation steps executed, and Jira reference (for example: `TD-123`).
- Prefer small, reviewable PRs and include follow-up items explicitly if any scope is intentionally deferred.
