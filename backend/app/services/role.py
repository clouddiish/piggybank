from fastapi import Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.core.session import get_session
from app.db_models import Role
from app.schemas import RoleFilters


class RoleService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_roles(self, filters: RoleFilters = []) -> list[Role]:
        logger.info("executing query to fetch roles")
        statement = select(Role)

        if filters:
            for filter_name, filter_values in filters:
                column = getattr(Role, filter_name, None)
                if not column:
                    logger.warning(f"ignoring invalid filter: {filter_name}")
                    continue
                if filter_values:
                    statement = statement.where(or_(*(column == val for val in filter_values)))

        result = await self.session.execute(statement)
        roles = result.scalars().all()
        return roles


def get_role_service(session: AsyncSession = Depends(get_session)) -> RoleService:
    return RoleService(session)
