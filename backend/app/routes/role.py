from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import Tag
from app.core.logger import logger
from app.schemas import RoleCreate, RoleUpdate, RoleOut, RoleFilters
from app.services.role import RoleService, get_role_service


router = APIRouter(prefix="/roles", tags=[Tag.role])


@router.get("", response_model=list[RoleOut], status_code=200, summary="get all roles with optional filters")
async def get_roles(filters: Annotated[RoleFilters, Query()], service: RoleService = Depends(get_role_service)):
    logger.info("fetching all roles")
    roles = await service.get_roles(filters=filters)
    logger.info(f"returned {len(roles)} roles")
    return roles
