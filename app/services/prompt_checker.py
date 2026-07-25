import re
from typing import List, Dict, Tuple, Any, Optional
from app.models.schemas import StandardCheck


class PromptChecker:
    """
    Evaluates prompts against industry standard guidelines from Google, Anthropic, and OpenAI,
    with specific optimization heuristics for 1B-3B parameter small LLMs.
    """

    @classmethod
    def evaluate(cls, system_prompt: str, user_prompt: str, problem_info: Optional[Dict[str, Any]] = None):
        instance = cls()
        return instance.analyze_prompt(system_prompt, user_prompt, problem_info)

    def analyze_prompt(
        self, system_prompt: str, user_prompt: str, problem_info: Optional[Dict[str, Any]] = None
    ) -> Tuple[float, List[StandardCheck], Dict[str, float], List[str]]:
        combined_text = f"{system_prompt}\n{user_prompt}"
        checks: List[StandardCheck] = []
        suggestions: List[str] = []

        # --- GOOGLE STANDARDS ---
        google_score, google_checks, google_suggs = self._check_google_standards(
            system_prompt, user_prompt, combined_text
        )
        checks.extend(google_checks)
        suggestions.extend(google_suggs)

        # --- ANTHROPIC STANDARDS ---
        anthropic_score, anthropic_checks, anthropic_suggs = self._check_anthropic_standards(
            system_prompt, user_prompt, combined_text
        )
        checks.extend(anthropic_checks)
        suggestions.extend(anthropic_suggs)

        # --- OPENAI STANDARDS ---
        openai_score, openai_checks, openai_suggs = self._check_openai_standards(
            system_prompt, user_prompt, combined_text
        )
        checks.extend(openai_checks)
        suggestions.extend(openai_suggs)

        # --- SMALL MODEL SUITABILITY ---
        small_model_score, small_checks, small_suggs = self._check_small_model_suitability(
            system_prompt, user_prompt, combined_text
        )
        checks.extend(small_checks)
        suggestions.extend(small_suggs)

        category_scores = {
            "Google Standards": round(google_score, 1),
            "Anthropic Standards": round(anthropic_score, 1),
            "OpenAI Standards": round(openai_score, 1),
            "Small Model Suitability": round(small_model_score, 1),
        }

        # Overall score is a weighted average favoring Small Model Suitability
        overall = (
            google_score * 0.25
            + anthropic_score * 0.25
            + openai_score * 0.25
            + small_model_score * 0.25
        )
        overall_score = round(min(max(overall, 0.0), 100.0), 1)

        # Remove duplicate suggestions while preserving order
        unique_suggestions = []
        for sug in suggestions:
            if sug not in unique_suggestions:
                unique_suggestions.append(sug)

        return overall_score, checks, category_scores, unique_suggestions

    def _check_google_standards(
        self, system_prompt: str, user_prompt: str, combined: str
    ) -> Tuple[float, List[StandardCheck], List[str]]:
        checks = []
        suggestions = []
        passed_count = 0
        total_checks = 4

        # 1. Clear Persona / Role definition
        persona_keywords = [
            "you are", "role:", "act as", "your task", "you function as", "expert", "assistant", "agent"
        ]
        has_persona = any(kw in system_prompt.lower() for kw in persona_keywords)
        if has_persona:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Google Standards",
                    criterion="Clear Persona & Role Definition",
                    passed=True,
                    feedback="System prompt explicitly defines a persona or role.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Google Standards",
                    criterion="Clear Persona & Role Definition",
                    passed=False,
                    feedback="Missing explicit persona or role assignment in system prompt (e.g., 'You are an expert...').",
                    impact_score=2.5,
                )
            )
            suggestions.append("Add a clear persona or role in the system prompt (e.g., 'You are an expert data extraction assistant.') to steer small model behavior.")

        # 2. Explicit Output Formatting constraints
        format_keywords = ["json", "format", "schema", "output structure", "respond with", "return a", "markdown"]
        has_format = any(kw in combined.lower() for kw in format_keywords)
        if has_format:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Google Standards",
                    criterion="Explicit Output Formatting Constraints",
                    passed=True,
                    feedback="Prompt explicitly specifies target output format or schema constraints.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Google Standards",
                    criterion="Explicit Output Formatting Constraints",
                    passed=False,
                    feedback="Missing concrete output format directives (e.g. JSON, exact schema).",
                    impact_score=2.5,
                )
            )
            suggestions.append("Explicitly state the exact expected output format (e.g., JSON schema, list, or markdown table) to prevent model drift.")

        # 3. Structured Context Delimiters
        delimiters = ['"""', "```", "###", "---", "<context>", "<input>", "==="]
        has_delimiters = any(delim in combined for delim in delimiters)
        if has_delimiters:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Google Standards",
                    criterion="Structured Context Delimiters",
                    passed=True,
                    feedback="Uses clear section delimiters (e.g., ```, ###, or triple quotes) to partition input data.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Google Standards",
                    criterion="Structured Context Delimiters",
                    passed=False,
                    feedback="Input text or data is not separated from instructions using structural delimiters.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Wrap input data or context using clear delimiters like triple quotes `\"\"\"` or markdown backticks ```` ``` ````.")

        # 4. Zero-shot / Few-shot Examples
        example_keywords = ["example:", "input:", "output:", "sample:", "few-shot", "e.g.,"]
        has_examples = any(kw in combined.lower() for kw in example_keywords)
        if has_examples:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Google Standards",
                    criterion="Zero/Few-Shot Example Guidance",
                    passed=True,
                    feedback="Prompt provides sample input/output examples to anchor model responses.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Google Standards",
                    criterion="Zero/Few-Shot Example Guidance",
                    passed=False,
                    feedback="No input/output examples provided to demonstrate desired output format.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Provide 1-2 concise few-shot examples (Input -> Output pair) so 1B models can copy the target structure.")

        score = (passed_count / total_checks) * 100.0
        return score, checks, suggestions

    def _check_anthropic_standards(
        self, system_prompt: str, user_prompt: str, combined: str
    ) -> Tuple[float, List[StandardCheck], List[str]]:
        checks = []
        suggestions = []
        passed_count = 0
        total_checks = 3

        # 1. XML Tags for Structural Framing
        xml_tag_pattern = r"<\/?[a-zA-Z_0-9\-]+>"
        xml_tags = re.findall(xml_tag_pattern, combined)
        has_xml = len(xml_tags) >= 2
        if has_xml:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Anthropic Standards",
                    criterion="XML Structural Tags",
                    passed=True,
                    feedback=f"Prompt uses XML tags ({', '.join(set(xml_tags[:4]))}) to structure context and instructions.",
                    impact_score=3.33,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Anthropic Standards",
                    criterion="XML Structural Tags",
                    passed=False,
                    feedback="Missing XML tags (e.g., <context>, <instructions>, <data>) for clean prompt framing.",
                    impact_score=3.33,
                )
            )
            suggestions.append("Use XML tags like `<context>`, `<instructions>`, and `<input>` to cleanly separate data components for small LLMs.")

        # 2. Chain-of-Thought / Thinking Directive
        cot_keywords = [
            "<thinking>", "think step", "reason step", "scratchpad", "chain of thought",
            "show your reasoning", "analyze first", "<reasoning>"
        ]
        has_cot = any(kw in combined.lower() for kw in cot_keywords)
        if has_cot:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Anthropic Standards",
                    criterion="Explicit CoT / Thinking Directives",
                    passed=True,
                    feedback="Prompt instructs the model to reason through the problem step-by-step or inside <thinking> tags.",
                    impact_score=3.33,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Anthropic Standards",
                    criterion="Explicit CoT / Thinking Directives",
                    passed=False,
                    feedback="No explicit thinking or reasoning directives found to guide model logic before generating output.",
                    impact_score=3.33,
                )
            )
            suggestions.append("Direct the model to perform reasoning step-by-step inside `<thinking>` tags before rendering final output.")

        # 3. Clear Output Boundaries / Tag-based Enclosure
        boundary_keywords = ["<output>", "respond in", "<result>", "<json>", "final answer"]
        has_boundary = any(kw in combined.lower() for kw in boundary_keywords) or bool(re.search(r"<\/?[a-zA-Z0-9]+>", user_prompt))
        if has_boundary:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Anthropic Standards",
                    criterion="Clear Output Boundaries",
                    passed=True,
                    feedback="Prompt specifies output tag boundaries or explicit final response section.",
                    impact_score=3.33,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Anthropic Standards",
                    criterion="Clear Output Boundaries",
                    passed=False,
                    feedback="Lacks explicit tag boundaries (e.g., <output>) to isolate model answers from reasoning.",
                    impact_score=3.33,
                )
            )
            suggestions.append("Ask the model to wrap its final answer inside `<output>` tags to isolate the payload from explanations.")

        score = (passed_count / total_checks) * 100.0
        return score, checks, suggestions

    def _check_openai_standards(
        self, system_prompt: str, user_prompt: str, combined: str
    ) -> Tuple[float, List[StandardCheck], List[str]]:
        checks = []
        suggestions = []
        passed_count = 0
        total_checks = 4

        # 1. System / User Separation
        has_system_sep = len(system_prompt.strip()) >= 15 and len(user_prompt.strip()) >= 10
        if has_system_sep:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="OpenAI Standards",
                    criterion="System vs User Prompt Separation",
                    passed=True,
                    feedback="Distinct system instruction and user prompt components are properly utilized.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="OpenAI Standards",
                    criterion="System vs User Prompt Separation",
                    passed=False,
                    feedback="System prompt is too brief or all instructions are crammed into user prompt.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Separate persistent role & rule directives into System Prompt, keeping dynamic variables in User Prompt.")

        # 2. Markdown Sectioning
        has_markdown_headers = bool(re.search(r"^#{1,4}\s", combined, re.MULTILINE)) or "**" in combined
        if has_markdown_headers:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="OpenAI Standards",
                    criterion="Markdown Sectioning & Organization",
                    passed=True,
                    feedback="Uses markdown headers or bold headings to structure instructions logically.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="OpenAI Standards",
                    criterion="Markdown Sectioning & Organization",
                    passed=False,
                    feedback="Prompt lacks clear markdown headers (e.g., ### Instructions, ### Context).",
                    impact_score=2.5,
                )
            )
            suggestions.append("Use Markdown section headers (e.g. `### Instructions`, `### Constraints`) for high legibility.")

        # 3. Step-by-Step Reasoning Triggers
        step_keywords = ["step by step", "step-by-step", "break down", "reason through", "calculate", "logic"]
        has_step = any(kw in combined.lower() for kw in step_keywords)
        if has_step:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="OpenAI Standards",
                    criterion="Step-by-Step Execution Trigger",
                    passed=True,
                    feedback="Includes step-by-step reasoning instructions to prevent short-circuiting on complex tasks.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="OpenAI Standards",
                    criterion="Step-by-Step Execution Trigger",
                    passed=False,
                    feedback="No explicit trigger asking the model to process instructions step-by-step.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Include an instruction such as 'Think step-by-step before producing your final answer'.")

        # 4. Negative Constraints
        negative_keywords = [
            "do not", "don't", "never", "avoid", "no conversational", "only return", "no extra text", "without intro"
        ]
        has_negative = any(kw in combined.lower() for kw in negative_keywords)
        if has_negative:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="OpenAI Standards",
                    criterion="Explicit Negative Constraints",
                    passed=True,
                    feedback="Prompt defines clear negative constraints ('do not include', 'only return JSON').",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="OpenAI Standards",
                    criterion="Explicit Negative Constraints",
                    passed=False,
                    feedback="Missing explicit negative guardrails to prevent unwanted intro/outro chatter.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Add explicit negative constraints (e.g., 'Do NOT include conversational filler or markdown wrapping outside JSON').")

        score = (passed_count / total_checks) * 100.0
        return score, checks, suggestions

    def _check_small_model_suitability(
        self, system_prompt: str, user_prompt: str, combined: str
    ) -> Tuple[float, List[StandardCheck], List[str]]:
        checks = []
        suggestions = []
        passed_count = 0
        total_checks = 4

        # 1. Strict Schema Example for 1B Models
        has_json_schema = "{" in combined and "}" in combined
        if has_json_schema:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Small Model Suitability",
                    criterion="Concrete Output Schema Template",
                    passed=True,
                    feedback="Provides exact structural json/template representation required for 1B-3B models.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Small Model Suitability",
                    criterion="Concrete Output Schema Template",
                    passed=False,
                    feedback="Small 1B models drift when output schema is described only in prose without concrete code/JSON templates.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Small LLMs (1B-3B) need a raw concrete `{...}` template example in the prompt, not just description text.")

        # 2. Strict 'No Chatter' Rule for Small Models
        chatter_keywords = ["only return raw", "do not write anything else", "no conversational", "no prelude", "no codeblocks"]
        has_chatter_guard = any(kw in combined.lower() for kw in chatter_keywords)
        if has_chatter_guard:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Small Model Suitability",
                    criterion="Strict Zero-Chatter Directive",
                    passed=True,
                    feedback="Explicitly forbids small models from prepending conversational filler ('Sure, here is...').",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Small Model Suitability",
                    criterion="Strict Zero-Chatter Directive",
                    passed=False,
                    feedback="Small models tend to output 'Here is your JSON:' unless strictly forbidden.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Add directive: 'Return ONLY the JSON payload. Do NOT write intros like \"Here is the JSON:\"'.")

        # 3. Prompt Clarity and Length (Not overly bloated or ambiguous)
        length = len(combined.split())
        if 20 <= length <= 600:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Small Model Suitability",
                    criterion="Prompt Length & Focus",
                    passed=True,
                    feedback=f"Prompt is concise and focused ({length} words), ideal for 1B-3B model context windows.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Small Model Suitability",
                    criterion="Prompt Length & Focus",
                    passed=False,
                    feedback=f"Prompt length ({length} words) is either too minimal (<20 words) or too bloated for tight attention spans of small LLMs.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Keep small model prompts between 50-400 words to avoid context dilution and attention drift.")

        # 4. Fallback Handling Directive
        fallback_keywords = ["if missing", "default to", "return null", "if unknown", "fallback", "n/a"]
        has_fallback = any(kw in combined.lower() for kw in fallback_keywords)
        if has_fallback:
            passed_count += 1
            checks.append(
                StandardCheck(
                    standard_name="Small Model Suitability",
                    criterion="Explicit Null / Edge-Case Fallback",
                    passed=True,
                    feedback="Includes instructions for handling missing data or edge cases cleanly.",
                    impact_score=2.5,
                )
            )
        else:
            checks.append(
                StandardCheck(
                    standard_name="Small Model Suitability",
                    criterion="Explicit Null / Edge-Case Fallback",
                    passed=False,
                    feedback="Does not instruct the model how to handle missing data or missing parameters.",
                    impact_score=2.5,
                )
            )
            suggestions.append("Specify fallback behavior (e.g. 'If a field is missing, set value to null').")

        score = (passed_count / total_checks) * 100.0
        return score, checks, suggestions


prompt_checker = PromptChecker()
