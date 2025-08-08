from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.db_models.base import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    type_id = Column(Integer, ForeignKey("type.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="SET NULL"), nullable=True)
    date = Column(Date, nullable=False)
    value = Column(Numeric, nullable=False)
    comment = Column(String, nullable=True)

    user = relationship("User", back_populates="transactions")
    type = relationship("Type", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
