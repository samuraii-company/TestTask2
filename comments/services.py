from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from posts.models import Posts

from . import models
from . import schemas


def transaction(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception:
            database = args[1]
            database.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong"
            )

    return wrapper


async def get_comments(id: int, database: Session):
    """Get comments by post"""

    return (
        database.query(models.Comments)
        .join(Posts)
        .filter(models.Comments.post == id)
        .all()
    )


@transaction
async def create_comment(comment: schemas.Comment, database: Session, id: int):
    """Create new comment"""

    _comment = models.Comments(text=comment.text, author=id, post=comment.post)
    database.add(_comment)

    _ = (  # noqa
        database.query(Posts)
        .filter(Posts.id == comment.post)
        .update(
            {Posts.comments_count: Posts.comments_count + 1}, synchronize_session=False
        )
    )

    database.commit()


@transaction
async def delete_comment(id: int, database: Session):
    """Delete comment"""

    _comment = database.query(models.Comments).filter(models.Comments.id == id).first()

    _ = (  # noqa
        database.query(Posts)
        .filter(Posts.id == _comment.post)
        .update(
            {Posts.comments_count: Posts.comments_count - 1},
            synchronize_session=False,
        )
    )
    database.query(models.Comments).filter(models.Comments.id == id).delete()

    database.commit()


async def update_comment(id: int, database: Session, comment_data: schemas.BaseComment):
    """Update Comment"""

    database.query(models.Comments).filter(models.Comments.id == id).update(
        {models.Comments.text: comment_data.text}, synchronize_session=False
    )

    database.commit()


@transaction
async def create_replies(
    replies: schemas.RepliesComment, database: Session, current_user: int
):
    """Create new replies on comment"""
    _replies = models.Comments(
        text=replies.text,
        author=current_user,
        answer_comment_id=replies.comment,
    )

    database.add(_replies)
    database.commit()
    database.refresh(_replies)
