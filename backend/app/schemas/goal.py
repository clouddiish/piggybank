from datetime import date
from typing import ClassVar

from pydantic import BaseModel, model_validator


class GoalBase(BaseModel):
    type_id: int
    category_id: int | None = None
    name: str
    start_date: date
    end_date: date
    target_value: float

    @model_validator(mode="after")
    def check_dates(cls, model):
        if model.end_date <= model.start_date:
            raise ValueError("end_date must be later than start_date")
        return model


class GoalCreate(GoalBase):
    model_config = {"extra": "forbid"}


class GoalUpdate(GoalBase):
    model_config = {"extra": "forbid"}


class GoalOut(GoalBase):
    id: int
    user_id: int


class GoalFilters(BaseModel):
    user_id: list[int] | None = None
    type_id: list[int] | None = None
    category_id: list[int] | None = None
    name: list[str] | None = None
    start_date_gt: date | None = None
    start_date_lt: date | None = None
    end_date_gt: date | None = None
    end_date_lt: date | None = None
    target_value_gt: float | None = None
    target_value_lt: float | None = None

    list_filters: ClassVar[list[str]] = ["user_id", "type_id", "category_id"]
    gt_filters: ClassVar[list[str]] = ["start_date_gt", "end_date_gt", "target_value_gt"]
    lt_filters: ClassVar[list[str]] = ["start_date_lt", "end_date_lt", "target_value_lt"]
    kw_filters: ClassVar[list[str]] = ["name"]

    model_config = {"extra": "forbid"}
