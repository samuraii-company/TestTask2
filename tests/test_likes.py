import pytest
from httpx import AsyncClient
from database.test_db import app
from auth.jwt import create_access_token
from database.test_db import app, override_get_db

from users.models import Users
from posts.models import Posts


class TestLikes:
    def setup(self):
        self.client = AsyncClient(app=app, base_url="http://test")
        self.database = next(override_get_db())
        self.new_user = Users(email="test3@gmail.com", password="password")
        self.post = Posts(title="Test", text="Test", author=self.new_user.id)
        self.database.add(self.new_user)
        self.database.add(self.post)
        self.database.commit()
        self.database.refresh(self.new_user)
        self.database.refresh(self.post)
        self.user_access_token = create_access_token(
            {"sub": self.new_user.email, "id": self.new_user.id}
        )

    @pytest.mark.asyncio
    async def test_likes(self):
        async with self.client as ac:

            """Success Adding like on post"""
            response = await ac.post(
                "api/v1/likes/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
                json={"post": self.post.id},
            )
            assert response.status_code == 200

            """Removing like"""
            response = await ac.post(
                "api/v1/likes/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
                json={"post": self.post.id},
            )
            assert response.status_code == 200

            """Post not found for like"""
            response = await ac.post(
                "api/v1/likes/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
                json={"post": 20},
            )
            assert response.status_code == 404
