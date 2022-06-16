from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(100), index=True)
    password = Column(String(100))
    join_at = Column(DateTime, default=datetime.now)
    posts = relationship("Posts", back_populates="post_author")
    likes = relationship("Likes", back_populates="like_author")
    comments = relationship("Comments", back_populates="comment_author")
