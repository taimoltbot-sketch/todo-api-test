# Todo API

使用 [agentic-workflow-template](https://github.com/taimoltbot-sketch/agentic-workflow-template) 產生的 Todo API。

## 📊 CI Status

![CI](https://github.com/taimoltbot-sketch/todo-api-test/actions/workflows/ci.yml/badge.svg)

## 🎯 這個專案示範了什麼

這是一個測試 agentic-workflow-template 的範例專案，展示了以下 skills 的產出：

| 檔案 | 來源 Skill | 說明 |
|------|------------|------|
| `RFC-001-todo-api.md` | `/planner` | 需求規格文件 |
| `todo-erd.md` | `/diagram` | ERD 圖表 |
| `tests/test_todos.py` | `/tdd` | 12 個測試案例 |
| `verify-steps.md` | `/verify` | 6 階段驗證說明 |
| `db-optimization.md` | `/db-optimize` | 索引策略建議 |
| `EVALUATION.md` | - | 整體評價報告 |

## 🚀 快速開始

```bash
# 安裝 uv (如果還沒有)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安裝依賴
uv sync --all-extras

# 跑測試
uv run pytest -v

# 啟動 server
uv run uvicorn app.main:app --reload
```

## 📝 API Endpoints

| Method | Endpoint | 說明 |
|--------|----------|------|
| POST | `/todos` | 建立待辦事項 |
| GET | `/todos` | 列出所有待辦事項 |
| PATCH | `/todos/{id}` | 更新待辦事項 |
| DELETE | `/todos/{id}` | 刪除待辦事項 |
| GET | `/health` | 健康檢查 |

## 🧪 測試

```bash
# 跑測試 + 覆蓋率
uv run pytest --cov=app --cov-report=html -v

# 只跑特定測試
uv run pytest tests/test_todos.py::TestTodoCreate -v
```

## 🔍 Lint & Type Check

```bash
# Lint
uv run ruff check app/ tests/

# Format
uv run ruff format app/ tests/

# Type check
uv run mypy app/
```

## 📦 CI/CD

這個專案使用 GitHub Actions 進行 CI，包含：

1. **Test & Lint** - Ruff + MyPy + Pytest
2. **Security Scan** - Bandit + pip-audit
3. **Build Check** - 確認可以正常 import

## 📄 License

MIT
