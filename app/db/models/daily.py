from sqlalchemy import Column, VARCHAR, DATETIME, BIGINT, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base


class Daily(Base):
    __tableName__ = "daily"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    balance = Column(BIGINT, nullable=False)
    profit = Column(BIGINT, nullable=False, default=0)
    user_id = Column(VARCHAR(15), ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="daily")