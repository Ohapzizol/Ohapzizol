from sqlalchemy import Column, VARCHAR, DATETIME, BIGINT
from app.db.base import Base

class Pay(Base):
    __tablename__ = "pay"

    name = Column(VARCHAR(30), primary_key=True, nullable=False)
    value = Column(BIGINT, nullable=False)
    description = Column(VARCHAR(500))
    date = Column(DATETIME, nullable=False)
    tag = Column(VARCHAR(10), nullable=False)
