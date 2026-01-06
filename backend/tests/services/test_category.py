from unittest.mock import AsyncMock, MagicMock

import pytest

from app.common.enums import EntityType
from app.common.exceptions import EntityNotFoundException, ActionForbiddenException
from app.core.config import get_settings
from app.db_models import Category, Type, User
from app.schemas import CategoryFilters, CategoryCreate, CategoryUpdate
from app.services import CategoryService


settings = get_settings()


@pytest.mark.unit
class TestCategoryServices:
    @pytest.mark.anyio
    async def test_get_by_id__all_ok_same_user(
        self,
        mock_session: AsyncMock,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_categories[0]
        mock_category_service.user_service.is_admin = AsyncMock(return_value=False)

        category = await mock_category_service.get_by_id(entity_id=mock_categories[0].id, gotten_by=mock_users[0])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_category_service.user_service.is_admin.assert_not_called()
        assert category == mock_categories[0]

    @pytest.mark.anyio
    async def test_get_by_id__all_ok_admin(
        self,
        mock_session: AsyncMock,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_categories[0]
        mock_category_service.user_service.is_admin = AsyncMock(return_value=True)

        category = await mock_category_service.get_by_id(entity_id=mock_categories[0].id, gotten_by=mock_users[1])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_category_service.user_service.is_admin.assert_called_once()
        assert category == mock_categories[0]

    @pytest.mark.anyio
    async def test_get_by_id__id_does_not_exist(
        self, mock_session: AsyncMock, mock_category_service: CategoryService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = None

        with pytest.raises(EntityNotFoundException):
            await mock_category_service.get_by_id(entity_id=3, gotten_by=mock_users[0])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id__different_user(
        self,
        mock_session: AsyncMock,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_categories[0]
        mock_category_service.user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_category_service.get_by_id(entity_id=mock_categories[0].id, gotten_by=mock_users[1])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_category_service.user_service.is_admin.assert_called_once()

    @pytest.mark.anyio
    async def test_get_all_with_filters__no_filters_admin(
        self,
        mock_session: AsyncMock,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = mock_categories
        mock_category_service.user_service.is_admin = AsyncMock(return_value=True)

        categories = await mock_category_service.get_all_with_filters(gotten_by=mock_users[0])

        mock_category_service.user_service.is_admin.assert_called_once()
        mock_session.execute.assert_called_once()
        mock_query.scalars.return_value.all.assert_called_once()
        assert categories == mock_categories

    @pytest.mark.anyio
    async def test_get_all_with_filters__with_filters(
        self,
        mock_session: AsyncMock,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = [mock_categories[1]]
        mock_category_service.user_service.is_admin = AsyncMock(return_value=False)

        categories = await mock_category_service.get_all_with_filters(
            filters=CategoryFilters(name=["groceries"]), gotten_by=mock_users[1]
        )

        mock_category_service.user_service.is_admin.assert_called_once()
        mock_session.execute.assert_called_once()
        mock_query.scalars.return_value.all.assert_called_once()
        assert categories == [mock_categories[1]]

    @pytest.mark.anyio
    async def test_validate_create__all_ok(
        self, mock_category_service: CategoryService, mock_types: list[Type]
    ) -> None:
        category_create = CategoryCreate(type_id=1, name="test category")
        mock_category_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        await mock_category_service._validate_create(create_schema=category_create)

        mock_category_service.type_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_validate_create__type_does_not_exist(self, mock_category_service: CategoryService) -> None:
        category_create = CategoryCreate(type_id=100, name="test category")
        mock_category_service.type_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.type)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_category_service._validate_create(create_schema=category_create)

        mock_category_service.type_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_get_create_or_update_valid_fields__CategoryCreate(
        self, mock_category_service: CategoryService
    ) -> None:
        category_create = CategoryCreate(type_id=1, name="test category")

        valid_fields = mock_category_service._get_create_or_update_valid_fields(schema=category_create)

        assert valid_fields == {"type_id": 1, "name": "test category"}

    @pytest.mark.anyio
    async def test_get_create_or_update_valid_fields__CategoryUpdate(
        self, mock_category_service: CategoryService
    ) -> None:
        category_update = CategoryUpdate(type_id=1, name="test category")

        valid_fields = mock_category_service._get_create_or_update_valid_fields(schema=category_update)

        assert valid_fields == {"type_id": 1, "name": "test category"}

    @pytest.mark.anyio
    async def test_create__all_ok(self, mock_session: AsyncMock, mock_category_service: CategoryService) -> None:
        mock_category_service._validate_create = AsyncMock()
        mock_category_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"type_id": 1, "name": "test category", "user_id": 1}
        )

        category_create = CategoryCreate(type_id=1, name="test category")
        category = await mock_category_service.create(create_schema=category_create)

        mock_category_service._validate_create.assert_called_once()
        mock_category_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        assert isinstance(category, Category)
        assert hasattr(category, "id")
        assert category.type_id == 1
        assert category.name == category_create.name
        assert category.user_id == 1

    @pytest.mark.anyio
    async def test_validate_update__all_ok_same_user(
        self,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
        mock_types: list[Type],
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(return_value=mock_categories[1])
        mock_category_service.user_service.is_admin = AsyncMock(return_value=False)
        mock_category_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        category = await mock_category_service._validate_update(
            entity_id=1, update_schema=CategoryUpdate(type_id=1, name="test category"), updated_by=mock_users[0]
        )

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_not_called()
        mock_category_service.type_service.get_by_id.assert_called_once()
        assert category == mock_categories[1]

    @pytest.mark.anyio
    async def test_validate_update__all_ok_admin(
        self,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
        mock_types: list[Type],
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(return_value=mock_categories[1])
        mock_category_service.user_service.is_admin = AsyncMock(return_value=True)
        mock_category_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        category = await mock_category_service._validate_update(
            entity_id=1, update_schema=CategoryUpdate(type_id=1, name="test category"), updated_by=mock_users[1]
        )

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_called_once()
        mock_category_service.type_service.get_by_id.assert_called_once()
        assert category == mock_categories[1]

    @pytest.mark.anyio
    async def test_validate_update__category_does_not_exist(
        self, mock_category_service: CategoryService, mock_users: list[User], mock_types: list[Type]
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.category)
        )
        mock_category_service.user_service.is_admin = AsyncMock(return_value=True)
        mock_category_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        with pytest.raises(EntityNotFoundException):
            await mock_category_service._validate_update(
                entity_id=100, update_schema=CategoryUpdate(type_id=1, name="test category"), updated_by=mock_users[1]
            )

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_not_called()
        mock_category_service.type_service.get_by_id.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_update__different_user(
        self,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
        mock_types: list[Type],
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(return_value=mock_categories[1])
        mock_category_service.user_service.is_admin = AsyncMock(return_value=False)
        mock_category_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        with pytest.raises(ActionForbiddenException):
            await mock_category_service._validate_update(
                entity_id=1, update_schema=CategoryUpdate(type_id=1, name="test category"), updated_by=mock_users[1]
            )

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_called_once()
        mock_category_service.type_service.get_by_id.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_update__type_does_not_exist(
        self,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
        mock_types: list[Type],
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(return_value=mock_categories[1])
        mock_category_service.user_service.is_admin = AsyncMock(return_value=True)
        mock_category_service.type_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.type)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_category_service._validate_update(
                entity_id=1, update_schema=CategoryUpdate(type_id=1, name="test category"), updated_by=mock_users[1]
            )

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_called_once()
        mock_category_service.type_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_update__all_ok(
        self,
        mock_session: AsyncMock,
        mock_category_service: CategoryService,
        mock_categories: list[Category],
        mock_users: list[User],
    ) -> None:
        mock_category_service._validate_update = AsyncMock(return_value=mock_categories[1])
        mock_category_service._get_create_or_update_valid_fields = MagicMock(
            return_value={"type_id": 1, "name": "test category", "user_id": 1}
        )

        category_update = CategoryUpdate(type_id=1, name="test category")
        category = await mock_category_service.update(
            entity_id=mock_categories[1].id, update_schema=category_update, updated_by=mock_users[0]
        )

        mock_category_service._validate_update.assert_called_once()
        mock_category_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert category.id == mock_categories[1].id
        assert category.name == category_update.name
        assert category.type_id == category_update.type_id

    @pytest.mark.anyio
    async def test_validate_delete__all_ok_same_user(
        self, mock_category_service: CategoryService, mock_categories: list[Category], mock_users: list[User]
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(return_value=mock_categories[1])
        mock_category_service.user_service.is_admin = AsyncMock(return_value=False)

        category = await mock_category_service._validate_delete(entity_id=1, deleted_by=mock_users[0])

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_not_called()
        assert category == mock_categories[1]

    @pytest.mark.anyio
    async def test_validate_delete__all_ok_admin(
        self, mock_category_service: CategoryService, mock_categories: list[Category], mock_users: list[User]
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(return_value=mock_categories[1])
        mock_category_service.user_service.is_admin = AsyncMock(return_value=True)

        category = await mock_category_service._validate_delete(entity_id=1, deleted_by=mock_users[1])

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_called_once()
        assert category == mock_categories[1]

    @pytest.mark.anyio
    async def test_validate_delete__id_not_found(
        self, mock_category_service: CategoryService, mock_users: list[User]
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.category)
        )
        mock_category_service.user_service.is_admin = AsyncMock(return_value=True)

        with pytest.raises(EntityNotFoundException):
            await mock_category_service._validate_delete(entity_id=100, deleted_by=mock_users[0])

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_not_called()

    @pytest.mark.anyio
    async def test_validate_delete__different_user(
        self, mock_category_service: CategoryService, mock_categories: list[Category], mock_users: list[User]
    ) -> None:
        mock_category_service.get_by_id = AsyncMock(return_value=mock_categories[1])
        mock_category_service.user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_category_service._validate_delete(entity_id=1, deleted_by=mock_users[1])

        mock_category_service.get_by_id.assert_called_once()
        mock_category_service.user_service.is_admin.assert_called_once()

    @pytest.mark.anyio
    async def test_delete__all_ok(
        self, mock_session: AsyncMock, mock_category_service: CategoryService, mock_categories: list[Category]
    ) -> None:
        mock_category_service._validate_delete = AsyncMock(return_value=mock_categories[1])

        category = await mock_category_service.delete(entity_id=mock_categories[1].id)

        mock_category_service._validate_delete.assert_called_once()
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()
        assert category == mock_categories[1]
