from typing import Generic, TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.common.exceptions import EntityNotFoundException
from app.core.logger import get_logger


DatabaseModelT = TypeVar("DatabaseModelT")
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)
FilterSchemaT = TypeVar("FilterSchemaT", bound=BaseModel)


logger = get_logger(__name__)


class BaseService(Generic[DatabaseModelT, CreateSchemaT, UpdateSchemaT, FilterSchemaT]):
    def __init__(self, session: AsyncSession, db_model_class: Type[DatabaseModelT], entity_type: EntityType) -> None:
        self.session = session
        self.db_model_class = db_model_class
        self.entity_type = entity_type

    async def get_by_id(self, entity_id: int) -> DatabaseModelT:
        """
        Get entity by its id.

        Args:
            entity_id (int): The id of the entity to retrieve.

        Returns:
            DatabaseModelT: The database model instance.

        Raises:
            EntityNotFoundException: If the entity with the given id does not exist.
        """
        logger.info(f"executing query to fetch {self.entity_type.value} with id {entity_id}")

        query = await self.session.execute(select(self.db_model_class).where(self.db_model_class.id == entity_id))
        entity = query.scalar_one_or_none()

        if not entity:
            logger.error(f"{self.entity_type.value} with id {entity_id} not found")
            raise EntityNotFoundException(entity_id=entity_id, entity_type=self.entity_type)

        return entity

    async def get_all_with_filters(self, filters: FilterSchemaT = None) -> list[DatabaseModelT]:
        """
        Get all entities of specified type, matching optional filters.

        Args:
            filters (FilterSchemaT): The optional filters to apply.

        Returns:
            list[DatabaseModelT]: A list of all entities matching provided filters.
        """
        logger.info(f"executing query to fetch all {self.entity_type.value} with filters {filters}")

        statement = select(self.db_model_class)

        if filters:
            for filter_name, filter_values in filters:
                column = getattr(self.db_model_class, filter_name, None)
                if not column:
                    logger.warning(f"ignoring invalid filter: {filter_name}")
                    continue
                if filter_values:
                    statement = statement.where(or_(*(column == val for val in filter_values)))

        query = await self.session.execute(statement)
        entities = query.scalars().all()
        return entities

    async def create(self, create_schema: CreateSchemaT) -> DatabaseModelT:
        """
        Create new entity in the database.

        Args:
            create_schema (CreateSchemaT): The schema for creating the entity.

        Returns:
            DatabaseModelT: The created entity.
        """
        logger.info(f"executing query to create a new {self.entity_type.value}")

        entity_db = self.db_model_class(**create_schema.model_dump())
        self.session.add(entity_db)
        await self.session.commit()
        return entity_db

    async def update(self, entity_id: int, update_schema: UpdateSchemaT) -> DatabaseModelT:
        """
        Update an existing entity in the database.

        Args:
            entity_id (int): The id of the entity to update.
            update_schema (UpdateSchemaT): The schema for updating the entity.

        Returns:
            DatabaseModelT: The updated entity.

        Raises:
            EntityNotFoundException: If the entity with the given id does not exist.
        """
        logger.info(f"executing query to update {self.entity_type.value} with id {entity_id}")

        entity_db = await self.get_by_id(entity_id=entity_id)

        for key, value in update_schema.model_dump().items():
            setattr(entity_db, key, value)

        self.session.add(entity_db)
        await self.session.commit()
        await self.session.refresh(entity_db)
        return entity_db

    async def delete(self, entity_id: int) -> DatabaseModelT:
        """
        Delete an existing entity in the database.

        Args:
            entity_id (int): The id of the entity to delete.

        Returns:
            DatabaseModelT: The deleted entity.

        Raises:
            EntityNotFoundException: If the entity with the given id does not exist.
        """
        logger.info(f"executing query to delete {self.entity_type.value} with id {entity_id}")

        entity_db = await self.get_by_id(entity_id=entity_id)
        await self.session.delete(entity_db)
        await self.session.commit()
        return entity_db
