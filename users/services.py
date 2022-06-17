from sqlalchemy.orm import Session
from typing import List

from . import models


async def get_all_users(database: Session) -> List[models.Users] | None:
    """Get all users"""

    return database.query(models.Users).all()


async def get_user_by_id(id: int, database: Session) -> models.Users | None:
    """Get user by id"""

    return database.query(models.Users).filter(models.Users.id == id).first()
