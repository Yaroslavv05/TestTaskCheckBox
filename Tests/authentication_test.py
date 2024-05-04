import pytest
from main import app
from httpx import AsyncClient, ASGITransport

@pytest.mark.asyncio
async def test_registration_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000") as client:
        registration_response = await client.post("/register", json={"name": "Test User", "username": "TestUser2", "password": "password123"})
        assert registration_response.status_code == 200

        duplicate_registration_response = await client.post("/register", json={"name": "Test User 2", "username": "TestUser2", "password": "password456"})
        assert duplicate_registration_response.status_code == 401
        
        login_response = await client.post("/token", data={"username": "TestUser2", "password": "password123"})
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

