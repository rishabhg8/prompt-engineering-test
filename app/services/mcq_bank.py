from typing import List, Optional
from app.models.schemas import MCQQuestion, MCQOption


MCQ_QUESTIONS: List[MCQQuestion] = [
    MCQQuestion(
        id="mcq-1",
        title="Flawed Customer Support Prompt Analysis",
        difficulty="Easy",
        demo_prompt="Write a email to a customer who is angry about late delivery.",
        scenario_description=(
            "A junior prompt engineer submitted this prompt to generate customer service emails. "
            "Evaluate this prompt against Google's 5-Step Framework (Task, Context, References, Evaluate, Iterate) "
            "and select ALL correct statements describing what is wrong or missing."
        ),
        options=[
            MCQOption(
                id="opt-1",
                text="Missing Persona: Fails to specify the role (e.g. 'You are an empathetic Lead Support Specialist').",
                is_correct=True,
                explanation="CORRECT. Google's Task framework mandates assigning a clear persona to set tone and perspective."
            ),
            MCQOption(
                id="opt-2",
                text="Missing Context: Fails to provide details like order ID, reason for delay, or compensation offer.",
                is_correct=True,
                explanation="CORRECT. Google's Context framework requires scenario details so the model doesn't hallucinate missing facts."
            ),
            MCQOption(
                id="opt-3",
                text="Missing Output Format & Length Constraints: Does not specify format, tone, or word count limit.",
                is_correct=True,
                explanation="CORRECT. Specifying format (e.g. '3 paragraphs, professional & apologizing tone') prevents vague output."
            ),
            MCQOption(
                id="opt-4",
                text="Correctly includes a few-shot reference example.",
                is_correct=False,
                explanation="INCORRECT. The prompt contains zero reference examples or sample emails."
            )
        ],
        google_framework_mapping=["Task", "Context", "References"]
    ),
    MCQQuestion(
        id="mcq-2",
        title="Evaluating a Code Review Prompt",
        difficulty="Medium",
        demo_prompt=(
            "System Prompt: You are a Senior Python Security Auditor.\n"
            "User Prompt: Review the following Python function for SQL injection vulnerabilities:\n"
            "def get_user(db, name):\n"
            "    return db.query(f'SELECT * FROM users WHERE name = {name}')"
        ),
        scenario_description=(
            "Analyze this security review prompt against Google's Prompting Framework. "
            "Select ALL correct statements regarding its strengths and missing elements."
        ),
        options=[
            MCQOption(
                id="opt-1",
                text="Strengths: Properly defines a clear persona ('Senior Python Security Auditor') in System Prompt.",
                is_correct=True,
                explanation="CORRECT. Persona definition follows Google's Task step."
            ),
            MCQOption(
                id="opt-2",
                text="Strengths: Provides specific context and code payload in the User Prompt.",
                is_correct=True,
                explanation="CORRECT. Context includes the target code snippet."
            ),
            MCQOption(
                id="opt-3",
                text="Missing Element: Does not request Chain-of-Thought reasoning or structured output format (e.g. Markdown vulnerability report).",
                is_correct=True,
                explanation="CORRECT. Asking the model to think step-by-step or format results as a vulnerability matrix enhances accuracy."
            ),
            MCQOption(
                id="opt-4",
                text="Missing Element: The prompt is completely invalid because system prompts cannot specify roles.",
                is_correct=False,
                explanation="INCORRECT. System prompts are the recommended location for persona and role definitions."
            )
        ],
        google_framework_mapping=["Task", "Context", "Iterate"]
    ),
    MCQQuestion(
        id="mcq-3",
        title="Multi-Step Math & Logic Prompt Evaluation",
        difficulty="Hard",
        demo_prompt=(
            "Calculate the total cost: A store sells apples for $2 each. John bought 5 apples, "
            "3 oranges at $3 each, and got a 10% discount. Return the number."
        ),
        scenario_description=(
            "When tested on a small 1.5B parameter LLM, this prompt frequently produces wrong math answers. "
            "Select ALL correct improvement techniques based on Google's key takeaways and research paper techniques."
        ),
        options=[
            MCQOption(
                id="opt-1",
                text="Instruct the model to use Chain-of-Thought (CoT) prompting ('Think step-by-step before giving the final answer').",
                is_correct=True,
                explanation="CORRECT. CoT prompting breaks multi-step math into intermediate steps, drastically reducing calculation errors."
            ),
            MCQOption(
                id="opt-2",
                text="Encapsulate intermediate reasoning inside scratchpad or XML tags (e.g., <thinking>...</thinking>).",
                is_correct=True,
                explanation="CORRECT. XML scratchpad directives isolate intermediate logic from final output."
            ),
            MCQOption(
                id="opt-3",
                text="Provide a 1-shot reference example showing how a similar math problem is solved step-by-step.",
                is_correct=True,
                explanation="CORRECT. Few-shot reference examples anchor small LLM reasoning."
            ),
            MCQOption(
                id="opt-4",
                text="Remove all numbers from the context.",
                is_correct=False,
                explanation="INCORRECT. Removing numbers prevents the model from solving the problem."
            )
        ],
        google_framework_mapping=["References", "Iterate"]
    ),
    MCQQuestion(
        id="mcq-4",
        title="Medical Guardrails & System Persona Enforcement",
        difficulty="Expert",
        demo_prompt=(
            "System Prompt: You are a helpful medical assistant. Always answer user medical questions.\n"
            "User Prompt: What is the exact dosage of Amoxicillin I should take for a severe tooth infection?"
        ),
        scenario_description=(
            "A patient intake portal prompt was tested and generated specific antibiotic dosage advice without physician oversight, "
            "violating medical compliance. Select ALL prompt engineering guardrail techniques that should be applied to fix this prompt."
        ),
        options=[
            MCQOption(
                id="opt-1",
                text="Introduce explicit refusal guardrails in the System Prompt forbidding medical diagnosis or medication dosage prescriptions.",
                is_correct=True,
                explanation="CORRECT. Guardrails in System Prompts strictly prevent dangerous unverified medical advice."
            ),
            MCQOption(
                id="opt-2",
                text="Add negative constraints ('Do NOT prescribe specific medications or calculate dosages under any circumstances').",
                is_correct=True,
                explanation="CORRECT. Google's Iterate framework highlights negative constraints as vital safety guardrails."
            ),
            MCQOption(
                id="opt-3",
                text="Specify a required fallback action ('Direct the user to consult a licensed healthcare professional or pharmacist').",
                is_correct=True,
                explanation="CORRECT. Providing safe fallback directives ensures user helpfulness without legal/medical risk."
            ),
            MCQOption(
                id="opt-4",
                text="Increase sampling temperature to 1.5 to make dosage estimates more creative.",
                is_correct=False,
                explanation="INCORRECT. Higher temperature increases hallucination risk and is dangerous for medical prompts."
            )
        ],
        google_framework_mapping=["Task", "Iterate"]
    )
]


class MCQBank:
    """Service for managing MCQ questions."""

    def get_all(self) -> List[MCQQuestion]:
        return MCQ_QUESTIONS

    def get_by_id(self, mcq_id: str) -> Optional[MCQQuestion]:
        for q in MCQ_QUESTIONS:
            if q.id == mcq_id:
                return q
        return None


mcq_bank = MCQBank()


def get_all_mcqs() -> List[MCQQuestion]:
    return mcq_bank.get_all()


def get_mcq_by_id(mcq_id: str) -> Optional[MCQQuestion]:
    return mcq_bank.get_by_id(mcq_id)
