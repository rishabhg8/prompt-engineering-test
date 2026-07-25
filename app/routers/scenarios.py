from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import TaskScenario
from app.services.task_scenarios import task_scenario_bank

router = APIRouter(prefix="/api/scenarios", tags=["Task Scenarios"])


@router.get("", response_model=List[TaskScenario], summary="List all curated Task Scenarios")
def get_all_scenarios():
    """Retrieve bank of curated Task Scenarios for candidates."""
    return task_scenario_bank.get_all()


@router.get("/{scenario_id}", response_model=TaskScenario, summary="Get Task Scenario by ID")
def get_scenario_by_id(scenario_id: str):
    """Retrieve a specific Task Scenario by its unique identifier."""
    scenario = task_scenario_bank.get_by_id(scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task scenario with ID '{scenario_id}' not found.",
        )
    return scenario
