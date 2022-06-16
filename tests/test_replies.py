import pytest
from httpx import AsyncClient
from database.test_db import app
from auth.jwt import create_access_token
from database.test_db import app, override_get_db

from users.models import Users
from posts.models import Posts
from comments.models import Comments


class TestReplies:
    def setup(self):
        self.client = AsyncClient(app=app, base_url="http://test")
        self.database = next(override_get_db())
        self.new_user = Users(email="test4@gmail.com", password="password")
        self.post = Posts(text="Test", author=self.new_user.id)
        self.comment = Comments(text="Test", post=self.post.id, author=self.new_user.id)

        self.database.add(self.new_user)
        self.database.add(self.post)
        self.database.add(self.comment)
        self.database.commit()
        self.database.refresh(self.new_user)
        self.database.refresh(self.post)
        self.database.refresh(self.comment)
        self.user_access_token = create_access_token(
            {"sub": self.new_user.email, "id": self.new_user.id}
        )

    @pytest.mark.asyncio
    async def test_replies(self):
        async with self.client as ac:

            """Success Replies for comment"""
            response = await ac.post(
                "api/v1/comments/replies/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
                json={"text": "New replies", "comment": self.comment.id},
            )
            assert response.status_code == 201

            """Comment not found for replies"""
            response = await ac.post(
                "api/v1/comments/replies/",
                headers={"Authorization": f"Bearer {self.user_access_token}"},
                json={"text": "New replies", "comment": 20},
            )
            assert response.status_code == 404
