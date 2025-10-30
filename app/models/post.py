from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.base import Base
from models.mixins import TimestampMixin, SoftDeleteMixin
from models.association_tables import post_tag

class Post(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text)

    # FK users (owner)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    owner = relationship("User", back_populates="posts")

    # tags many-to-many
    tags = relationship("Tag", secondary=post_tag, back_populates="posts")

    # one-to-many with comments
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
