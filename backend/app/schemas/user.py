from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)

    model_config = {"extra": "forbid"}


class UserUpdate(UserBase):
    role_id: int
    password: str = Field(min_length=8)

    model_config = {"extra": "forbid"}


class UserInDB(UserBase):
    password_hash: str


class UserOut(UserBase):
    role_id: int
    id: int


class UserFilters(BaseModel):
    role_id: list[int] | None = None
    email: list[str] | None = None

    model_config = {"extra": "forbid"}
