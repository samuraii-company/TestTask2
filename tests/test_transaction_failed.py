import pytest

from database.test_db import override_get_db

from comments.services import create_comment
from comments.schemas import Comment


class TestCommentTransaction:
    @pytest.mark.asyncio
    async def test_falied_transaction_create(self):
        with pytest.raises(Exception):

            """Can't add comment on this post, transaction error, rollback"""
            database = next(override_get_db())
            comment = Comment(text="Test", post=12)

            await create_comment(comment, database, 12)
