from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query

from app.common.enums import Tag
from app.common.exceptions import EntityNotFoundException
from app.common.responses import common_responses_dict
from app.core.logger import get_logger
from app.schemas import TypeOut, TypeFilters, ErrorResponse
from app.services import TypeService, get_type_service
from app.services.security import get_current_user


logger = get_logger(__name__)

router = APIRouter(prefix="/types", tags=[Tag.type], dependencies=[Depends(get_current_user)])


@router.get(
    "/{type_id}",
    response_model=TypeOut,
    status_code=200,
    description="get one type by its id",
    responses={
        **common_responses_dict,
        404: {
            "description": "type not found",
            "model": ErrorResponse,
            "content": {"application/json": {"example": {"detail": "type with id 100 not found"}}},
        },
    },
)
async def get_type(type_id: int, service: TypeService = Depends(get_type_service)) -> TypeOut:
    logger.info(f"fetching type with id {type_id}")
    try:
        type = await service.get_by_id(entity_id=type_id)
        return type
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "",
    response_model=list[TypeOut],
    status_code=200,
    description="get all types with optional filters",
    responses=common_responses_dict,
)
async def get_types(
    filters: Annotated[TypeFilters, Query()], service: TypeService = Depends(get_type_service)
) -> list[TypeOut]:
    logger.info(f"fetching all types with filters {filters}")
    types = await service.get_all_with_filters(filters=filters)
    logger.info(f"returned {len(types)} types")
    return types
