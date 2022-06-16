from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from auth.jwt import get_current_user
from posts.validators import post_exists
from database.db import get_db
from auth.schemas import TokenData

from . import services
from . import schemas
from . import validators


router = APIRouter(tags=["comments"], prefix="/api/v1/comments")


@router.get("/", response_model=List[schemas.OutComments])
async def get_comments_by_post(
    post: int = Query(...), database: Session = Depends(get_db)
):

    """Get comments by post"""

    _post = await post_exists(post, database)

    if not _post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    _comments = await services.get_comments(post, database)

    if not _comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comments not found"
        )

    return _comments


@router.post("/")
async def create_comment(
    comment: schemas.Comment,
    database: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):

    """Create new comment"""

    _post = await post_exists(comment.post, database)

    if not _post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    await services.create_comment(comment, database, current_user.id)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Comment was added"
    )


@router.post("/replies/")
async def create_replies_on_comment(
    replies: schemas.RepliesComment,
    database: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):

    """Create new replies on comment"""

    _comment = await validators.comment_exists(replies.comment, database)
    if not _comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    await services.create_replies(replies, database, current_user.id)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="Replies was added"
    )


@router.delete("/{id}/", response_class=JSONResponse)
async def delete_comment(
    id: int,
    database: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):

    """Delete comment by id"""

    _comment = await validators.comment_exists(id, database)
    if not _comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if _comment.author != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't delete not your comment",
        )

    await services.delete_comment(id, database)

    return JSONResponse(status_code=status.HTTP_200_OK, content="Comment was deleted")


@router.put("/{id}/", response_class=JSONResponse)
async def update_comment_by_id(
    id: int,
    comment_data: schemas.BaseComment,
    database: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):

    """Update comment by id"""

    _comment = await validators.comment_exists(id, database)
    if not _comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if _comment.author != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't update not your comment",
        )

    await services.update_comment(id, database, comment_data)

    return JSONResponse(status_code=status.HTTP_200_OK, content="Comment was updated")
