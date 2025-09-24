import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import Base, engine

# ---------------- Setup temporary test DB ----------------
@pytest.fixture(scope="module")
def setup_db():
    # Create tables before tests
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)

# ---------------- Test register, login, and tasks ----------------
@pytest.mark.asyncio
async def test_register_and_get_tasks(setup_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # -------- Register user --------
        response = await client.post("/auth/register", json={"username": "testuser", "password": "testpass"})
        assert response.status_code == 200
        user = response.json()
        assert user["username"] == "testuser"

        # -------- Login to get JWT token --------
        response = await client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # -------- Create a task --------
        response = await client.post("/tasks/", json={"title": "Test Task", "description": "Desc"}, headers=headers)
        assert response.status_code == 200
        task = response.json()
        assert task["title"] == "Test Task"

        # -------- Get tasks --------
        response = await client.get("/tasks/", headers=headers)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Test Task"
