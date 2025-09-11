from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query

from app.common.enums import Tag
from app.common.exceptions import EntityNotFoundException, ActionForbiddenException, EntityNotAssociatedException
from app.common.responses import common_responses_dict
from app.core.logger import get_logger
from app.db_models import User
from app.schemas import GoalCreate, GoalUpdate, GoalOut, GoalFilters, ErrorResponse
from app.services import GoalService, get_goal_service
from app.services.security import get_current_user


logger = get_logger(__name__)

router = APIRouter(prefix="/goals", tags=[Tag.goal])


@router.get(
    "/{goal_id}",
    response_model=GoalOut,
    status_code=200,
    description="get one goal by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only view their own goals"}}},
        },
        404: {
            "description": "goal not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "goal with id 100 not found"}}},
        },
    },
)
async def get_goal(
    goal_id: int,
    service: GoalService = Depends(get_goal_service),
    current_user: User = Depends(get_current_user),
) -> GoalOut:
    logger.info(f"fetching goal with id {goal_id}")
    try:
        goal = await service.get_by_id(entity_id=goal_id, gotten_by=current_user)
        return goal
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "",
    response_model=list[GoalOut],
    status_code=200,
    description="get all goals with optional filters",
    responses=common_responses_dict,
)
async def get_goals(
    filters: Annotated[GoalFilters, Query()],
    service: GoalService = Depends(get_goal_service),
    current_user: User = Depends(get_current_user),
) -> list[GoalOut]:
    logger.info(f"fetching all goals with filters {filters}")
    goals = await service.get_all_with_filters(filters=filters, gotten_by=current_user)
    logger.info(f"returned {len(goals)} goals")
    return goals


@router.post(
    "",
    response_model=GoalOut,
    status_code=201,
    description="create a new goal",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only view their own goals"}}},
        },
        404: {
            "description": "type not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "type with id 100 not found"}}},
        },
        409: {
            "description": "entity not assocaited",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "entity not associated: category with id 10 is not of type with id 2"}
                }
            },
        },
    },
)
async def create_goal(
    new_goal: GoalCreate,
    service: GoalService = Depends(get_goal_service),
    current_user: User = Depends(get_current_user),
) -> GoalOut:
    logger.info("creating a new goal")
    try:
        goal = await service.create(create_schema=new_goal, created_by=current_user, user_id=current_user.id)
        return goal
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EntityNotAssociatedException as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.put(
    "/{goal_id}",
    response_model=GoalOut,
    status_code=200,
    description="update a goal by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only update their own goals"}}},
        },
        404: {
            "description": "type not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "type with id 100 not found"}}},
        },
        409: {
            "description": "entity not assocaited",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {"detail": "entity not associated: category with id 10 is not of type with id 2"}
                }
            },
        },
    },
)
async def update_goal(
    goal_id: int,
    updated_goal: GoalUpdate,
    service: GoalService = Depends(get_goal_service),
    current_user: User = Depends(get_current_user),
) -> GoalOut:
    logger.info(f"updating goal with id {goal_id}")
    try:
        goal = await service.update(entity_id=goal_id, update_schema=updated_goal, updated_by=current_user)
        return goal
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except EntityNotAssociatedException as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete(
    "/{goal_id}",
    response_model=GoalOut,
    status_code=200,
    description="delete goal by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only delete their own goals"}}},
        },
        404: {
            "description": "user not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "goal with id 100 not found"}}},
        },
    },
)
async def delete_goal(
    goal_id: int,
    service: GoalService = Depends(get_goal_service),
    current_user: User = Depends(get_current_user),
) -> GoalOut:
    logger.info(f"deleting goal with id {goal_id}")
    try:
        goal = await service.delete(entity_id=goal_id, deleted_by=current_user)
        return goal
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
