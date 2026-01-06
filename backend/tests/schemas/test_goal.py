from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.goal import GoalCreate, GoalUpdate, GoalOut, GoalFilters


@pytest.mark.unit
class TestGoalSchemas:
    @pytest.mark.anyio
    async def test_GoalCreate__all_ok(self):
        data = {
            "type_id": 1,
            "category_id": 2,
            "name": "test goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
            "target_value": 1000.0,
        }
        goal = GoalCreate(**data)

        assert goal.type_id == 1
        assert goal.category_id == 2
        assert goal.name == "test goal"
        assert goal.start_date == date(2026, 1, 1)
        assert goal.end_date == date(2026, 12, 31)
        assert goal.target_value == 1000.0

    @pytest.mark.anyio
    async def test_GoalCreate__extra_field(self):
        data = {
            "type_id": 1,
            "category_id": 2,
            "name": "test goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
            "target_value": 1000.0,
            "extra": "not allowed",
        }
        with pytest.raises(ValidationError) as e:
            GoalCreate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalCreate__missing_field(self):
        data = {
            "type_id": 1,
        }
        with pytest.raises(ValidationError) as e:
            GoalCreate(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalCreate__invalid_type(self):
        data = {
            "type_id": "wrong",
            "category_id": 2,
            "name": "test goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
            "target_value": 1000.0,
        }
        with pytest.raises(ValidationError) as e:
            GoalCreate(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalCreate__invalid_dates(self):
        data = {
            "type_id": 1,
            "category_id": 2,
            "name": "test goal",
            "start_date": date(2026, 12, 31),
            "end_date": date(2026, 1, 1),
            "target_value": 1000.0,
        }
        with pytest.raises(ValidationError) as e:
            GoalCreate(**data)

        assert "end_date must be later than start_date" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalUpdate__all_ok(self):
        data = {
            "type_id": 1,
            "category_id": 2,
            "name": "updated goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
            "target_value": 2000.0,
        }
        goal = GoalUpdate(**data)

        assert goal.type_id == 1
        assert goal.category_id == 2
        assert goal.name == "updated goal"
        assert goal.start_date == date(2026, 1, 1)
        assert goal.end_date == date(2026, 12, 31)
        assert goal.target_value == 2000.0

    @pytest.mark.anyio
    async def test_GoalUpdate__extra_field(self):
        data = {
            "type_id": 1,
            "category_id": 2,
            "name": "updated goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
            "target_value": 2000.0,
            "extra": "not allowed",
        }
        with pytest.raises(ValidationError) as e:
            GoalUpdate(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalUpdate__missing_field(self):
        data = {
            "name": "updated goal",
        }
        with pytest.raises(ValidationError) as e:
            GoalUpdate(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalUpdate__invalid_type(self):
        data = {
            "type_id": "wrong",
            "category_id": 2,
            "name": "updated goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
            "target_value": 2000.0,
        }
        with pytest.raises(ValidationError) as e:
            GoalUpdate(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalUpdate__invalid_dates(self):
        data = {
            "type_id": 1,
            "category_id": 2,
            "name": "updated goal",
            "start_date": date(2026, 12, 31),
            "end_date": date(2026, 1, 1),
            "target_value": 2000.0,
        }
        with pytest.raises(ValidationError) as e:
            GoalUpdate(**data)

        assert "end_date must be later than start_date" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalOut__all_ok(self):
        data = {
            "id": 1,
            "user_id": 5,
            "type_id": 1,
            "category_id": 2,
            "name": "test goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
            "target_value": 1000.0,
        }
        goal = GoalOut(**data)

        assert goal.id == 1
        assert goal.user_id == 5
        assert goal.type_id == 1
        assert goal.category_id == 2
        assert goal.name == "test goal"
        assert goal.start_date == date(2026, 1, 1)
        assert goal.end_date == date(2026, 12, 31)
        assert goal.target_value == 1000.0

    @pytest.mark.anyio
    async def test_GoalOut__missing_field(self):
        data = {
            "id": 1,
            "user_id": 5,
            "type_id": 1,
            "category_id": 2,
            "name": "test goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
        }
        with pytest.raises(ValidationError) as e:
            GoalOut(**data)

        assert "Field required" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalOut__invalid_type(self):
        data = {
            "id": 1,
            "user_id": 5,
            "type_id": "wrong",
            "category_id": 2,
            "name": "test goal",
            "start_date": date(2026, 1, 1),
            "end_date": date(2026, 12, 31),
            "target_value": 1000.0,
        }
        with pytest.raises(ValidationError) as e:
            GoalOut(**data)

        assert "validation error for" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalOut__invalid_dates(self):
        data = {
            "id": 1,
            "user_id": 5,
            "type_id": 1,
            "category_id": 2,
            "name": "test goal",
            "start_date": date(2026, 12, 31),
            "end_date": date(2026, 1, 1),
            "target_value": 1000.0,
        }
        with pytest.raises(ValidationError) as e:
            GoalOut(**data)

        assert "end_date must be later than start_date" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalFilters__all_ok(self):
        data = {
            "user_id": [1, 2],
            "type_id": [3],
            "category_id": [4],
            "name": ["goal"],
            "start_date_gt": date(2026, 1, 1),
            "end_date_lt": date(2026, 12, 31),
            "target_value_gt": 100.0,
            "target_value_lt": 5000.0,
        }
        filters = GoalFilters(**data)

        assert filters.user_id == [1, 2]
        assert filters.type_id == [3]
        assert filters.category_id == [4]
        assert filters.name == ["goal"]
        assert filters.start_date_gt == date(2026, 1, 1)
        assert filters.end_date_lt == date(2026, 12, 31)
        assert filters.target_value_gt == 100.0
        assert filters.target_value_lt == 5000.0

    @pytest.mark.anyio
    async def test_GoalFilters__None_ok(self):
        data = {}
        filters = GoalFilters(**data)

        assert filters.user_id is None
        assert filters.type_id is None
        assert filters.category_id is None
        assert filters.name is None
        assert filters.start_date_gt is None
        assert filters.end_date_lt is None
        assert filters.target_value_gt is None
        assert filters.target_value_lt is None

    @pytest.mark.anyio
    async def test_GoalFilters__extra_field(self):
        data = {
            "user_id": [1, 2],
            "extra": "not allowed",
        }
        with pytest.raises(ValidationError) as e:
            GoalFilters(**data)

        assert "extra" in str(e.value)

    @pytest.mark.anyio
    async def test_GoalFilters__invalid_type(self):
        data = {
            "user_id": "should be list",
        }
        with pytest.raises(ValidationError) as e:
            GoalFilters(**data)

        assert "Input should be a valid list" in str(e.value)
