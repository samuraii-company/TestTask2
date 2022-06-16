from sqlalchemy.orm import Session

from . import models


async def comment_exists(id: int, database: Session):
    """Check comment exists in system"""

    return database.query(models.Comments).filter(models.Comments.id == id).first()
