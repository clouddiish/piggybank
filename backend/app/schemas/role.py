from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleOut(RoleBase):
    id: int


class RoleFilters(BaseModel):
    model_config = {"extra": "forbid"}

    name: list[str] | None = None
