from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# --- Problem & Evaluation Schemas ---
class Problem(BaseModel):
    id: str = Field(..., description="Unique problem identifier")
    title: str = Field(..., description="Title of the problem")
    category: str = Field(..., description="Category of prompt engineering task")
    difficulty: str = Field(..., description="Difficulty level (Easy, Medium, Hard)")
    description: str = Field(..., description="Full problem description and instructions")
    small_model_recommended: str = Field(..., description="Recommended small model ID for testing")
    golden_prompt_reference: Dict[str, Any] = Field(
        ..., description="Golden reference prompt and expected output"
    )
    test_cases: List[Dict[str, Any]] = Field(default_factory=list, description="Test cases for evaluation")
    evaluation_criteria: List[str] = Field(default_factory=list, description="Key criteria evaluated for this problem")


class PromptEvaluationRequest(BaseModel):
    problem_id: str = Field(..., description="ID of the problem being solved")
    system_prompt: str = Field(..., description="System instructions provided to the model")
    user_prompt: str = Field(..., description="User prompt or input template provided to the model")
    selected_model: str = Field(
        default="meta-llama/llama-3.2-1b-instruct",
        description="Target small model ID selected for evaluation",
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(default=0.95, ge=0.0, le=1.0, description="Top-p nucleus sampling parameter")


class StandardCheck(BaseModel):
    standard_name: str = Field(..., description="Standard category: Google / Anthropic / OpenAI / Small Model")
    criterion: str = Field(..., description="Specific rule or standard criterion being checked")
    passed: bool = Field(..., description="Whether the prompt passed this specific check")
    feedback: str = Field(..., description="Detailed feedback on why it passed or failed")
    impact_score: float = Field(..., description="Score weight or impact (0.0 to 10.0)")


class PromptEvaluationResponse(BaseModel):
    overall_score: float = Field(..., description="Overall score percentage (0-100)")
    small_model_output: str = Field(..., description="Actual output returned by the small model")
    golden_output: str = Field(..., description="Expected baseline golden output for comparison")
    standard_checks: List[StandardCheck] = Field(..., description="List of standard compliance checks")
    category_scores: Dict[str, float] = Field(
        ..., description="Scores breakdown by category (Google, Anthropic, OpenAI, Small Model)"
    )
    actionable_suggestions: List[str] = Field(
        ..., description="Actionable recommendations to improve prompt for small LLMs"
    )
    execution_time_ms: float = Field(..., description="Execution time in milliseconds")


# --- Task Scenario Schema ---
class TaskScenario(BaseModel):
    id: str = Field(..., description="Unique scenario identifier")
    title: str = Field(..., description="Scenario title")
    category: str = Field(..., description="Domain category")
    difficulty: str = Field(..., description="Difficulty level (Easy, Medium, Hard, Expert)")
    objective: str = Field(..., description="Primary prompt engineering goal")
    background_context: str = Field(..., description="Detailed background scenario context")
    input_data: str = Field(..., description="Sample input payload or raw context provided")
    target_format: str = Field(..., description="Expected output format specification")
    starter_system_prompt: str = Field(..., description="Starter template for system prompt")
    starter_user_prompt: str = Field(..., description="Starter template for user prompt")

    @property
    def input_data_payload(self) -> str:
        return self.input_data


# --- Google Guardrails Schemas ---
class GoogleGuardrailCheck(BaseModel):
    step_name: str = Field(..., description="Google Framework Step: Task, Context, References, Evaluate, Iterate")
    element: str = Field(..., description="Specific element evaluated")
    passed: bool = Field(..., description="Whether criterion was satisfied")
    feedback: str = Field(..., description="Detailed explanation of compliance or failure")
    impact_weight: int = Field(..., description="Weight of check toward overall score")


class GoogleGuardrailEvaluationRequest(BaseModel):
    system_prompt: str = Field(default="", description="System prompt content")
    user_prompt: str = Field(default="", description="User prompt content")


class GooglePromptAnalysis(BaseModel):
    overall_score: int = Field(..., description="Overall 0-100% Google Framework compliance score")
    passed_steps: List[str] = Field(..., description="List of framework steps that passed")
    missing_steps: List[str] = Field(..., description="List of framework steps that need improvement")
    category_breakdown: Dict[str, float] = Field(..., description="Score breakdown by T-C-R-E-I step (0-100%)")
    checks: List[GoogleGuardrailCheck] = Field(..., description="Detailed breakdown of individual checks")
    actionable_suggestions: List[str] = Field(..., description="Actionable recommendations to meet Google guardrails")


# --- MCQ Bank Schemas ---
class MCQOption(BaseModel):
    id: str = Field(..., description="Option identifier")
    text: str = Field(..., description="Option label/text")
    is_correct: bool = Field(..., description="Whether this option is correct")
    explanation: str = Field(..., description="Detailed explanation of why correct or incorrect")


class MCQQuestion(BaseModel):
    id: str = Field(..., description="Unique question identifier")
    title: str = Field(..., description="Question title")
    difficulty: str = Field(..., description="Difficulty level (Easy, Medium, Hard, Expert)")
    demo_prompt: str = Field(..., description="Prompt snippet evaluated in the question")
    scenario_description: str = Field(..., description="Scenario context and task instructions")
    options: List[MCQOption] = Field(..., description="Multi-select choices")
    google_framework_mapping: List[str] = Field(..., description="Associated T-C-R-E-I steps evaluated")
