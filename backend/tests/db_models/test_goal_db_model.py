import pytest

from app.db_models import Goal


@pytest.mark.unit
class TestGoalDbModel:
    @pytest.mark.anyio
    async def test_goal_model__all_ok(self):
        goal = Goal(
            user_id=1,
            type_id=2,
            category_id=3,
            name="test goal",
            start_date="2026-01-01",
            end_date="2026-12-31",
            target_value=1000,
        )

        assert hasattr(goal, "id")
        assert goal.user_id == 1
        assert goal.type_id == 2
        assert goal.category_id == 3
        assert goal.name == "test goal"
        assert str(goal.start_date) == "2026-01-01"
        assert str(goal.end_date) == "2026-12-31"
        assert goal.target_value == 1000
