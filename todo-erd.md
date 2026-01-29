# Todo API - ERD (Entity Relationship Diagram)

根據 `mermaid-expert` skill 產出的資料庫模型圖。

## ERD 圖表

```mermaid
erDiagram
    TODO {
        int id PK "Primary Key, auto increment"
        string title "Required, max 255 chars"
        text description "Optional, detailed info"
        boolean completed "Default: false"
        timestamp created_at "Auto set on create"
        timestamp updated_at "Auto update on change"
    }
```

## 說明

- **TODO** 是唯一的實體
- `id`: 自動遞增的主鍵
- `title`: 必填欄位，待辦事項標題
- `description`: 選填欄位，詳細描述
- `completed`: 布林值，預設為 false
- `created_at` / `updated_at`: 自動管理的時間戳記

## 未來擴展 (如果加入使用者系統)

```mermaid
erDiagram
    USER ||--o{ TODO : owns
    USER {
        uuid id PK
        string email UK
        string name
        timestamp created_at
    }
    TODO {
        int id PK
        uuid user_id FK
        string title
        text description
        boolean completed
        timestamp created_at
        timestamp updated_at
    }
```

## 渲染方式

- GitHub/GitLab Markdown 原生支援
- [Mermaid Live Editor](https://mermaid.live)
- VS Code + Markdown Preview Mermaid 擴充
