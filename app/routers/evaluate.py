from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    PromptEvaluationRequest,
    PromptEvaluationResponse,
    GoogleGuardrailEvaluationRequest,
    GooglePromptAnalysis,
)
from app.services.problem_bank import problem_bank
from app.services.prompt_checker import prompt_checker
from app.services.openrouter_client import openrouter_client
from app.services.google_guardrails import google_guardrails

router = APIRouter(prefix="/api/evaluate", tags=["Evaluation"])


@router.post("", response_model=PromptEvaluationResponse, summary="Evaluate prompt quality and execute on small LLM")
async def evaluate_prompt(request: PromptEvaluationRequest):
    """
    Evaluates system and user prompts against Google, Anthropic, OpenAI, and Small Model engineering standards,
    runs the prompt on the selected small LLM (or mock engine), and returns detailed analysis, output comparison,
    and actionable feedback.
    """
    problem = problem_bank.get_by_id(request.problem_id)
    problem_dict = problem.dict() if problem else None

    # 1. Analyze prompt quality against standard criteria
    overall_score, standard_checks, category_scores, suggestions = prompt_checker.analyze_prompt(
        system_prompt=request.system_prompt,
        user_prompt=request.user_prompt,
        problem_info=problem_dict,
    )

    # 2. Execute completion on OpenRouter (or Fallback Mock Engine)
    small_model_output, exec_time_ms = await openrouter_client.generate_completion(
        system_prompt=request.system_prompt,
        user_prompt=request.user_prompt,
        model_id=request.selected_model,
        temperature=request.temperature,
        top_p=request.top_p,
        problem_id=request.problem_id,
        prompt_score=overall_score,
    )

    # 3. Retrieve golden reference output baseline
    golden_output = ""
    if problem and problem.golden_prompt_reference:
        golden_output = problem.golden_prompt_reference.get("expected_output", "")

    return PromptEvaluationResponse(
        overall_score=overall_score,
        small_model_output=small_model_output,
        golden_output=golden_output,
        standard_checks=standard_checks,
        category_scores=category_scores,
        actionable_suggestions=suggestions,
        execution_time_ms=exec_time_ms,
    )


@router.post(
    "/guardrails",
    response_model=GooglePromptAnalysis,
    summary="Evaluate candidate prompts against Google Guardrails (T-C-R-E-I)",
)
def evaluate_google_guardrails(request: GoogleGuardrailEvaluationRequest):
    """
    Evaluates candidate prompts against Google's 5-Step Framework (Task, Context, References, Evaluate, Iterate).
    Calculates 0-100% compliance score, passed/missing steps, category breakdown, and actionable fix suggestions.
    """
    return google_guardrails.analyze(
        system_prompt=request.system_prompt,
        user_prompt=request.user_prompt,
    )
