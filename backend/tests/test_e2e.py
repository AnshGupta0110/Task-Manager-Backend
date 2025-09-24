import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db import Base, engine

@pytest.fixture(scope="module")
def setup_db():
    # Setup DB tables before tests
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_e2e_task_flow(setup_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        
        # 1️ Register user
        register_resp = await client.post("/auth/register", json={
            "username": "e2euser",
            "password": "testpass"
        })
        assert register_resp.status_code == 200
        user = register_resp.json()
        assert user["username"] == "e2euser"

        # 2️ Login user to get JWT token
        login_resp = await client.post("/auth/login", json={
            "username": "e2euser",
            "password": "testpass"
        })
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3️ Create a task
        task_resp = await client.post("/tasks/", json={
            "title": "E2E Task",
            "description": "E2E Test Description"
        }, headers=headers)
        assert task_resp.status_code == 200
        task = task_resp.json()
        assert task["title"] == "E2E Task"
        assert task["completed"] is False

        # 4️ Mark task as completed
        complete_resp = await client.put(f"/tasks/{task['id']}/complete", headers=headers)
        assert complete_resp.status_code == 200
        updated_task = complete_resp.json()
        assert updated_task["completed"] is True

        # 5️ Get all tasks for the user
        tasks_resp = await client.get("/tasks/", headers=headers)
        assert tasks_resp.status_code == 200
        tasks = tasks_resp.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "E2E Task"
        assert tasks[0]["completed"] is True

        # 6️ Delete the task
        delete_resp = await client.delete(f"/tasks/{task['id']}", headers=headers)
        assert delete_resp.status_code == 200

        # 7️ Confirm tasks list is empty
        final_resp = await client.get("/tasks/", headers=headers)
        assert final_resp.status_code == 200
        assert final_resp.json() == []
