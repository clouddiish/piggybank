import pytest
from unittest.mock import AsyncMock, MagicMock

from app.common.enums import EntityType, TypeName
from app.common.exceptions import EntityNotFoundException
from app.core.config import get_settings
from app.db_models import Type
from app.schemas import TypeFilters, TypeCreate, TypeUpdate
from app.services import TypeService


settings = get_settings()


@pytest.mark.unit
class TestTypeServices:
    @pytest.mark.anyio
    async def test_get_by_id__id_exists(
        self, mock_session: AsyncMock, mock_type_service: TypeService, mock_types: list[Type]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_types[0]

        type = await mock_type_service.get_by_id(entity_id=mock_types[0].id)

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        assert type == mock_types[0]

    @pytest.mark.anyio
    async def test_get_by_id__id_does_not_exist(
        self, mock_session: AsyncMock, mock_type_service: TypeService, mock_types: list[Type]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = None

        with pytest.raises(EntityNotFoundException):
            await mock_type_service.get_by_id(entity_id=3)

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()

    @pytest.mark.anyio
    async def test_get_all_with_filters__no_filters(
        self, mock_session: AsyncMock, mock_type_service: TypeService, mock_types: list[Type]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = mock_types

        types = await mock_type_service.get_all_with_filters()

        mock_session.execute.assert_called_once()
        mock_query.scalars.return_value.all.assert_called_once()
        assert types == mock_types

    @pytest.mark.anyio
    async def test_get_all_with_filters__with_filters(
        self, mock_session: AsyncMock, mock_type_service: TypeService, mock_types: list[Type]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = [mock_types[1]]

        types = await mock_type_service.get_all_with_filters(filters=TypeFilters(name=["expense"]))

        mock_session.execute.assert_called_once()
        mock_query.scalars.return_value.all.assert_called_once()
        assert types == [mock_types[1]]

    @pytest.mark.anyio
    async def test_get_create_or_update_valid_fields__TypeCreate(self, mock_type_service: TypeService) -> None:
        type_create = TypeCreate(name=TypeName.expense)

        valid_fields = mock_type_service._get_create_or_update_valid_fields(schema=type_create)

        assert valid_fields == {"name": TypeName.expense}

    @pytest.mark.anyio
    async def test_get_create_or_update_valid_fields__TypeUpdate(self, mock_type_service: TypeService) -> None:
        type_update = TypeUpdate(name=TypeName.expense)

        valid_fields = mock_type_service._get_create_or_update_valid_fields(schema=type_update)

        assert valid_fields == {"name": TypeName.expense}

    @pytest.mark.anyio
    async def test_create__all_ok(self, mock_session: AsyncMock, mock_type_service: TypeService) -> None:
        mock_type_service._validate_create = AsyncMock()
        mock_type_service._get_create_or_update_valid_fields = MagicMock(return_value={"name": TypeName.expense})

        type_create = TypeCreate(name=TypeName.expense)
        type = await mock_type_service.create(create_schema=type_create)

        mock_type_service._validate_create.assert_called_once()
        mock_type_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        assert isinstance(type, Type)
        assert hasattr(type, "id")
        assert type.name == type_create.name

    @pytest.mark.anyio
    async def test_validate_update__all_ok(self, mock_type_service: TypeService, mock_types: list[Type]) -> None:
        mock_type_service.get_by_id = AsyncMock(return_value=mock_types[1])

        type = await mock_type_service._validate_update(entity_id=1, update_schema=TypeUpdate(name=TypeName.expense))

        mock_type_service.get_by_id.assert_called_once()
        assert type == mock_types[1]

    @pytest.mark.anyio
    async def test_validate_update__id_does_not_exist(self, mock_type_service: TypeService) -> None:
        mock_type_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=3, entity_type=EntityType.type)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_type_service._validate_update(entity_id=3, update_schema=TypeUpdate(name=TypeName.expense))

        mock_type_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_update__all_ok(
        self, mock_session: AsyncMock, mock_type_service: TypeService, mock_types: list[Type]
    ) -> None:
        mock_type_service._validate_update = AsyncMock(return_value=mock_types[1])
        mock_type_service._get_create_or_update_valid_fields = MagicMock(return_value={"name": TypeName.expense})

        type_update = TypeUpdate(name=TypeName.expense)
        type = await mock_type_service.update(entity_id=mock_types[1].id, update_schema=type_update)

        mock_type_service._validate_update.assert_called_once()
        mock_type_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert type.id == mock_types[1].id
        assert type.name == type_update.name

    @pytest.mark.anyio
    async def test_update__id_does_not_exist(self, mock_session: AsyncMock, mock_type_service: TypeService) -> None:
        mock_type_service._validate_update = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=3, entity_type=EntityType.type)
        )
        mock_type_service._get_create_or_update_valid_fields = MagicMock(return_value={"name": TypeName.expense})

        type_update = TypeUpdate(name=TypeName.expense)
        with pytest.raises(EntityNotFoundException):
            await mock_type_service.update(entity_id=3, update_schema=type_update)

        mock_type_service._validate_update.assert_called_once()
        mock_type_service._get_create_or_update_valid_fields.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called

    @pytest.mark.anyio
    async def test_validate_delete__all_ok(self, mock_type_service: TypeService, mock_types: list[Type]) -> None:
        mock_type_service.get_by_id = AsyncMock(return_value=mock_types[1])

        type = await mock_type_service._validate_delete(entity_id=1)

        mock_type_service.get_by_id.assert_called_once()
        assert type == mock_types[1]

    @pytest.mark.anyio
    async def test_validate_delete__id_not_found(self, mock_type_service: TypeService, mock_types: list[Type]) -> None:
        mock_type_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.type)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_type_service._validate_delete(entity_id=100)

        mock_type_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_delete__all_ok(
        self, mock_session: AsyncMock, mock_type_service: TypeService, mock_types: list[Type]
    ) -> None:
        mock_type_service._validate_delete = AsyncMock(return_value=mock_types[1])

        type = await mock_type_service.delete(entity_id=mock_types[1].id)

        mock_type_service._validate_delete.assert_called_once()
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()
        assert type == mock_types[1]

    @pytest.mark.anyio
    async def test_delete__id_does_not_exist(self, mock_session: AsyncMock, mock_type_service: TypeService) -> None:
        mock_type_service._validate_delete = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=3, entity_type=EntityType.type)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_type_service.delete(entity_id=3)

        mock_type_service._validate_delete.assert_called_once()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
