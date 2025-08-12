from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import relationship

from app.common.enums import RoleName
from app.db_models.base import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(RoleName), nullable=False)

    users = relationship("User", back_populates="role", cascade="all, delete")
