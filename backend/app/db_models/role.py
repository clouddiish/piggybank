from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db_models.base import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="role")
