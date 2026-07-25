import unittest
from app.services.google_guardrails import GoogleGuardrailsEvaluator

class TestGoogleGuardrails(unittest.TestCase):

    def test_empty_prompt_evaluation(self):
        analysis = GoogleGuardrailsEvaluator.analyze("", "")
        self.assertEqual(analysis.overall_score, 0)
        self.assertGreater(len(analysis.missing_steps), 0)

    def test_full_google_5step_prompt(self):
        sys_prompt = "You are an expert Google Cloud Solutions Architect."
        user_prompt = (
            "Scenario: Migrating an on-premise relational database to Google Cloud Spanner.\n"
            "Task: Create a 5-point migration checklist.\n"
            "Format: Respond strictly in a 3-column Markdown table.\n"
            "Example:\n"
            "Input: Schema -> Output: | Phase | Action | Status |\n"
            "Constraints: Do not include preamble. Think step-by-step."
        )
        analysis = GoogleGuardrailsEvaluator.analyze(sys_prompt, user_prompt)
        self.assertGreaterEqual(analysis.overall_score, 60)

if __name__ == "__main__":
    unittest.main()
