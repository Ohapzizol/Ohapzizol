from sqlalchemy import Column, VARCHAR, DATETIME, BIGINT, INTEGER, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    content = Column(VARCHAR(50), nullable=False)
    month = Column(INTEGER, nullable=False)
    year = Column(INTEGER, nullable=False)
    user_id = Column(VARCHAR(15), ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="comment")
