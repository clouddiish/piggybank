from unittest.mock import AsyncMock, MagicMock

import pytest

from app.common.exceptions import (
    EntityNotFoundException,
    ActionForbiddenException,
    EntityNotAssociatedException,
)
from app.db_models import Goal, Type, Category, User
from app.schemas import GoalCreate, GoalUpdate, GoalFilters
from app.services import GoalService


@pytest.mark.unit
class TestGoalService:
    @pytest.mark.anyio
    async def test_get_by_id__all_ok_same_user(
        self,
        mock_session: AsyncMock,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_goals[0]
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=False)

        goal = await mock_goal_service.get_by_id(entity_id=mock_goals[0].id, gotten_by=mock_users[0])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_goal_service.user_service.is_admin.assert_not_called()
        assert goal == mock_goals[0]

    @pytest.mark.anyio
    async def test_get_by_id__all_ok_admin(
        self,
        mock_session: AsyncMock,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_goals[0]
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=True)

        goal = await mock_goal_service.get_by_id(entity_id=mock_goals[0].id, gotten_by=mock_users[1])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_goal_service.user_service.is_admin.assert_called_once()
        assert goal == mock_goals[0]

    @pytest.mark.anyio
    async def test_get_by_id__id_does_not_exist(
        self, mock_session: AsyncMock, mock_goal_service: GoalService, mock_users: list[User]
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = None

        with pytest.raises(EntityNotFoundException):
            await mock_goal_service.get_by_id(entity_id=999, gotten_by=mock_users[0])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()

    @pytest.mark.anyio
    async def test_get_by_id__different_user(
        self,
        mock_session: AsyncMock,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalar_one_or_none.return_value = mock_goals[0]
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_goal_service.get_by_id(entity_id=mock_goals[0].id, gotten_by=mock_users[1])

        mock_session.execute.assert_called_once()
        mock_query.scalar_one_or_none.assert_called_once()
        mock_goal_service.user_service.is_admin.assert_called_once()

    @pytest.mark.anyio
    async def test_get_all_with_filters__admin(
        self,
        mock_session: AsyncMock,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = mock_goals
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=True)

        goals = await mock_goal_service.get_all_with_filters(gotten_by=mock_users[1])

        mock_goal_service.user_service.is_admin.assert_called_once()
        mock_session.execute.assert_called_once()
        assert goals == mock_goals

    @pytest.mark.anyio
    async def test_get_all_with_filters__non_admin_adds_user_filter(
        self,
        mock_session: AsyncMock,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
        mock_users: list[User],
    ) -> None:
        mock_query = MagicMock()
        mock_session.execute.return_value = mock_query
        mock_query.scalars.return_value.all.return_value = [mock_goals[0]]
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=False)

        filters = GoalFilters(type_id=[1])
        goals = await mock_goal_service.get_all_with_filters(filters=filters, gotten_by=mock_users[0])

        assert filters.user_id == [mock_users[0].id]
        mock_goal_service.user_service.is_admin.assert_called_once()
        mock_session.execute.assert_called_once()
        assert goals == [mock_goals[0]]

    @pytest.mark.anyio
    async def test_validate_create__all_ok(
        self, mock_goal_service: GoalService, mock_types: list[Type], mock_users: list[User]
    ) -> None:
        create_schema = GoalCreate(
            type_id=1,
            category_id=None,
            name="test goal",
            start_date="2024-01-01",
            end_date="2024-12-31",
            target_value=100.0,
        )
        mock_goal_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        await mock_goal_service._validate_create(create_schema=create_schema, created_by=mock_users[0])

        mock_goal_service.type_service.get_by_id.assert_called_once()

    @pytest.mark.anyio
    async def test_validate_create__category_not_associated(
        self,
        mock_goal_service: GoalService,
        mock_types: list[Type],
        mock_categories: list[Category],
        mock_users: list[User],
    ) -> None:
        create_schema = create_schema = GoalCreate(
            type_id=1,
            category_id=2,
            name="test goal",
            start_date="2024-01-01",
            end_date="2024-12-31",
            target_value=100.0,
        )
        mock_goal_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])
        mock_goal_service.category_service.get_by_id = AsyncMock(return_value=mock_categories[1])  # mismatched type

        with pytest.raises(EntityNotAssociatedException):
            await mock_goal_service._validate_create(create_schema=create_schema, created_by=mock_users[0])

    @pytest.mark.anyio
    async def test_validate_update__all_ok_admin(
        self,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
        mock_types: list[Type],
        mock_users: list[User],
    ) -> None:
        mock_goal_service.get_by_id = AsyncMock(return_value=mock_goals[0])
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=True)
        mock_goal_service.type_service.get_by_id = AsyncMock(return_value=mock_types[0])

        goal = await mock_goal_service._validate_update(
            entity_id=1,
            update_schema=GoalUpdate(
                type_id=1,
                category_id=None,
                name="test goal",
                start_date="2024-01-01",
                end_date="2024-12-31",
                target_value=100.0,
            ),
            updated_by=mock_users[1],
        )

        assert goal == mock_goals[0]

    @pytest.mark.anyio
    async def test_validate_update__different_user_forbidden(
        self,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
        mock_users: list[User],
    ) -> None:
        mock_goal_service.get_by_id = AsyncMock(return_value=mock_goals[0])
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_goal_service._validate_update(
                entity_id=1,
                update_schema=GoalUpdate(
                    type_id=1,
                    category_id=1,
                    name="test goal",
                    start_date="2024-01-01",
                    end_date="2024-12-31",
                    target_value=100.0,
                ),
                updated_by=mock_users[1],
            )

    @pytest.mark.anyio
    async def test_validate_delete__all_ok_admin(
        self, mock_goal_service: GoalService, mock_goals: list[Goal], mock_users: list[User]
    ) -> None:
        mock_goal_service.get_by_id = AsyncMock(return_value=mock_goals[0])
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=True)

        goal = await mock_goal_service._validate_delete(entity_id=1, deleted_by=mock_users[1])

        assert goal == mock_goals[0]

    @pytest.mark.anyio
    async def test_validate_delete__different_user_forbidden(
        self, mock_goal_service: GoalService, mock_goals: list[Goal], mock_users: list[User]
    ) -> None:
        mock_goal_service.get_by_id = AsyncMock(return_value=mock_goals[0])
        mock_goal_service.user_service.is_admin = AsyncMock(return_value=False)

        with pytest.raises(ActionForbiddenException):
            await mock_goal_service._validate_delete(entity_id=1, deleted_by=mock_users[1])

    @pytest.mark.anyio
    async def test_create__all_ok(self, mock_session: AsyncMock, mock_goal_service: GoalService) -> None:
        mock_goal_service._validate_create = AsyncMock()
        mock_goal_service._get_create_or_update_valid_fields = MagicMock(
            return_value={
                "type_id": 1,
                "name": "test goal",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "target_value": 200.0,
                "user_id": 1,
            }
        )

        create_schema = GoalCreate(
            type_id=1,
            name="test goal",
            start_date="2024-01-01",
            end_date="2024-12-31",
            target_value=200.0,
        )
        goal = await mock_goal_service.create(create_schema=create_schema)

        mock_goal_service._validate_create.assert_called_once()
        mock_goal_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        assert isinstance(goal, Goal)
        assert goal.type_id == 1
        assert goal.name == "test goal"
        assert str(goal.start_date) == "2024-01-01"
        assert str(goal.end_date) == "2024-12-31"
        assert goal.target_value == 200.0

    @pytest.mark.anyio
    async def test_update__all_ok(
        self,
        mock_session: AsyncMock,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
        mock_users: list[User],
    ) -> None:
        mock_goal_service._validate_update = AsyncMock(return_value=mock_goals[0])
        mock_goal_service._get_create_or_update_valid_fields = MagicMock(return_value={"target_value": 200.0})

        update_schema = GoalUpdate(
            type_id=1,
            name="test goal",
            start_date="2024-01-01",
            end_date="2024-12-31",
            target_value=200.0,
        )
        goal = await mock_goal_service.update(entity_id=1, update_schema=update_schema, updated_by=mock_users[0])

        mock_goal_service._validate_update.assert_called_once()
        mock_goal_service._get_create_or_update_valid_fields.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert goal.target_value == 200.0

    @pytest.mark.anyio
    async def test_delete__all_ok(
        self,
        mock_session: AsyncMock,
        mock_goal_service: GoalService,
        mock_goals: list[Goal],
    ) -> None:
        mock_goal_service._validate_delete = AsyncMock(return_value=mock_goals[0])

        goal = await mock_goal_service.delete(entity_id=mock_goals[0].id)

        mock_goal_service._validate_delete.assert_called_once()
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()
        assert goal == mock_goals[0]
