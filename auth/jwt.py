from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from settings import config as cfg
from . import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = cfg.SECRET_TOKEN
ALGORITHM = cfg.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def create_access_token(data: dict):
    """Create access token"""

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """verify token"""

    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        id: int = payload.get("id")
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, email=email)
        return token_data

    except JWTError:
        raise credentials_exception


def get_current_user(data: str = Depends(oauth2_scheme)):
    """Get current authenticated user"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(data, credentials_exception)
    return token_data
