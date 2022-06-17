from sqlalchemy.orm import Session

from posts.models import Posts
from comments.services import transaction

from . import models
from . import schemas


@transaction
async def add_like(like: schemas.Like, database: Session, id: int) -> None:
    """Add like"""

    _like = models.Likes(post=like.post, user=id)

    database.add(_like)

    database.query(Posts).filter(Posts.id == like.post).update(
        {Posts.likes_count: Posts.likes_count + 1}, synchronize_session=False
    )

    database.commit()


@transaction
async def delete_like(like: schemas.Like, database: Session, id: int) -> None:
    """Delete like"""

    _ = (  # noqa
        database.query(Posts)
        .filter(Posts.id == like.post)
        .update({Posts.likes_count: Posts.likes_count - 1}, synchronize_session=False)
    )
    database.query(models.Likes).filter(
        models.Likes.post == like.post, models.Likes.user == id
    ).delete()

    database.commit()
