import unittest
from app.services.google_guardrails import GoogleGuardrailsEvaluator

class TestGoogleGuardrails(unittest.TestCase):

    def test_low_quality_prompt(self):
        analysis = GoogleGuardrailsEvaluator.analyze("", "Write a summary.")
        self.assertLess(analysis.overall_score, 50)
        self.assertGreater(len(analysis.actionable_suggestions), 0)

    def test_full_google_framework_prompt(self):
        sys_prompt = "You are a Google Cloud Certified Data Architect."
        user_prompt = (
            "Scenario: Migrating an on-premise database to Spanner.\n"
            "Task: Write a migration checklist.\n"
            "Format: 3-column Markdown table.\n"
            "Example:\n"
            "Input: Schema -> Output: | Phase | Action | Status |\n"
            "Constraints: Think step-by-step before output."
        )
        analysis = GoogleGuardrailsEvaluator.analyze(sys_prompt, user_prompt)
        self.assertGreaterEqual(analysis.overall_score, 60)

if __name__ == "__main__":
    unittest.main()
