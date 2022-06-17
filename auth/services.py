from sqlalchemy.orm import Session

from users import schemas, models
from auth import hashing


async def new_user_register(user: schemas.User, database: Session) -> None:
    """Create new user"""

    _user = models.Users(
        email=user.email,
        password=hashing.get_password_hash(user.password),
    )

    database.add(_user)
    database.commit()
    database.refresh(_user)
