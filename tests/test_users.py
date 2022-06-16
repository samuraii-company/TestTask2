import pytest
from httpx import AsyncClient

from auth.jwt import create_access_token
from database.test_db import app, override_get_db

from users.models import Users


class TestUser:
    def setup(self):
        self.user_access_token = create_access_token({"sub": "test@gmail.com", "id": 1})

        self.database = next(override_get_db())
        self.new_user = Users(email="test3@gmail.com", password="password")
        self.database.add(self.new_user)
        self.database.commit()
        self.database.refresh(self.new_user)

        self.bad_id: int = 100

    @pytest.mark.asyncio
    async def test_all_users(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:

            """Get all users"""
            response = await ac.get(
                "api/v1/users/",
            )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_user_by_id(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:

            """Get user by id"""
            get_response = await ac.get(
                f"api/v1/users/{self.new_user.id}/",
            )
            assert get_response.status_code == 200

            """User with this id not found"""
            bad_request = await ac.get(
                f"api/v1/users/{self.bad_id}/",
            )
            assert bad_request.status_code == 404
