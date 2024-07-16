from sqlalchemy import Column, VARCHAR, BIGINT

from ..base_class import Base


class User(Base):
    __tablename__ = "user"
    id = Column(VARCHAR(15), primary_key=True, nullable=False)
    name = Column(VARCHAR(4), nullable=False)
    password = Column(VARCHAR(15), nullable=False)
    balance = Column(BIGINT, nullable=False)
