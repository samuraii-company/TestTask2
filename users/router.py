from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from typing import List
from sqlalchemy.orm import Session

from database.db import get_db

from . import services
from . import schemas


router = APIRouter(tags=["users"], prefix="/api/v1/users")


@router.get("/", response_model=List[schemas.OutUser])
async def get_all_users(database: Session = Depends(get_db)):
    """Get all users"""
    
    users = await services.get_all_users(database)
    return users


@router.get("/{id}/", response_model=schemas.OutUser)
async def get_user_by_id(id: int, database: Session = Depends(get_db)):
    """Get user by id"""

    _user = await services.get_user_by_id(id, database)
    if not _user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )

    return _user
