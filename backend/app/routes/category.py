from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query

from app.common.enums import Tag
from app.common.exceptions import EntityNotFoundException, ActionForbiddenException
from app.common.responses import common_responses_dict
from app.core.logger import get_logger
from app.db_models import User
from app.schemas import CategoryCreate, CategoryUpdate, CategoryOut, CategoryFilters, ErrorResponse
from app.services import CategoryService, get_category_service
from app.services.security import get_current_user


logger = get_logger(__name__)

router = APIRouter(prefix="/categories", tags=[Tag.category])


@router.get(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=200,
    description="get one category by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only view their own categories"}}},
        },
        404: {
            "description": "category not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "category with id 100 not found"}}},
        },
    },
)
async def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
) -> CategoryOut:
    logger.info(f"fetching category with id {category_id}")
    try:
        category = await service.get_by_id(entity_id=category_id, gotten_by=current_user)
        return category
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "",
    response_model=list[CategoryOut],
    status_code=200,
    description="get all categories with optional filters",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users is not an admin"}}},
        },
    },
)
async def get_categories(
    filters: Annotated[CategoryFilters, Query()],
    service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
) -> list[CategoryOut]:
    logger.info(f"fetching all categories with filters {filters}")
    categories = await service.get_all_with_filters(filters=filters, gotten_by=current_user)
    logger.info(f"returned {len(categories)} categories")
    return categories


@router.post(
    "",
    response_model=CategoryOut,
    status_code=201,
    description="create a new category",
    responses={
        **common_responses_dict,
        404: {
            "description": "type not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "type with id 100 not found"}}},
        },
    },
)
async def create_category(
    new_category: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
) -> CategoryOut:
    logger.info("creating a new category")
    try:
        category = await service.create(create_schema=new_category, user_id=current_user.id)
        return category
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=200,
    description="update a category by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only update their own categories"}}},
        },
    },
)
async def update_category(
    category_id: int,
    updated_category: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
) -> CategoryOut:
    logger.info(f"updating category with id {category_id}")
    try:
        category = await service.update(entity_id=category_id, update_schema=updated_category, updated_by=current_user)
        return category
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=200,
    description="delete category by its id",
    responses={
        **common_responses_dict,
        403: {
            "description": "action forbidden",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "users can only delete their own categories"}}},
        },
        404: {
            "description": "user not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "category with id 100 not found"}}},
        },
    },
)
async def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
) -> CategoryOut:
    logger.info(f"deleting category with id {category_id}")
    try:
        category = await service.delete(entity_id=category_id, deleted_by=current_user)
        return category
    except ActionForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
