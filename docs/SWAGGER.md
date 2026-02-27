# Swagger / OpenAPI Documentation

This service publishes an OpenAPI 3 schema and interactive Swagger UI via FastAPI.

## Endpoints

- OpenAPI JSON: `/openapi.json`
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Repository OpenAPI Snapshot

A committed OpenAPI snapshot is available at `openapi.json` in the repository root.

Regenerate it after adding or changing APIs:

```bash
python scripts/export_openapi.py
```

## What is documented

The generated schema includes:

- endpoint groups (`System`, `Tickets`, `Integrations`, `Reports`)
- request/response models from `app/schemas.py`
- status codes and error responses for key operations
- summaries/descriptions for each route

## Quick usage

1. Start the API:

   ```bash
   uvicorn app.main:app --reload
   ```

2. Open Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. Expand an endpoint and click **Try it out**.
4. Use the generated examples/schemas to build requests.

## Notes

- Integration and report endpoints intentionally return `501 Not Implemented` by design.
- Swagger stays up to date with route decorators and Pydantic schemas.
