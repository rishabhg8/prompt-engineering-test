import unittest
import asyncio
from app.services.openrouter_client import OpenRouterClient

class TestOpenRouterClient(unittest.TestCase):

    def test_mock_small_model_response_high_score(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        output, latency = loop.run_until_complete(
            OpenRouterClient.generate_response(
                system_prompt="Extract JSON strictly.",
                user_prompt="<instructions>Extract data</instructions>",
                model="meta-llama/llama-3.2-1b-instruct",
                prompt_score=90
            )
        )
        
        self.assertTrue(len(output) > 0, "Output should not be empty")
        self.assertGreater(latency, 0.0, "Latency should be positive")
        self.assertTrue("status" in output or "success" in output or len(output) > 10)

    def test_mock_small_model_response_low_score(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        output, latency = loop.run_until_complete(
            OpenRouterClient.generate_response(
                system_prompt="",
                user_prompt="Give me data",
                model="qwen/qwen-2.5-1.5b-instruct",
                prompt_score=30
            )
        )
        
        self.assertTrue(len(output) > 0)
        self.assertGreater(latency, 0.0)

if __name__ == "__main__":
    unittest.main()
