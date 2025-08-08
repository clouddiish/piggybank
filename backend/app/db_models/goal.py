from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.db_models.base import Base


class Goal(Base):
    __tablename__ = "goal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    type_id = Column(Integer, ForeignKey("type.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    target_value = Column(Numeric, nullable=False)

    user = relationship("User", back_populates="goals")
    type = relationship("Type", back_populates="goals")
    category = relationship("Category", back_populates="goals")
