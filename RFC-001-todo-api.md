# RFC-001: Todo API

## Status

- [x] Draft
- [ ] Review
- [ ] Approved
- [ ] Implemented

**Author:** Template Tester (AI)
**Created:** 2025-01-29
**Updated:** 2025-01-29

---

## 1. 背景 (Context)

### 問題描述
需要一個簡單的待辦事項 API 來管理使用者的任務清單。這是測試 agentic-workflow-template 流程的範例專案。

### 相關資料
- 測試任務：驗證 template skills 的可用性

---

## 2. 目標 (Goals)

### 必須達成 (Must Have)
- [x] POST /todos - 建立待辦事項
- [x] GET /todos - 列出所有待辦事項
- [x] PATCH /todos/:id - 更新待辦事項
- [x] DELETE /todos/:id - 刪除待辦事項

### 最好能有 (Should Have)
- [ ] 分頁功能
- [ ] 過濾 (completed/pending)

### 明確排除 (Out of Scope)
- 使用者認證系統
- 多使用者隔離
- 檔案附件

---

## 3. 使用者故事 (User Stories)

### Story 1: 建立待辦事項
**As a** 使用者
**I want** 建立一個新的待辦事項
**So that** 我可以記錄要做的事

**Acceptance Criteria:**
- Given 使用者發送 POST 請求帶有 title
- When API 收到請求
- Then 回傳 201 與新建立的 todo 物件

### Story 2: 查看所有待辦事項
**As a** 使用者
**I want** 列出所有待辦事項
**So that** 我可以查看我的任務清單

---

## 4. 技術方案 (Technical Design)

### 4.1 API 設計

#### POST /todos - 建立
```
POST /todos
Content-Type: application/json

Request:
{
  "title": "買牛奶",
  "description": "去超市買"
}

Response (201):
{
  "id": 1,
  "title": "買牛奶",
  "description": "去超市買",
  "completed": false,
  "created_at": "2025-01-29T12:00:00Z"
}
```

#### GET /todos - 列出
```
GET /todos

Response (200):
[
  {
    "id": 1,
    "title": "買牛奶",
    "completed": false
  }
]
```

#### PATCH /todos/:id - 更新
```
PATCH /todos/1
Content-Type: application/json

Request:
{
  "completed": true
}

Response (200):
{
  "id": 1,
  "title": "買牛奶",
  "completed": true
}
```

#### DELETE /todos/:id - 刪除
```
DELETE /todos/1

Response (204): No Content
```

### 4.2 資料庫設計

```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 5. 原子任務清單

- [ ] `[DB]` 建立 todos migration
- [ ] `[Backend]` 建立 Todo model
- [ ] `[Backend]` 實作 POST /todos endpoint
- [ ] `[Backend]` 實作 GET /todos endpoint
- [ ] `[Backend]` 實作 PATCH /todos/:id endpoint
- [ ] `[Backend]` 實作 DELETE /todos/:id endpoint
- [ ] `[Test]` 撰寫 API 單元測試

---

## 變更紀錄 (Changelog)

| 日期 | 作者 | 變更內容 |
|------|------|----------|
| 2025-01-29 | Tester | 初始版本 |
