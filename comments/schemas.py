from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from users.schemas import OutUser


class BaseComment(BaseModel):
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Updated Comment",
            }
        }


class Comment(BaseComment):
    post: int

    class Config:
        schema_extra = {
            "example": {
                "text": "Some Comment",
                "post": 1,
            }
        }


class RepliesComment(BaseModel):
    text: str
    comment: int

    class Config:
        schema_extra = {
            "example": {
                "text": "Some Replies",
                "comment": 1,
            }
        }


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
        schema_extra = {
            "example": [
                {
                    "id": 1,
                    "text": "Some Comment",
                    "created_at": "2022-06-16T17:42:42.542307",
                    "comment_author": {"id": 1, "email": "test@gmail.com"},
                    "children": [],
                },
                {
                    "id": 2,
                    "text": "Another Comment",
                    "created_at": "2022-06-16T17:43:15.629675",
                    "comment_author": {"id": 1, "email": "test@gmail.com"},
                    "children": [],
                },
            ]
        }
