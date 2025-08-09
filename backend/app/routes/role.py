from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query

from app.common.enums import Tag
from app.common.exceptions import EntityNotFoundException
from app.core.logger import get_logger
from app.schemas import RoleOut, RoleFilters
from app.services import RoleService, get_role_service
from app.services.security import get_current_admin


logger = get_logger(__name__)

router = APIRouter(prefix="/roles", tags=[Tag.role], dependencies=[Depends(get_current_admin)])


@router.get("/{role_id}", response_model=RoleOut, status_code=200, summary="get one role by its id")
async def get_role(role_id: int, service: RoleService = Depends(get_role_service)) -> RoleOut:
    logger.info(f"fetching role with id {role_id}")
    try:
        role = await service.get_by_id(entity_id=role_id)
        return role
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[RoleOut], status_code=200, summary="get all roles with optional filters")
async def get_roles(
    filters: Annotated[RoleFilters, Query()], service: RoleService = Depends(get_role_service)
) -> list[RoleOut]:
    logger.info(f"fetching all roles with filters {filters}")
    roles = await service.get_all_with_filters(filters=filters)
    logger.info(f"returned {len(roles)} roles")
    return roles
