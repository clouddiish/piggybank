import pytest

from app.db_models import Role


@pytest.mark.unit
class TestRoleDbModel:
    @pytest.mark.anyio
    async def test_role_model__all_ok(self):
        role = Role(name="test role")

        assert hasattr(role, "id")
        assert role.name == "test role"
