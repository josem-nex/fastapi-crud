from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base
from models.mixins import TimestampMixin, SoftDeleteMixin

class Tag(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # posts many-to-many
    posts = relationship("Post", secondary="post_tag", back_populates="tags")
