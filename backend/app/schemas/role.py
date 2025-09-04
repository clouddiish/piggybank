from typing import ClassVar

from pydantic import BaseModel

from app.common.enums import RoleName


class RoleBase(BaseModel):
    name: RoleName


class RoleCreate(RoleBase):
    model_config = {"extra": "forbid"}


class RoleUpdate(RoleBase):
    model_config = {"extra": "forbid"}


class RoleOut(RoleBase):
    id: int


class RoleFilters(BaseModel):
    name: list[RoleName] | None = None

    list_filters: ClassVar[list[str]] = ["name"]
    gt_filters: ClassVar[list[str]] = []
    lt_filters: ClassVar[list[str]] = []
    kw_filters: ClassVar[list[str]] = []

    model_config = {"extra": "forbid"}
