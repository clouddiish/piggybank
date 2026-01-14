from unittest.mock import AsyncMock, MagicMock

import pytest

from app.common.exceptions import (
    EntityNotFoundException,
    ActionForbiddenException,
    EntityNotAssociatedException,
)
from app.db_models import Transaction, Type, Category, User
from app.schemas import TransactionCreate, TransactionUpdate, TransactionFilters
from app.services import TransactionService


@pytest.mark.unit
class TestTransactionService:
    @pytest.mark.anyio
    async def test_get_by_id__all_ok_same_user(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_transactions[0]
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=False)

        transaction = await mock_transaction_service.get_by_id(
            entity_id=mock_transactions[0].id, gotten_by=mock_users[0]
        )

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_transaction_service.user_service.is_admin.assert_not_called()
        assert transaction == mock_transactions[0]

    @pytest.mark.anyio
    async def test_get_by_id__all_ok_admin(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_transactions[0]
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=True)

        transaction = await mock_transaction_service.get_by_id(
            entity_id=mock_transactions[0].id, gotten_by=mock_users[1]
        )

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_transaction_service.user_service.is_admin.assert_called_once()
        assert transaction == mock_transactions[0]

    @pytest.mark.anyio
    async def test_get_by_id__id_does_not_exist(
        self, mock_session: AsyncMock, mock_transaction_service: TransactionService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = None

        with pytest.raises(EntityNotFoundException):
            await mock_transaction_service.get_by_id(entity_id=999, gotten_by=mock_users[0])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id__different_user(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_transactions[0]
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_transaction_service.get_by_id(entity_id=mock_transactions[0].id, gotten_by=mock_users[1])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_transaction_service.user_service.is_admin.assert_called_once()

    @pytest.mark.anyio
    async def test_get_all_with_filters__admin(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = mock_transactions
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=True)

        transactions = await mock_transaction_service.get_all_with_filters(gotten_by=mock_users[1])

        mock_transaction_service.user_service.is_admin.assert_called_once()
        mock_session.execute.assert_called_once()
        assert transactions == mock_transactions

    @pytest.mark.anyio
    async def test_get_all_with_filters__non_admin_adds_user_filter(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = [mock_transactions[0]]
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=False)

        filters = TransactionFilters(type_id=[1])
        transactions = await mock_transaction_service.get_all_with_filters(filters=filters, gotten_by=mock_users[0])

        assert filters.user_id == [mock_users[0].id]
        mock_transaction_service.user_service.is_admin.assert_called_once()
        mock_session.execute.assert_called_once()
        assert transactions == [mock_transactions[0]]

    @pytest.mark.anyio
    async def test_get_total_with_filters__admin(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar.return_value = 1500.0
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=True)

        total = await mock_transaction_service.get_total_with_filters(gotten_by=mock_users[1])

        mock_transaction_service.user_service.is_admin.assert_called_once()
        mock_session.execute.assert_called_once()
        assert total == 1500.0

    @pytest.mark.anyio
    async def test_get_total_with_filters__non_admin_adds_user_filter(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar.return_value = 500.0
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=False)

        filters = TransactionFilters(type_id=[1])
        total = await mock_transaction_service.get_total_with_filters(filters=filters, gotten_by=mock_users[0])

        assert filters.user_id == [mock_users[0].id]
        mock_transaction_service.user_service.is_admin.assert_called_once()
        mock_session.execute.assert_called_once()
        assert total == 500.0

    @pytest.mark.anyio
    async def test_validate_create__all_ok(
        self, mock_transaction_service: TransactionService, mock_types: list[Type], mock_users: list[User]
    ) -> None:
        create_schema = TransactionCreate(type_id=1, category_id=None, date="2024-01-01", value=100.0)
        mock_transaction_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        await mock_transaction_service._validate_create(create_schema=create_schema, created_by=mock_users[0])

        mock_transaction_service.type_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_validate_create__category_not_associated(
        self,
        mock_transaction_service: TransactionService,
        mock_types: list[Type],
        mock_categories: list[Category],
        mock_users: list[User],
    ) -> None:
        create_schema = TransactionCreate(type_id=1, category_id=2, date="2024-01-01", value=100.0)
        mock_transaction_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])
        mock_transaction_service.category_service.get_by_id = AsyncMock(
            return_value=mock_categories[1]
        )  # mismatched type

        with pytest.raises(EntityNotAssociatedException):
            await mock_transaction_service._validate_create(create_schema=create_schema, created_by=mock_users[0])

    @pytest.mark.anyio
    async def test_validate_update__all_ok_admin(
        self,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_types: list[Type],
        mock_users: list[User],
    ) -> None:
        mock_transaction_service.get_by_id = AsyncMock(return_value=mock_transactions[0])
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=True)
        mock_transaction_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        transaction = await mock_transaction_service._validate_update(
            entity_id=1,
            update_schema=TransactionUpdate(type_id=1, date="2024-01-01", value=50.0),
            updated_by=mock_users[1],
        )

        assert transaction == mock_transactions[0]

    @pytest.mark.anyio
    async def test_validate_update__different_user_forbidden(
        self,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
        mock_types: list[Type],
    ) -> None:
        mock_transaction_service.get_by_id = AsyncMock(return_value=mock_transactions[0])
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_transaction_service._validate_update(
                entity_id=1,
                update_schema=TransactionUpdate(type_id=1, date="2024-01-01", value=50.0),
                updated_by=mock_users[1],
            )

    @pytest.mark.anyio
    async def test_validate_delete__all_ok_admin(
        self, mock_transaction_service: TransactionService, mock_transactions: list[Transaction], mock_users: list[User]
    ) -> None:
        mock_transaction_service.get_by_id = AsyncMock(return_value=mock_transactions[0])
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=True)

        transaction = await mock_transaction_service._validate_delete(entity_id=1, deleted_by=mock_users[1])

        assert transaction == mock_transactions[0]

    @pytest.mark.anyio
    async def test_validate_delete__different_user_forbidden(
        self, mock_transaction_service: TransactionService, mock_transactions: list[Transaction], mock_users: list[User]
    ) -> None:
        mock_transaction_service.get_by_id = AsyncMock(return_value=mock_transactions[0])
        mock_transaction_service.user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_transaction_service._validate_delete(entity_id=1, deleted_by=mock_users[1])

    @pytest.mark.anyio
    async def test_create__all_ok(self, mock_session: AsyncMock, mock_transaction_service: TransactionService) -> None:
        mock_transaction_service._validate_create = AsyncMock()
        mock_transaction_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"type_id": 1, "date": "2024-01-01", "value": 200.0, "user_id": 1}
        )

        create_schema = TransactionCreate(type_id=1, date="2024-01-01", value=200.0)
        transaction = await mock_transaction_service.create(create_schema=create_schema)

        mock_transaction_service._validate_create.assert_called_once()
        mock_transaction_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        assert isinstance(transaction, Transaction)
        assert transaction.type_id == 1
        assert transaction.value == 200.0
        assert transaction.user_id == 1

    @pytest.mark.anyio
    async def test_update__all_ok(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
        mock_users: list[User],
    ) -> None:
        mock_transaction_service._validate_update = AsyncMock(return_value=mock_transactions[0])
        mock_transaction_service._get_create_or_update_valid_fields = MagicMock(return_value={"value": 300.0})

        update_schema = TransactionUpdate(type_id=1, date="2024-01-01", value=300.0)
        transaction = await mock_transaction_service.update(
            entity_id=1, update_schema=update_schema, updated_by=mock_users[0]
        )

        mock_transaction_service._validate_update.assert_called_once()
        mock_transaction_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert transaction.value == 300.0

    @pytest.mark.anyio
    async def test_delete__all_ok(
        self,
        mock_session: AsyncMock,
        mock_transaction_service: TransactionService,
        mock_transactions: list[Transaction],
    ) -> None:
        mock_transaction_service._validate_delete = AsyncMock(return_value=mock_transactions[0])

        transaction = await mock_transaction_service.delete(entity_id=mock_transactions[0].id)

        mock_transaction_service._validate_delete.assert_called_once()
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()
        assert transaction == mock_transactions[0]
