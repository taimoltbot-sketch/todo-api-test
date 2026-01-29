"""
Todo API 測試案例
================
根據 TDD skill 的 Red-Green-Refactor 流程
目前狀態：🔴 RED (測試先行，實作尚未完成)
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestTodoCreate:
    """POST /todos - 建立待辦事項"""

    async def test_creates_todo_with_valid_title(self, client: AsyncClient):
        """應該成功建立待辦事項當提供有效的 title"""
        response = await client.post("/todos", json={
            "title": "買牛奶"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "買牛奶"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    async def test_creates_todo_with_description(self, client: AsyncClient):
        """應該成功建立待辦事項帶有 description"""
        response = await client.post("/todos", json={
            "title": "買牛奶",
            "description": "去全聯買兩瓶"
        })
        assert response.status_code == 201
        assert response.json()["description"] == "去全聯買兩瓶"

    async def test_returns_422_when_title_missing(self, client: AsyncClient):
        """應該回傳 422 當缺少 title"""
        response = await client.post("/todos", json={})
        assert response.status_code == 422

    async def test_returns_422_when_title_empty(self, client: AsyncClient):
        """應該回傳 422 當 title 為空字串"""
        response = await client.post("/todos", json={
            "title": ""
        })
        assert response.status_code == 422


@pytest.mark.asyncio
class TestTodoList:
    """GET /todos - 列出所有待辦事項"""

    async def test_returns_empty_list_when_no_todos(self, client: AsyncClient):
        """應該回傳空陣列當沒有待辦事項"""
        response = await client.get("/todos")
        assert response.status_code == 200
        assert response.json() == []

    async def test_returns_all_todos(self, client: AsyncClient):
        """應該回傳所有待辦事項"""
        # Arrange: 先建立幾個 todo
        await client.post("/todos", json={"title": "Task 1"})
        await client.post("/todos", json={"title": "Task 2"})
        
        # Act
        response = await client.get("/todos")
        
        # Assert
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) == 2
        assert todos[0]["title"] == "Task 1"
        assert todos[1]["title"] == "Task 2"


@pytest.mark.asyncio
class TestTodoUpdate:
    """PATCH /todos/:id - 更新待辦事項"""

    async def test_updates_todo_completed_status(self, client: AsyncClient):
        """應該成功更新 completed 狀態"""
        # Arrange
        create_resp = await client.post("/todos", json={"title": "Test"})
        todo_id = create_resp.json()["id"]
        
        # Act
        response = await client.patch(f"/todos/{todo_id}", json={
            "completed": True
        })
        
        # Assert
        assert response.status_code == 200
        assert response.json()["completed"] is True

    async def test_updates_todo_title(self, client: AsyncClient):
        """應該成功更新 title"""
        create_resp = await client.post("/todos", json={"title": "Old Title"})
        todo_id = create_resp.json()["id"]
        
        response = await client.patch(f"/todos/{todo_id}", json={
            "title": "New Title"
        })
        
        assert response.status_code == 200
        assert response.json()["title"] == "New Title"

    async def test_returns_404_when_todo_not_found(self, client: AsyncClient):
        """應該回傳 404 當待辦事項不存在"""
        response = await client.patch("/todos/99999", json={
            "completed": True
        })
        assert response.status_code == 404


@pytest.mark.asyncio
class TestTodoDelete:
    """DELETE /todos/:id - 刪除待辦事項"""

    async def test_deletes_todo_successfully(self, client: AsyncClient):
        """應該成功刪除待辦事項"""
        # Arrange
        create_resp = await client.post("/todos", json={"title": "To Delete"})
        todo_id = create_resp.json()["id"]
        
        # Act
        response = await client.delete(f"/todos/{todo_id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verify it's deleted
        get_resp = await client.get("/todos")
        assert all(t["id"] != todo_id for t in get_resp.json())

    async def test_returns_404_when_todo_not_found(self, client: AsyncClient):
        """應該回傳 404 當待辦事項不存在"""
        response = await client.delete("/todos/99999")
        assert response.status_code == 404


# --- Fixtures (conftest.py 內容示意) ---

# @pytest.fixture
# async def client():
#     """建立測試用的 HTTP client"""
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac
#
# @pytest.fixture(autouse=True)
# async def clean_database():
#     """每個測試前清空資料庫"""
#     await db.execute("TRUNCATE todos RESTART IDENTITY")
#     yield
