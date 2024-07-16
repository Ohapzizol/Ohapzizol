from sqlalchemy import Column, VARCHAR, DATETIME, BIGINT, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base


class Pay(Base):
    __tablename__ = "pay"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(30), nullable=False)
    value = Column(BIGINT, nullable=False)
    description = Column(VARCHAR(500))
    date = Column(DATETIME, nullable=False)
    tag = Column(VARCHAR(10), nullable=False)
    user_id = Column(VARCHAR(15), ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="pays")
