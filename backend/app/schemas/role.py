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

    model_config = {"extra": "forbid"}
