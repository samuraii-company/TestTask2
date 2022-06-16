from sqlalchemy.orm import Session

from . import models


async def post_exists(id: int, database: Session):
    """Check post exists in system"""

    return database.query(models.Posts).filter(models.Posts.id == id).first()
