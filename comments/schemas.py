from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from users.schemas import OutUser


class BaseComment(BaseModel):
    text: str


class Comment(BaseComment):
    post: int


class RepliesComment(BaseModel):
    text: str
    comment: int


class OutBase(BaseModel):
    id: int
    text: str
    created_at: datetime
    comment_author: OutUser

    class Config:
        orm_mode = True


class OutReplies(OutBase):
    children: Optional[List["OutReplies"]] = []

    class Config:
        orm_mode = True


class OutComments(OutBase):
    children: Optional[List[OutReplies]] = []

    class Config:
        orm_mode = True
