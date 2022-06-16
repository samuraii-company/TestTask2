import pytest
from httpx import AsyncClient
from database.test_db import app


class TestRegister:
    def setup(self):
        self.client = AsyncClient(app=app, base_url="http://test")
        self.user_data = {
            "email": "test2@gmail.com",
            "password": "secretpassword",
            "password2": "secretpassword",
        }
        self.user_data_2 = {
            "email": "test3@gmail.com",
            "password": "secretpassword",
            "password2": "secretpassword",
        }
        self.user_data_3 = {
            "email": "test3@gmail.com",
            "password": "secretpassword",
            "password2": "secretpassword2",
        }

        self.user_data_4 = {
            "email": "test5@gmail.com",
            "password": "hehe",
            "password2": "hehe",
        }

    @pytest.mark.asyncio
    async def test_register(self):

        async with self.client as ac:

            """Success Register"""
            response = await ac.post("/register", json=self.user_data)
            assert response.status_code == 201

            """User with this email already exist"""
            response = await ac.post("/register", json=self.user_data)
            assert response.status_code == 400

            """Passwords don't match"""
            response = await ac.post("/register", json=self.user_data_3)
            assert response.status_code == 400

            """Password length lower than 9 symbols"""
            response = await ac.post("/register", json=self.user_data_4)
            assert response.status_code == 400
