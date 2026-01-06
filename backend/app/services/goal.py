from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.common.exceptions import ActionForbiddenException, EntityNotAssociatedException
from app.core.session import get_session
from app.core.logger import get_logger
from app.db_models import Goal, User
from app.schemas import GoalCreate, GoalUpdate, GoalFilters
from app.services.base import BaseService
from app.services.category import get_category_service, CategoryService
from app.services.type import get_type_service, TypeService
from app.services.user import get_user_service, UserService


logger = get_logger(__name__)


class GoalService(BaseService[Goal, GoalCreate, GoalUpdate, GoalFilters]):
    def __init__(
        self,
        session: AsyncSession,
        category_service: CategoryService,
        type_service: TypeService,
        user_service: UserService,
    ) -> None:
        self.category_service = category_service
        self.type_service = type_service
        self.user_service = user_service
        super().__init__(session=session, db_model_class=Goal, entity_type=EntityType.goal)

    async def get_by_id(self, entity_id: int, gotten_by: User) -> Goal:
        # get the goal if exists
        goal_db = await super().get_by_id(entity_id=entity_id)

        # verify if they can get
        if not (gotten_by.id == goal_db.user_id or await self.user_service.is_admin(user_id=gotten_by.id)):
            raise ActionForbiddenException(detail="users can only view their own goals")

        return goal_db

    async def get_all_with_filters(self, filters: GoalFilters = None, gotten_by: User = None) -> list[Goal]:
        if not await self.user_service.is_admin(user_id=gotten_by.id):
            # if user is not an admin, always add filters to filter for only their own goals
            filters.user_id = [gotten_by.id]
        return await super().get_all_with_filters(filters=filters)

    async def _validate_create(self, create_schema: GoalCreate, created_by: User, **kwargs) -> None:
        # verify type exists
        type_db = await self.type_service.get_by_id(entity_id=create_schema.type_id)

        # if provided, verify category exists and belongs to the type
        if create_schema.category_id:
            category_db = await self.category_service.get_by_id(
                entity_id=create_schema.category_id, gotten_by=created_by
            )
            if category_db.type_id != type_db.id:
                raise EntityNotAssociatedException(
                    detail=f"category with id {category_db.id} is not of type with id {type_db.id}"
                )

    async def _validate_update(self, entity_id: int, update_schema: GoalUpdate, updated_by: User, **kwargs) -> Goal:
        # verify goal exists
        goal_db = await self.get_by_id(entity_id=entity_id, gotten_by=updated_by)

        # verify if they can update
        if not (updated_by.id == goal_db.user_id or await self.user_service.is_admin(user_id=updated_by.id)):
            raise ActionForbiddenException(detail="users can only update their own goals")

        # verify type exists
        type_db = await self.type_service.get_by_id(entity_id=update_schema.type_id)

        # if provided, verify category exists and belongs to the type
        if update_schema.category_id:
            category_db = await self.category_service.get_by_id(
                entity_id=update_schema.category_id, gotten_by=updated_by
            )
            if category_db.type_id != type_db.id:
                raise EntityNotAssociatedException(
                    detail=f"category with id {category_db.id} is not of type with id {type_db.id}"
                )

        return goal_db

    async def _validate_delete(self, entity_id: int, deleted_by: User) -> Goal:
        # verify goal exists
        goal_db = await self.get_by_id(entity_id=entity_id, gotten_by=deleted_by)

        # verify they can delete
        if not (deleted_by.id == goal_db.user_id or await self.user_service.is_admin(user_id=deleted_by.id)):
            raise ActionForbiddenException(detail="users can only delete their own goals")

        return goal_db


def get_goal_service(
    session: AsyncSession = Depends(get_session),
    category_service: CategoryService = Depends(get_category_service),
    type_service: TypeService = Depends(get_type_service),
    user_service: UserService = Depends(get_user_service),
) -> GoalService:
    return GoalService(
        session=session,
        category_service=category_service,
        type_service=type_service,
        user_service=user_service,
    )
