from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db_models.base import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    type_id = Column(Integer, ForeignKey("type.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)

    user = relationship("User", back_populates="categories")
    type = relationship("Type", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    goals = relationship("Goal", back_populates="category")
