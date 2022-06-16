import pytest
from httpx import AsyncClient
from database.test_db import app
from auth.jwt import create_access_token
from database.test_db import app, override_get_db

from users.models import Users


class TestPosts:
    def setup(self):
        self.client = AsyncClient(app=app, base_url="http://test")
        self.database = next(override_get_db())
        self.new_user = Users(email="test4@gmail.com", password="password")
        self.database.add(self.new_user)
        self.database.commit()
        self.database.refresh(self.new_user)
        self.user_access_token = create_access_token({"sub": "test@gmail.com", "id": 1})
        self.user_access_token_2 = create_access_token(
            {"sub": self.new_user.email, "id": self.new_user.id}
        )

    @pytest.mark.asyncio
    async def test_posts(self):
        async with self.client as ac:

            """Posts by user not found"""
            response = await ac.get(
                f"api/v1/posts/?user={self.new_user.id}",
            )
            assert response.status_code == 404

            """Create new post"""
            response = await ac.post(
                "api/v1/posts/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
                json={"title": "Test", "text": "Text text"},
            )
            assert response.status_code == 201

            """Get posts by user"""
            response = await ac.get(
                f"api/v1/posts/?user={self.new_user.id}",
            )
            assert response.status_code == 200

            """Get all posts"""
            response = await ac.get(
                "api/v1/posts/",
            )
            assert response.status_code == 200

            """Get post by id"""
            response = await ac.get(
                "api/v1/posts/3/",
            )
            assert response.status_code == 200

            """Update post by id"""
            response = await ac.put(
                "api/v1/posts/3/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
                json={
                    "title": "New Updated Post",
                    "text": "New Text",
                },
            )
            assert response.status_code == 200

            """Posts for updating not found"""
            response = await ac.put(
                "api/v1/posts/13/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
                json={
                    "title": "New Updated Post",
                    "text": "New Text",
                },
            )
            assert response.status_code == 404

            """Can't update not self post"""
            response = await ac.put(
                "api/v1/posts/3/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
                json={
                    "title": "Bad New Updated Post",
                    "text": "Bad New Text",
                },
            )
            assert response.status_code == 400

            """Can't delete not self post"""
            response = await ac.delete(
                "api/v1/posts/3/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
            )
            assert response.status_code == 400

            """Success deleting post"""
            response = await ac.delete(
                "api/v1/posts/3/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
            )
            assert response.status_code == 200

            """Post not found for deleting"""
            response = await ac.delete(
                "api/v1/posts/3/",
                headers={"Authorization": f"Bearer {self.user_access_token_2}"},
            )
            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_by_id_bad(self):
        async with self.client as ac:

            """Post with this id not found"""
            response = await ac.get(
                "api/v1/posts/200/",
            )
            assert response.status_code == 404
