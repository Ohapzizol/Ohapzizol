from sqlalchemy import Column, VARCHAR, BIGINT
from sqlalchemy.orm import relationship

from ..base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(VARCHAR(15), primary_key=True, nullable=False)
    name = Column(VARCHAR(4), nullable=False)
    password = Column(VARCHAR(60), nullable=False)
    balance = Column(BIGINT, nullable=False)
    pays = relationship("Pay", back_populates="user")
    dailies = relationship("Daily", back_populates="user")
