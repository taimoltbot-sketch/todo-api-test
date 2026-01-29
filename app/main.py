"""
Todo API - FastAPI 實作
根據 TDD skill 的 Green 階段
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Todo API",
    description="使用 agentic-workflow-template 產生的 Todo API",
    version="1.0.0"
)

# --- In-memory Database ---
todos_db: dict[UUID, dict] = {}


# --- Schemas ---
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime


# --- Endpoints ---
@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate) -> TodoResponse:
    """建立待辦事項"""
    todo_id = uuid4()
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "created_at": datetime.now()
    }
    todos_db[todo_id] = new_todo
    return TodoResponse(**new_todo)


@app.get("/todos", response_model=list[TodoResponse])
async def list_todos() -> list[TodoResponse]:
    """列出所有待辦事項"""
    return [TodoResponse(**todo) for todo in todos_db.values()]


@app.patch("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: UUID, update: TodoUpdate) -> TodoResponse:
    """更新待辦事項"""
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    todo = todos_db[todo_id]
    if update.title is not None:
        todo["title"] = update.title
    if update.description is not None:
        todo["description"] = update.description
    if update.completed is not None:
        todo["completed"] = update.completed
    
    return TodoResponse(**todo)


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID) -> None:
    """刪除待辦事項"""
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    del todos_db[todo_id]


@app.get("/health")
async def health_check():
    """健康檢查"""
    return {"status": "healthy"}
