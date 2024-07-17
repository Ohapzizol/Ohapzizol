from sqlalchemy import Column, VARCHAR, DATE, BIGINT, ForeignKey, TIME
from sqlalchemy.orm import relationship
from ..base import Base


class Pay(Base):
    __tablename__ = "pay"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(30), nullable=False)
    value = Column(BIGINT, nullable=False)
    description = Column(VARCHAR(500))
    date = Column(DATE, nullable=False)
    time = Column(TIME, nullable=False)
    tag = Column(VARCHAR(10))
    user_id = Column(VARCHAR(15), ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="pays")
