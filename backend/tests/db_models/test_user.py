import pytest

from app.db_models import User


@pytest.mark.unit
class TestUserDbModel:
    @pytest.mark.anyio
    async def test_user_model__all_ok(self):
        user = User(email="testemail@example.com", password_hash="testhash", is_protected=False)

        assert hasattr(user, "id")
        assert user.email == "testemail@example.com"
        assert user.password_hash == "testhash"
        assert user.is_protected is False
