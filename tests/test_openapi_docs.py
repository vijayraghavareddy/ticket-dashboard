import unittest

from fastapi.testclient import TestClient

from app.main import app


class OpenAPIDocumentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_openapi_includes_expected_tags(self) -> None:
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)

        schema = response.json()
        tags = {tag["name"] for tag in schema.get("tags", [])}
        self.assertTrue({"System", "Tickets", "Integrations", "Reports"}.issubset(tags))

    def test_tickets_routes_have_swagger_summaries(self) -> None:
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)

        schema = response.json()
        create_ticket_summary = schema["paths"]["/tickets"]["post"].get("summary")
        transition_summary = schema["paths"]["/tickets/{ticket_id}/transition"]["post"].get("summary")

        self.assertEqual(create_ticket_summary, "Create ticket")
        self.assertEqual(transition_summary, "Transition ticket status")


if __name__ == "__main__":
    unittest.main()
