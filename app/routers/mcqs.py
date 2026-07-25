from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import MCQQuestion
from app.services.mcq_bank import mcq_bank

router = APIRouter(prefix="/api/mcqs", tags=["MCQ Bank"])


@router.get("", response_model=List[MCQQuestion], summary="List all prompt engineering MCQs")
def get_all_mcqs():
    """Retrieve bank of multi-select MCQ questions evaluating prompt engineering concepts."""
    return mcq_bank.get_all()


@router.get("/{mcq_id}", response_model=MCQQuestion, summary="Get MCQ Question by ID")
def get_mcq_by_id(mcq_id: str):
    """Retrieve a specific MCQ question by its ID."""
    mcq = mcq_bank.get_by_id(mcq_id)
    if not mcq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MCQ with ID '{mcq_id}' not found.",
        )
    return mcq
