from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType, TypeName
from app.common.exceptions import EntityNotFoundException
from app.core.logger import get_logger
from app.core.session import get_session
from app.db_models import Type
from app.schemas import TypeCreate, TypeUpdate, TypeFilters
from app.services import BaseService


logger = get_logger(__name__)


class TypeService(BaseService[Type, TypeCreate, TypeUpdate, TypeFilters]):
    # has available all the methods from BaseService, but only gets are exposed in routes
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, db_model_class=Type, entity_type=EntityType.type)

    async def get_by_name(self, type_name: TypeName) -> Type:
        """
        Get type by name.

        Args:
            type_name (TypeName): The name of the type to retrieve.

        Returns:
            Type: The selected type.

        Raises:
            EntityNotFoundException: If the type with given name was not found.
        """
        logger.info(f"executing query to fetch type with name {type_name.value}")

        query = await self.session.execute(select(Type).where(Type.name == type_name))
        type = query.scalar_one_or_none()

        if not type:
            logger.error(f"type with name {type_name.value} not found")
            raise EntityNotFoundException(entity_id=type_name, entity_type=EntityType.type)

        return type


def get_type_service(session: AsyncSession = Depends(get_session)) -> TypeService:
    return TypeService(session)
