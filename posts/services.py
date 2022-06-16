from sqlalchemy.orm import Session
import random

from users import models as user_models

from . import models
from . import schemas


async def get_posts(id: int, database: Session):
    """Get posts by query params id"""

    return (
        database.query(models.Posts)
        .join(user_models.Users)
        .filter(models.Posts.author == id)
        .all()
    )


async def get_all_posts(database: Session):
    """Get all posts"""

    _posts = database.query(models.Posts).join(user_models.Users).all()

    random.shuffle(_posts)
    return _posts


async def create_post(post: schemas.Post, database: Session, author_id: int):
    """Create New Post"""

    _new_post = models.Posts(title=post.title, text=post.text, author=author_id)

    database.add(_new_post)
    database.commit()
    database.refresh(_new_post)


async def get_post_by_id(id: int, database: Session):
    """Get post by id"""

    return database.query(models.Posts).filter(models.Posts.id == id).first()


async def delete_post(id: int, database: Session):
    """Delete Post"""

    _ = database.query(models.Posts).filter(models.Posts.id == id).first()

    database.query(models.Posts).filter(models.Posts.id == id).delete()
    database.commit()


async def update_post(id: int, database: Session, post_data: schemas.Post) -> None:
    """Update Post"""

    database.query(models.Posts).filter(models.Posts.id == id).update(
        {models.Posts.title: post_data.title, models.Posts.text: post_data.text},
        synchronize_session=False,
    )

    database.commit()
