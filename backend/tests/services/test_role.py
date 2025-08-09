import pytest
from unittest.mock import AsyncMock, MagicMock

from app.common.enums import EntityType, RoleName
from app.common.exceptions import EntityNotFoundException
from app.core.config import get_settings
from app.db_models import Role
from app.schemas import RoleFilters, RoleCreate, RoleUpdate
from app.services import RoleService


settings = get_settings()


@pytest.fixture
def mock_role_service(mock_session: AsyncMock) -> RoleService:
    return RoleService(session=mock_session)


@pytest.fixture
def mock_roles() -> list[Role]:
    return [Role(id=i, name=role_name) for i, role_name in enumerate(RoleName)]


@pytest.mark.unit
class TestRoleServices:
    @pytest.mark.anyio
    async def test_get_by_id__id_exists(
        self, mock_session: AsyncMock, mock_role_service: RoleService, mock_roles: list[Role]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_roles[0]

        role = await mock_role_service.get_by_id(entity_id=mock_roles[0].id)

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        assert role == mock_roles[0]

    @pytest.mark.anyio
    async def test_get_by_id__id_does_not_exist(
        self, mock_session: AsyncMock, mock_role_service: RoleService, mock_roles: list[Role]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = None

        with pytest.raises(EntityNotFoundException):
            await mock_role_service.get_by_id(entity_id=3)

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()

    @pytest.mark.anyio
    async def test_get_all_with_filters__no_filters(
        self, mock_session: AsyncMock, mock_role_service: RoleService, mock_roles: list[Role]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = mock_roles

        roles = await mock_role_service.get_all_with_filters()

        mock_session.execute.assert_called_once()
        mock_query.scalars.return_value.all.assert_called_once()
        assert roles == mock_roles

    @pytest.mark.anyio
    async def test_get_all_with_filters__with_filters(
        self, mock_session: AsyncMock, mock_role_service: RoleService, mock_roles: list[Role]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = [mock_roles[1]]

        roles = await mock_role_service.get_all_with_filters(filters=RoleFilters(name=["user"]))

        mock_session.execute.assert_called_once()
        mock_query.scalars.return_value.all.assert_called_once()
        assert roles == [mock_roles[1]]

    @pytest.mark.anyio
    async def test_get_create_or_update_valid_fields__RoleCreate(self, mock_role_service: RoleService) -> None:
        role_create = RoleCreate(name=RoleName.user)

        valid_fields = mock_role_service._get_create_or_update_valid_fields(schema=role_create)

        assert valid_fields == {"name": RoleName.user}

    @pytest.mark.anyio
    async def test_get_create_or_update_valid_fields__RoleUpdate(self, mock_role_service: RoleService) -> None:
        role_update = RoleUpdate(name=RoleName.user)

        valid_fields = mock_role_service._get_create_or_update_valid_fields(schema=role_update)

        assert valid_fields == {"name": RoleName.user}

    @pytest.mark.anyio
    async def test_create__all_ok(self, mock_session: AsyncMock, mock_role_service: RoleService) -> None:
        mock_role_service._validate_create = AsyncMock()
        mock_role_service._get_create_or_update_valid_fields = MagicMock(return_value={"name": RoleName.user})

        role_create = RoleCreate(name=RoleName.user)
        role = await mock_role_service.create(create_schema=role_create)

        mock_role_service._validate_create.assert_called_once()
        mock_role_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        assert isinstance(role, Role)
        assert hasattr(role, "id")
        assert role.name == role_create.name

    @pytest.mark.anyio
    async def test_validate_update__all_ok(self, mock_role_service: RoleService, mock_roles: list[Role]) -> None:
        mock_role_service.get_by_id = AsyncMock(return_value=mock_roles[1])

        role = await mock_role_service._validate_update(entity_id=1, update_schema=RoleUpdate(name=RoleName.user))

        mock_role_service.get_by_id.assert_called_once()
        assert role == mock_roles[1]

    @pytest.mark.anyio
    async def test_validate_update__id_does_not_exist(self, mock_role_service: RoleService) -> None:
        mock_role_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=3, entity_type=EntityType.role)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_role_service._validate_update(entity_id=3, update_schema=RoleUpdate(name=RoleName.user))

        mock_role_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_update__all_ok(
        self, mock_session: AsyncMock, mock_role_service: RoleService, mock_roles: list[Role]
    ) -> None:
        mock_role_service._validate_update = AsyncMock(return_value=mock_roles[1])
        mock_role_service._get_create_or_update_valid_fields = MagicMock(return_value={"name": RoleName.user})

        role_update = RoleUpdate(name=RoleName.user)
        role = await mock_role_service.update(entity_id=mock_roles[1].id, update_schema=role_update)

        mock_role_service._validate_update.assert_called_once()
        mock_role_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert role.id == mock_roles[1].id
        assert role.name == role_update.name

    @pytest.mark.anyio
    async def test_update__id_does_not_exist(self, mock_session: AsyncMock, mock_role_service: RoleService) -> None:
        mock_role_service._validate_update = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=3, entity_type=EntityType.role)
        )
        mock_role_service._get_create_or_update_valid_fields = MagicMock(return_value={"name": RoleName.user})

        role_update = RoleUpdate(name=RoleName.user)
        with pytest.raises(EntityNotFoundException):
            await mock_role_service.update(entity_id=3, update_schema=role_update)

        mock_role_service._validate_update.assert_called_once()
        mock_role_service._get_create_or_update_valid_fields.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.refresh.assert_not_called

    @pytest.mark.anyio
    async def test_validate_delete__all_ok(self, mock_role_service: RoleService, mock_roles: list[Role]) -> None:
        mock_role_service.get_by_id = AsyncMock(return_value=mock_roles[1])

        role = await mock_role_service._validate_delete(entity_id=1)

        mock_role_service.get_by_id.assert_called_once()
        assert role == mock_roles[1]

    @pytest.mark.anyio
    async def test_validate_delete__id_not_found(self, mock_role_service: RoleService, mock_roles: list[Role]) -> None:
        mock_role_service.get_by_id = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=100, entity_type=EntityType.role)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_role_service._validate_delete(entity_id=100)

        mock_role_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_delete__all_ok(
        self, mock_session: AsyncMock, mock_role_service: RoleService, mock_roles: list[Role]
    ) -> None:
        mock_role_service._validate_delete = AsyncMock(return_value=mock_roles[1])

        role = await mock_role_service.delete(entity_id=mock_roles[1].id)

        mock_role_service._validate_delete.assert_called_once()
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()
        assert role == mock_roles[1]

    @pytest.mark.anyio
    async def test_delete__id_does_not_exist(self, mock_session: AsyncMock, mock_role_service: RoleService) -> None:
        mock_role_service._validate_delete = AsyncMock(
            side_effect=EntityNotFoundException(entity_id=3, entity_type=EntityType.role)
        )

        with pytest.raises(EntityNotFoundException):
            await mock_role_service.delete(entity_id=3)

        mock_role_service._validate_delete.assert_called_once()
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
