from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.common.exceptions import ActionForbiddenException
from app.core.session import get_session
from app.core.logger import get_logger
from app.db_models import Category, User
from app.schemas import CategoryCreate, CategoryUpdate, CategoryFilters
from app.services.base import BaseService
from app.services.type import get_type_service
from app.services.user import get_user_service


logger = get_logger(__name__)


class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate, CategoryFilters]):
    def __init__(self, session: AsyncSession) -> None:
        self.user_service = get_user_service(session=session)
        self.type_service = get_type_service(session=session)
        super().__init__(session=session, db_model_class=Category, entity_type=EntityType.category)

    async def get_by_id(self, entity_id: int, gotten_by: User) -> Category:
        """
        Get category by its id.

        Args:
            entity_id (int): The id of the category to retrieve.
            gotten_by (User): The user doing the getting.

        Returns:
            Category: The gotten category.

        Raises:
            EntityNotFoundException: If the entity with the given id does not exist.
            ActionForbiddenException: If the user doing the getting is not allowed to perform the get.
        """
        # get the category if exists
        category_db = await super().get_by_id(entity_id)

        # verify if they can get
        if not (gotten_by.id == category_db.user_id or await self.user_service.is_admin(user_id=gotten_by.id)):
            raise ActionForbiddenException(detail="users can only view their own categories")

        return category_db

    async def get_all_with_filters(self, filters: CategoryFilters = None, gotten_by: User = None):
        """
        Get all categories, matching optional filters.

        Args:
            filters (CategoryFilters): The optional filters to apply.

        Returns:
            list[Category]: A list of all categories matching provided filters.
        """
        if not await self.user_service.is_admin(user_id=gotten_by.id):
            # if user is not an admin, always add filters to filter for only their own categories
            filters.user_id = [gotten_by.id]
        return await super().get_all_with_filters(filters)

    async def _validate_create(self, create_schema: CategoryCreate, **kwargs) -> None:
        """
        Validate CategoryCreate schema.

        Args:
            schema (CategoryCreate): The schema to validate.

        Returns:
            None

        Raises:
            EntityNotFoundException: If type with provided id does not exist..
        """
        # verify type exists
        await self.type_service.get_by_id(entity_id=create_schema.type_id)

    async def _validate_update(
        self, entity_id: int, update_schema: CategoryUpdate, updated_by: User, **kwargs
    ) -> Category:
        """
        Validate CategoryUpdate schema.

        Args:
            entity_id (int): The id of the category to validate.
            schema (CategoryUpdate): The schema to validate.
            updated_by (User): The user doing the update.

        Returns:
            Category: The validated category.

        Raises:
            EntityNotFoundException: If the category or type with the given id do not exist.
            ActionForbiddenException: If the user doing the update is not allowed to perform the update.
        """
        # verify category exists
        category_db = await self.get_by_id(entity_id=entity_id, gotten_by=updated_by)

        # verify if they can update
        if not (updated_by.id == category_db.user_id or await self.user_service.is_admin(user_id=updated_by.id)):
            raise ActionForbiddenException(detail="users can only update their own categories")

        # verify type exists
        await self.type_service.get_by_id(entity_id=update_schema.type_id)

        return category_db

    async def _validate_delete(self, entity_id: int, deleted_by: User) -> Category:
        """
        Validate deletion of a category.

        Args:
            entity_id (int): The id of the category to validate.
            deleted_by (User): The user doing the delete.

        Returns:
            Category: The validated user.

        Raises:
            EntityNotFoundException: If the category with the given id does not exist.
            ActionForbiddenException: If user doing the delete is not allowed to perform the delete.
        """
        # verify category exists
        category_db = await self.get_by_id(entity_id=entity_id, gotten_by=deleted_by)

        # verify they can delete
        if not (deleted_by.id == category_db.user_id or await self.user_service.is_admin(user_id=deleted_by.id)):
            raise ActionForbiddenException(detail="users can only delete their own categories")

        return category_db


def get_category_service(session: AsyncSession = Depends(get_session)) -> CategoryService:
    return CategoryService(session)
