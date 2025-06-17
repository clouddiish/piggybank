import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.config import get_settings
from app.db_models import Role
from app.services import RoleService


settings = get_settings()


@pytest.fixture
def mock_role_service(mock_session_fixture: AsyncMock) -> RoleService:
    return RoleService(session=mock_session_fixture)


class TestRoleServices:
    @pytest.mark.anyio
    async def test_get_roles__no_filters(self, mock_session_fixture: AsyncMock, mock_role_service: RoleService) -> None:
        mock_roles = [Role(id=i, name=role_name) for i, role_name in enumerate(settings.initial_roles)]
        mock_result = MagicMock()
        mock_session_fixture.execute.return_value = mock_result
        mock_result.scalars.return_value.all.return_value = mock_roles

        result = await mock_role_service.get_roles()

        mock_session_fixture.execute.assert_called_once()
        assert result == mock_roles
