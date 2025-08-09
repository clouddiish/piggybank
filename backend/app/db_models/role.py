from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db_models.base import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_protected = Column(Boolean, default=False)

    users = relationship("User", back_populates="role", cascade="all, delete")
