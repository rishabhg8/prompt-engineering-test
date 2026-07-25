import unittest
from app.services.prompt_checker import PromptChecker

class TestPromptChecker(unittest.TestCase):

    def test_low_quality_prompt(self):
        system_prompt = ""
        user_prompt = "Give me the JSON data for John Doe."
        score, checks, category_scores, suggestions = PromptChecker.evaluate(system_prompt, user_prompt)
        
        self.assertLess(score, 60, "Low quality prompt should score under 60%")
        self.assertGreater(len(suggestions), 0, "Suggestions should be provided for low quality prompt")
        
    def test_golden_prompt_high_score(self):
        system_prompt = (
            "You are a precise data extraction expert. Respond strictly in valid raw JSON without preamble.\n"
            "### EXAMPLES\n"
            "Input: John Doe, 30 -> Output: {\"name\": \"John Doe\", \"age\": 30}"
        )
        user_prompt = (
            "<instructions>\n"
            "Extract name and age. Think step-by-step inside <thinking> tags.\n"
            "</instructions>\n"
            "<context>\n"
            "Input: Sarah Connor, age 34\n"
            "</context>"
        )
        score, checks, category_scores, suggestions = PromptChecker.evaluate(system_prompt, user_prompt)
        
        self.assertGreaterEqual(score, 80, "Golden prompt should score 80% or higher")
        passed_criteria = [c for c in checks if c.passed]
        self.assertGreaterEqual(len(passed_criteria), 6, "Most criteria should pass for golden prompt")

    def test_standards_coverage(self):
        system_prompt = "Act as an expert assistant."
        user_prompt = "Think step-by-step."
        score, checks, category_scores, suggestions = PromptChecker.evaluate(system_prompt, user_prompt)
        
        standards = set(c.standard_name for c in checks)
        self.assertIn("Google Standards", standards)
        self.assertIn("Anthropic Standards", standards)
        self.assertIn("OpenAI Standards", standards)

if __name__ == "__main__":
    unittest.main()
