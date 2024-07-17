from sqlalchemy import Column, VARCHAR, BIGINT, ForeignKey, INTEGER
from sqlalchemy.orm import relationship

from ..base import Base


class Daily(Base):
    __tableName__ = "daily"
    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    balance = Column(BIGINT, nullable=False)
    profit = Column(BIGINT, nullable=False, default=0)
    year = Column(INTEGER, nullable=False)
    month = Column(INTEGER, nullable=False)
    day = Column(INTEGER, nullable=False)
    user_id = Column(VARCHAR(15), ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="dailies")
