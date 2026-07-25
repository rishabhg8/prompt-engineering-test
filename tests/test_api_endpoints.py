import unittest

try:
    from fastapi.testclient import TestClient
    from app.main import app
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        if not FASTAPI_AVAILABLE:
            self.skipTest("FastAPI is not installed in local environment.")
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_list_problems(self):
        response = self.client.get("/api/problems")
        self.assertEqual(response.status_code, 200)
        problems = response.json()
        self.assertGreater(len(problems), 0, "Problems list should not be empty")

    def test_get_problem_by_id(self):
        problems_res = self.client.get("/api/problems")
        first_id = problems_res.json()[0]["id"]
        
        response = self.client.get(f"/api/problems/{first_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], first_id)

    def test_evaluate_prompt_endpoint(self):
        problems_res = self.client.get("/api/problems")
        first_id = problems_res.json()[0]["id"]

        payload = {
            "problem_id": first_id,
            "system_prompt": "You are a data extractor.",
            "user_prompt": "<instructions>Extract JSON</instructions>",
            "selected_model": "meta-llama/llama-3.2-1b-instruct",
            "temperature": 0.2,
            "top_p": 0.9
        }
        response = self.client.post("/api/evaluate", json=payload)
        self.assertEqual(response.status_code, 200)
        res_data = response.json()
        self.assertIn("overall_score", res_data)

if __name__ == "__main__":
    unittest.main()
