from fastapi import Depends
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import EntityType
from app.common.exceptions import ActionForbiddenException, EntityNotAssociatedException
from app.core.session import get_session
from app.core.logger import get_logger
from app.db_models import Transaction, User
from app.schemas import TransactionCreate, TransactionUpdate, TransactionFilters
from app.services.base import BaseService
from app.services.category import get_category_service, CategoryService
from app.services.type import get_type_service, TypeService
from app.services.user import get_user_service, UserService


logger = get_logger(__name__)


class TransactionService(BaseService[Transaction, TransactionCreate, TransactionUpdate, TransactionFilters]):
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
        super().__init__(session=session, db_model_class=Transaction, entity_type=EntityType.transaction)

    async def get_by_id(self, entity_id: int, gotten_by: User) -> Transaction:
        # get the transaction if exists
        transaction_db = await super().get_by_id(entity_id=entity_id)

        # verify if they can get
        if not (gotten_by.id == transaction_db.user_id or await self.user_service.is_admin(user_id=gotten_by.id)):
            raise ActionForbiddenException(detail="users can only view their own transactions")

        return transaction_db

    async def get_all_with_filters(
        self, filters: TransactionFilters = None, gotten_by: User = None
    ) -> list[Transaction]:
        if not await self.user_service.is_admin(user_id=gotten_by.id):
            # if user is not an admin, always add filters to filter for only their own transactions
            filters.user_id = [gotten_by.id]
        return await super().get_all_with_filters(filters=filters)

    async def get_total_with_filters(self, filters=None, gotten_by: User = None) -> float:
        if not await self.user_service.is_admin(user_id=gotten_by.id):
            # if user is not an admin, always add filters to filter for only their own transactions
            filters.user_id = [gotten_by.id]
        statement = select(func.sum(self.db_model_class.value))
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
        result = query.scalar()
        return result or 0.0

    async def _validate_create(self, create_schema: TransactionCreate, created_by: User, **kwargs) -> None:
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

    async def _validate_update(
        self, entity_id: int, update_schema: TransactionUpdate, updated_by: User, **kwargs
    ) -> Transaction:
        # verify transaction exists
        transaction_db = await self.get_by_id(entity_id=entity_id, gotten_by=updated_by)

        # verify if they can update
        if not (updated_by.id == transaction_db.user_id or await self.user_service.is_admin(user_id=updated_by.id)):
            raise ActionForbiddenException(detail="users can only update their own transactions")

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

        return transaction_db

    async def _validate_delete(self, entity_id: int, deleted_by: User) -> Transaction:
        # verify transaction exists
        transaction_db = await self.get_by_id(entity_id=entity_id, gotten_by=deleted_by)

        # verify they can delete
        if not (deleted_by.id == transaction_db.user_id or await self.user_service.is_admin(user_id=deleted_by.id)):
            raise ActionForbiddenException(detail="users can only delete their own transactions")

        return transaction_db


def get_transaction_service(
    session: AsyncSession = Depends(get_session),
    category_service: CategoryService = Depends(get_category_service),
    type_service: TypeService = Depends(get_type_service),
    user_service: UserService = Depends(get_user_service),
) -> TransactionService:
    return TransactionService(
        session=session,
        category_service=category_service,
        type_service=type_service,
        user_service=user_service,
    )
