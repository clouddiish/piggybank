import pytest

from app.db_models import Type


@pytest.mark.unit
class TestTypeDbModel:
    @pytest.mark.anyio
    async def test_type_model__all_ok(self):
        type = Type(name="test type")

        assert hasattr(type, "id")
        assert type.name == "test type"
