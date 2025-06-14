from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db_models.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role = relationship("Role", back_populates="users")
    categories = relationship("Category", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
