from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    password2: str

    class Config:
        schema_extra = {
            "example": {
                "email": "test@gmail.com",
                "password": "secretpassword",
                "password2": "secretpassword",
            }
        }


class OutUser(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
        schema_extra = {"example": {"id": 1, "email": "test@gmail.com"}}
