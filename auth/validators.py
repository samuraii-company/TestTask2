from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from users import models
from users import schemas

MIN_PASSWORD_LENGTH = 9


async def user_validation(user: schemas.User, database: Session) -> bool | None:
    """User Validation"""

    if not user.password == user.password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match"
        )

    if len(user.password) <= MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords lower than 9 symbols",
        )

    if database.query(models.Users).filter(models.Users.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    return True
