from sqlalchemy import Column, VARCHAR, BIGINT
from sqlalchemy.orm import relationship
from ..base import Base


class User(Base):
    __tablename__ = "user"

    name = Column(VARCHAR(7), primary_key=True, nullable=False)
    id = Column(VARCHAR(15), primary_key=True, nullable=False)
    password = Column(VARCHAR(60), nullable=False)
    balance = Column(BIGINT, default=0)

    pays = relationship("Pay", back_populates="user")
