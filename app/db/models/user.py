from sqlalchemy import Column, VARCHAR, BIGINT

from ..base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(VARCHAR(15), primary_key=True, nullable=False)
    name = Column(VARCHAR(7), nullable=False)
    password = Column(VARCHAR(60), nullable=False)
    balance = Column(BIGINT, default=0)
