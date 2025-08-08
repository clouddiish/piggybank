from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db_models.base import Base


class Type(Base):
    __tablename__ = "type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    categories = relationship("Category", back_populates="type", cascade="all, delete")
    goals = relationship("Goal", back_populates="type", cascade="all, delete")
    transactions = relationship("Transaction", back_populates="type", cascade="all, delete")
