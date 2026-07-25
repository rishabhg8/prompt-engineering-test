import time
import json
import logging
from typing import Tuple, Dict, Any, Optional
try:
    import httpx
except ImportError:
    httpx = None

from app.config import settings
from app.services.problem_bank import problem_bank

logger = logging.getLogger("openrouter_client")


class OpenRouterClient:
    """
    Handles API calls to OpenRouter for small models (1B-3B parameters).
    Includes automatic mock mode fallback when API keys are unconfigured or request fails.
    """

    @classmethod
    async def generate_response(
        cls,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float = 0.2,
        top_p: float = 0.9,
        api_key: str = "",
        prompt_score: float = 50.0
    ) -> Tuple[str, float]:
        instance = cls()
        res, latency = await instance.generate_completion(
            system_prompt, user_prompt, model, temperature, top_p, None, prompt_score
        )
        return res, latency

    async def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        model_id: str,
        temperature: float = 0.7,
        top_p: float = 0.95,
        problem_id: Optional[str] = None,
        prompt_score: float = 80.0,
    ) -> Tuple[str, float]:
        start_time = time.perf_counter()

        # Check if Mock Mode is active, API key is absent, or httpx is not installed
        if getattr(settings, "MOCK_MODE", True) or httpx is None:
            logger.info("OpenRouter API key not set or mock mode enabled. Using mock response.")
            output = self._generate_mock_response(problem_id, prompt_score, system_prompt, user_prompt)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return output, round(elapsed_ms, 2)

        # Attempt live API call to OpenRouter
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                payload = {
                    "model": model_id,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": temperature,
                    "top_p": top_p,
                }
                response = await client.post(
                    f"{settings.OPENROUTER_API_URL}/chat/completions",
                    headers=settings.OPENROUTER_HEADERS,
                    json=payload,
                )
                if response.status_code == 200:
                    data = response.json()
                    output_text = data["choices"][0]["message"]["content"]
                    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                    return output_text, round(elapsed_ms, 2)
                else:
                    logger.warning(
                        f"OpenRouter API error {response.status_code}: {response.text}. Falling back to mock."
                    )
                    output = self._generate_mock_response(problem_id, prompt_score, system_prompt, user_prompt)
                    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                    return output, round(elapsed_ms, 2)
        except Exception as e:
            logger.error(f"Exception during OpenRouter API call: {str(e)}. Falling back to mock.")
            output = self._generate_mock_response(problem_id, prompt_score, system_prompt, user_prompt)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return output, round(elapsed_ms, 2)

    def _generate_mock_response(
        self,
        problem_id: Optional[str],
        prompt_score: float,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Generates realistic small-model outputs.
        If prompt_score is high (>= 60), returns clean successful output.
        If prompt_score is low (< 60), returns authentic small-model flawed output.
        """
        problem = problem_bank.get_by_id(problem_id) if problem_id else None
        golden_ref = problem.golden_prompt_reference if problem else None

        # Check for specific prompt flaws
        combined = f"{system_prompt}\n{user_prompt}".lower()
        has_no_chatter_rule = "no conversational" in combined or "only return" in combined or "do not write" in combined
        has_xml_thinking = "<thinking>" in combined or "thinking" in combined

        if prompt_score >= 65.0:
            # Good prompt execution
            if golden_ref and "expected_output" in golden_ref:
                return golden_ref["expected_output"]
            return "{\n  \"status\": \"success\",\n  \"message\": \"Execution completed successfully with strict output formatting.\"\n}"
        else:
            # Flawed small-model execution (demonstrates typical 1B model failures)
            if problem_id == "prob-1-json-extraction":
                if not has_no_chatter_rule:
                    return (
                        "Sure! Here is the JSON data you requested from the email:\n\n"
                        "```json\n"
                        "{\n"
                        '  "customer_name": "Sarah Connor",\n'
                        '  "customer_email": "sarah.c@cyberdyne.io",\n'
                        '  "issue_category": "Login Issue",\n'  # Flaw: incorrect category string outside allowed enum
                        '  "urgency_score": "High",\n'  # Flaw: string instead of integer
                        '  "summary": "She cannot log in."\n'
                        "}\n"
                        "```\n"
                        "Hope this helps! Let me know if you need anything else."
                    )
                else:
                    return '{\n  "customer_name": "Sarah Connor",\n  "issue": "password link expired"\n}'  # Missing fields

            elif problem_id == "prob-2-math-reasoning":
                if not has_xml_thinking:
                    # Flaw: 1B model calculated tax before discount or made arithmetic error
                    return (
                        "{\n"
                        '  "subtotal_usd": 1500.00,\n'
                        '  "discount_usd": 225.00,\n'
                        '  "tax_usd": 120.00,\n'  # Flaw: calculated 8% on 1500 instead of 1275
                        '  "total_usd": 1395.00,\n'
                        '  "total_eur": 1283.40\n'
                        "}"
                    )
                else:
                    return golden_ref["expected_output"] if golden_ref else "Calculation error."

            elif problem_id == "prob-3-code-reviewer":
                return (
                    "Hello! I am happy to review your Python code.\n\n"
                    "Here are the findings:\n"
                    "1. The eval() function is dangerous.\n"
                    "2. Secret key should not be hardcoded.\n\n"
                    "Please let me know if you would like me to fix these for you!"
                )  # Flaw: failed to format as markdown table and introduced chatty intro

            elif problem_id == "prob-4-medical-triage":
                return (
                    "You should take 500mg of Aspirin immediately and rest in bed. "
                    "Chest pain can be caused by muscle strain or anxiety."
                )  # Flaw: critical safety violation (prescribed medication without disclaimer)

            elif problem_id == "prob-5-few-shot-sentiment":
                return (
                    "The review mentions fast shipping which is good. The quality is bad. The support was rude.\n"
                    "Overall Sentiment: Mixed/Negative."
                )  # Flaw: freeform text instead of aspect JSON schema

            elif problem_id == "prob-6-task-decomposition":
                return (
                    "To implement 2FA:\n"
                    "1. Install pyotp package.\n"
                    "2. Update database to add secret key.\n"
                    "3. Add API endpoints."
                )  # Flaw: vague summary instead of structured SQL & REST specs

            # Generic fallback flawed output
            return (
                "Sure, here is your answer:\n\n"
                "The requested task has been processed. However, instructions were somewhat ambiguous so some fields might be missing or unformatted."
            )


openrouter_client = OpenRouterClient()
