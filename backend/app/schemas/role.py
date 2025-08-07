from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    model_config = {"extra": "forbid"}


class RoleUpdate(RoleBase):
    model_config = {"extra": "forbid"}


class RoleOut(RoleBase):
    id: int


class RoleFilters(BaseModel):
    model_config = {"extra": "forbid"}

    name: list[str] | None = None
