import re
from typing import List, Dict, Tuple, Any
from app.models.schemas import (
    GoogleGuardrailCheck,
    GooglePromptAnalysis,
    GoogleGuardrailEvaluationRequest,
)


class GoogleGuardrailsEvaluator:
    """
    Evaluates candidate prompts against Google's 5-Step Framework (T-C-R-E-I):
    - Task: Persona, explicit task objective, output format constraint.
    - Context: Background scenario details, target audience, domain facts.
    - References: Few-shot exemplars, sample inputs/outputs.
    - Evaluate: Success criteria or metric definitions.
    - Iterate: Negative constraints ("do not..."), step-by-step reasoning directives ("think step by step"), or sub-prompt breakdown.
    """

    @classmethod
    def analyze(cls, system_prompt: str, user_prompt: str) -> GooglePromptAnalysis:
        sys_p = system_prompt or ""
        usr_p = user_prompt or ""
        combined = f"{sys_p}\n{usr_p}".strip()
        checks: List[GoogleGuardrailCheck] = []
        suggestions: List[str] = []

        step_weights = {"Task": 20, "Context": 20, "References": 20, "Evaluate": 20, "Iterate": 20}
        step_scores: Dict[str, float] = {"Task": 0.0, "Context": 0.0, "References": 0.0, "Evaluate": 0.0, "Iterate": 0.0}

        # ==========================================
        # STEP 1: TASK (Persona, Objective, Format)
        # ==========================================
        has_persona = bool(re.search(r'\b(you are|act as|your role|as an? \w+ (expert|assistant|specialist|auditor|engineer|doctor)|persona)\b', sys_p, re.IGNORECASE))
        if not has_persona:
            has_persona = bool(re.search(r'\b(you are|act as|your role|as an? \w+ (expert|assistant|specialist|auditor|engineer|doctor)|persona)\b', combined, re.IGNORECASE))

        has_objective = bool(re.search(r'\b(task|objective|goal|convert|extract|recommend|generate|analyze|summarize|create|build|write|triage)\b', combined, re.IGNORECASE))
        has_format = bool(re.search(r'\b(json|xml|markdown|bullet|list|table|csv|format|respond only with|output structure|schema)\b', combined, re.IGNORECASE))

        task_sub_passed = sum([has_persona, has_objective, has_format])
        task_ratio = task_sub_passed / 3.0
        step_scores["Task"] = round(task_ratio * 100.0, 1)

        checks.append(GoogleGuardrailCheck(
            step_name="Task",
            element="Persona & Role Assignment",
            passed=has_persona,
            feedback="Assigned explicit persona/role in System Prompt." if has_persona else "Missing Persona: Assign a clear role (e.g., 'You are a Senior Cloud Solutions Architect') to guide model behavior.",
            impact_weight=7
        ))
        checks.append(GoogleGuardrailCheck(
            step_name="Task",
            element="Explicit Task Objective",
            passed=has_objective,
            feedback="Explicit task objective defined." if has_objective else "Missing Objective: State the explicit goal or action verb for the task.",
            impact_weight=7
        ))
        checks.append(GoogleGuardrailCheck(
            step_name="Task",
            element="Output Format Constraint",
            passed=has_format,
            feedback="Output format explicitly specified." if has_format else "Missing Output Format: Explicitly require JSON, Markdown table, or structured schema.",
            impact_weight=6
        ))

        if not has_persona:
            suggestions.append("Task Step: Define a distinct persona in the system prompt (e.g., 'You are an empathetic Customer Support Lead').")
        if not has_format:
            suggestions.append("Task Step: Specify strict output format constraints (e.g., 'Output strictly valid JSON with keys: status, summary').")

        # ==========================================
        # STEP 2: CONTEXT (Scenario, Audience, Domain Facts)
        # ==========================================
        has_scenario = bool(re.search(r'\b(background|scenario|context|given|situation|problem|customer|patient|database|cloud|gcp|migration)\b', combined, re.IGNORECASE))
        has_audience_domain = bool(re.search(r'\b(audience|user|client|domain|enterprise|technical|non-technical|stakeholder|facts|policy)\b', combined, re.IGNORECASE)) or len(combined.split()) > 30

        context_sub_passed = sum([has_scenario, has_audience_domain])
        context_ratio = context_sub_passed / 2.0
        step_scores["Context"] = round(context_ratio * 100.0, 1)

        checks.append(GoogleGuardrailCheck(
            step_name="Context",
            element="Background Scenario Details",
            passed=has_scenario,
            feedback="Background scenario details provided." if has_scenario else "Missing Scenario Context: Provide relevant operational or historical context.",
            impact_weight=10
        ))
        checks.append(GoogleGuardrailCheck(
            step_name="Context",
            element="Target Audience & Domain Facts",
            passed=has_audience_domain,
            feedback="Target audience and domain facts outlined." if has_audience_domain else "Missing Target Audience/Domain Details: Clarify who the output is for or domain specific facts.",
            impact_weight=10
        ))

        if not has_scenario:
            suggestions.append("Context Step: Provide richer background context and environment constraints in the prompt.")

        # ==========================================
        # STEP 3: REFERENCES (Few-shot exemplars, inputs/outputs)
        # ==========================================
        has_exemplars = bool(re.search(r'\b(example|sample|input:|output:|exemplar|for instance|e\.g\.|reference|input data)\b', combined, re.IGNORECASE)) or ('<' in combined and '>' in combined)

        step_scores["References"] = 100.0 if has_exemplars else 0.0

        checks.append(GoogleGuardrailCheck(
            step_name="References",
            element="Few-Shot Exemplars / Reference Material",
            passed=has_exemplars,
            feedback="Includes reference exemplars or sample input/output pairs." if has_exemplars else "Missing References: Add 1-2 concrete few-shot examples (Input -> Output) to anchor generation.",
            impact_weight=20
        ))

        if not has_exemplars:
            suggestions.append("References Step: Add few-shot reference exemplars showing ideal input-to-output transformations.")

        # ==========================================
        # STEP 4: EVALUATE (Success Criteria, Metrics)
        # ==========================================
        has_criteria = bool(re.search(r'\b(success criteria|evaluated by|metric|criteria|ensure|verify|requirements|tone must be|accuracy|quality|compliance)\b', combined, re.IGNORECASE))

        step_scores["Evaluate"] = 100.0 if has_criteria else 0.0

        checks.append(GoogleGuardrailCheck(
            step_name="Evaluate",
            element="Success Criteria & Metric Definitions",
            passed=has_criteria,
            feedback="Defined success criteria or quality metrics." if has_criteria else "Missing Evaluation Criteria: Explicitly state criteria for success (e.g. 'Must maintain professional tone and 0 hallucinated facts').",
            impact_weight=20
        ))

        if not has_criteria:
            suggestions.append("Evaluate Step: Define explicit success criteria or metric definitions for prompt validation.")

        # ==========================================
        # STEP 5: ITERATE (Constraints, CoT, Sub-prompt)
        # ==========================================
        has_negative_constraints = bool(re.search(r'\b(do not|must not|never|avoid|strictly|no preamble|refuse|disclaimer)\b', combined, re.IGNORECASE))
        has_cot_directives = bool(re.search(r'\b(think step by step|chain of thought|reasoning|break down|scratchpad|<thinking>|sub-prompt|step 1|first,)\b', combined, re.IGNORECASE))

        iterate_sub_passed = sum([has_negative_constraints, has_cot_directives])
        iterate_ratio = max(iterate_sub_passed / 2.0, 1.0 if (has_negative_constraints or has_cot_directives) else 0.0)
        step_scores["Iterate"] = round(iterate_ratio * 100.0, 1)

        checks.append(GoogleGuardrailCheck(
            step_name="Iterate",
            element="Negative Constraints",
            passed=has_negative_constraints,
            feedback="Negative constraints defined ('do not...', 'must not...')." if has_negative_constraints else "Missing Negative Constraints: Add strict boundaries (e.g., 'Do not diagnose medical conditions').",
            impact_weight=10
        ))
        checks.append(GoogleGuardrailCheck(
            step_name="Iterate",
            element="Step-by-step Reasoning / CoT Directives",
            passed=has_cot_directives,
            feedback="Step-by-step reasoning or CoT directives present." if has_cot_directives else "Missing Reasoning Directives: Include 'Think step-by-step' or XML reasoning tags.",
            impact_weight=10
        ))

        if not has_negative_constraints:
            suggestions.append("Iterate Step: Introduce negative constraints ('Do not assume missing parameters', 'Never provide medical diagnoses').")
        if not has_cot_directives:
            suggestions.append("Iterate Step: Direct the model to reason step-by-step before producing final output.")

        # --- Aggregation ---
        total_possible_score = 100.0
        weighted_score = sum(step_scores[step] * (step_weights[step] / 100.0) for step in step_weights)
        overall_score = int(round(weighted_score))

        passed_steps = [step for step, score in step_scores.items() if score >= 60.0]
        missing_steps = [step for step, score in step_scores.items() if score < 60.0]

        return GooglePromptAnalysis(
            overall_score=overall_score,
            passed_steps=passed_steps,
            missing_steps=missing_steps,
            category_breakdown=step_scores,
            checks=checks,
            actionable_suggestions=suggestions,
        )


google_guardrails = GoogleGuardrailsEvaluator()
