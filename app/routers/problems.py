from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import Problem
from app.services.problem_bank import problem_bank

router = APIRouter(prefix="/api/problems", tags=["Problems"])


@router.get("", response_model=List[Problem], summary="List all prompt engineering problems")
def get_all_problems():
    """
    Returns the list of all curated prompt engineering problems categorized by challenge type.
    """
    return problem_bank.get_all()


@router.get("/{problem_id}", response_model=Problem, summary="Get problem details by ID")
def get_problem(problem_id: str):
    """
    Retrieves full details for a specific problem ID, including description, recommended model,
    golden reference prompt, test cases, and evaluation criteria.
    """
    problem = problem_bank.get_by_id(problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with ID '{problem_id}' not found.",
        )
    return problem
