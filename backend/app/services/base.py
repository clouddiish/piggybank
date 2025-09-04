from typing import Generic, TypeVar, Any

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
    def __init__(self, session: AsyncSession, db_model_class: type[DatabaseModelT], entity_type: EntityType) -> None:
        self.session = session
        self.db_model_class = db_model_class
        self.entity_type = entity_type

    async def get_by_id(self, entity_id: int, **kwargs) -> DatabaseModelT:
        """
        Get entity by its id.

        Args:
            entity_id (int): The id of the entity to retrieve.
            kwargs: Additional arguments for getting the entity.

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

    async def get_all_with_filters(self, filters: FilterSchemaT = None, **kwargs) -> list[DatabaseModelT]:
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
                clean_filter_name = filter_name.replace("_gt", "").replace("_lt", "")
                column = getattr(self.db_model_class, clean_filter_name, None)

                if not column:
                    logger.warning(f"ignoring invalid filter: {filter_name}")
                    continue

                # list filters (IN-style filter)
                if filter_name in filters.list_filters and filter_values:
                    statement = statement.where(column.in_(filter_values))

                # greater-than filters
                elif filter_name in filters.gt_filters and filter_values is not None:
                    statement = statement.where(column >= filter_values)

                # less-than filters
                elif filter_name in filters.lt_filters and filter_values is not None:
                    statement = statement.where(column <= filter_values)

                # keyword filters (ILIKE with ORs)
                elif filter_name in filters.kw_filters and filter_values:
                    statement = statement.where(or_(*(column.ilike(f"%{kw}%") for kw in filter_values)))

        query = await self.session.execute(statement)
        entities = query.scalars().all()
        return entities

    async def _validate_create(self, create_schema: CreateSchemaT, **kwargs) -> None:
        """
        Validate create schmea.

        Args:
            schema (CreateSchemaT): The schema to validate.
            kwargs: Additional arguments for creation.

        Returns:
            None
        """
        # no validation by default, to be overwritten in child classes
        pass

    def _get_create_or_update_valid_fields(self, schema: CreateSchemaT | UpdateSchemaT, **kwargs) -> dict[str, Any]:
        """
        Extract valid fields for DatabaseModelT from schema and kwargs.

        Args:
            schema (CreateSchemaT | UpdateSchemaT): The schema from which to extract valid fields.
            kwargs: Additional arguments from which to extract valid fields.

        Returns:
            dict[str, Any]: Dictionary of valid fields.
        """
        database_model_fields = self.db_model_class.__table__.columns
        # filter out extra fields not in the DatabaseModelT
        valid_fields = {key: value for key, value in schema.model_dump().items() if key in database_model_fields}
        # add additional fields from kwargs that are in DatabaseModelT
        valid_fields.update({key: value for key, value in kwargs.items() if key in database_model_fields})
        return valid_fields

    async def create(self, create_schema: CreateSchemaT, **kwargs) -> DatabaseModelT:
        """
        Create new entity in the database.

        Args:
            create_schema (CreateSchemaT): The schema for creating the entity.
            kwargs: Additional arguments for creation.

        Returns:
            DatabaseModelT: The created entity.
        """
        logger.info(f"executing query to create a new {self.entity_type.value}")

        await self._validate_create(create_schema=create_schema, **kwargs)

        valid_fields = self._get_create_or_update_valid_fields(schema=create_schema, **kwargs)
        entity_db = self.db_model_class(**valid_fields)
        self.session.add(entity_db)
        await self.session.commit()
        return entity_db

    async def _validate_update(self, entity_id: int, update_schema: UpdateSchemaT, **kwargs) -> DatabaseModelT:
        """
        Validate create schmea.

        Args:
            entity_id (int): The id of the entity to validate.
            schema (CreateSchemaT): The schema to validate.
            kwargs: Additional arguments for update.

        Returns:
            DatabaseModelT: The validated entity.

        Raises:
            EntityNotFoundException: If the entity with the given id does not exist.
        """
        # by default only validate if entity exists
        entity_db = await self.get_by_id(entity_id=entity_id)
        return entity_db

    async def update(self, entity_id: int, update_schema: UpdateSchemaT, **kwargs) -> DatabaseModelT:
        """
        Update an existing entity in the database.

        Args:
            entity_id (int): The id of the entity to update.
            update_schema (UpdateSchemaT): The schema for updating the entity.
            kwargs: Additional arguments for update.

        Returns:
            DatabaseModelT: The updated entity.

        Raises:
            EntityNotFoundException: If the entity with the given id does not exist.
        """
        logger.info(f"executing query to update {self.entity_type.value} with id {entity_id}")

        entity_db = await self._validate_update(entity_id=entity_id, update_schema=update_schema, **kwargs)

        valid_fields = self._get_create_or_update_valid_fields(schema=update_schema, **kwargs)
        for key, value in valid_fields.items():
            setattr(entity_db, key, value)

        self.session.add(entity_db)
        await self.session.commit()
        await self.session.refresh(entity_db)
        return entity_db

    async def _validate_delete(self, entity_id: int, **kwargs) -> DatabaseModelT:
        """
        Validate deletion of an entity.

        Args:
            entity_id (int): The id of the entity to validate.

        Returns:
            DatabaseModelT: The validated entity.
            kwargs: Additional arguments for delete.

        Raises:
            EntityNotFoundException: If the entity with the given id does not exist.
        """
        # by default only validate if entity exists
        entity_db = await self.get_by_id(entity_id=entity_id)
        return entity_db

    async def delete(self, entity_id: int, **kwargs) -> DatabaseModelT:
        """
        Delete an existing entity in the database.

        Args:
            entity_id (int): The id of the entity to delete.
            kwargs: Additional arguments for delete.

        Returns:
            DatabaseModelT: The deleted entity.

        Raises:
            EntityNotFoundException: If the entity with the given id does not exist.
        """
        logger.info(f"executing query to delete {self.entity_type.value} with id {entity_id}")

        entity_db = await self._validate_delete(entity_id=entity_id, **kwargs)

        await self.session.delete(entity_db)
        await self.session.commit()
        return entity_db
