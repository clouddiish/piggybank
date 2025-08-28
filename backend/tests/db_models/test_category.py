import pytest

from app.db_models import Category


@pytest.mark.unit
class TestCategoryDbModel:
    @pytest.mark.anyio
    async def test_category_model__all_ok(self):
        category = Category(user_id=1, type_id=1, name="test category")

        assert hasattr(category, "id")
        assert category.user_id == 1
        assert category.type_id == 1
        assert category.name == "test category"
