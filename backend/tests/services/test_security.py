import pytest

from app.services.security import verify_password, get_password_hash


@pytest.mark.unit
class TestSecurityServices:
    @pytest.mark.anyio
    async def test_verify_password__returns_True(self):
        password = "secret123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True

    @pytest.mark.anyio
    async def test_verify_password__returns_False(self):
        password = "secret123"
        wrong_password = "wrong123"
        hashed = get_password_hash(password)

        assert verify_password(wrong_password, hashed) is False

    @pytest.mark.anyio
    async def test_verify_password__invalid_hash(self):
        with pytest.raises(ValueError):
            verify_password("test", "not_a_valid_hash")

    @pytest.mark.anyio
    async def test_get_password_hash__returns_hash(self):
        password = "secret123"
        hashed = get_password_hash(password)

        assert isinstance(hashed, str)
        assert hashed != password
        assert hashed.startswith("$2b$")
