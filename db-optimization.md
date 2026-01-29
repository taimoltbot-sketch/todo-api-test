# Todo API - Database Optimization Report

根據 `database-optimizer` skill 的分析建議。

---

## 🔍 Analysis Summary

| 項目 | 說明 |
|------|------|
| Table | `todos` |
| 預期資料量 | 小型應用：< 10,000 筆 |
| 主要查詢模式 | 列出全部、按 ID 查詢 |

---

## 📊 索引策略

### 現有索引

```sql
-- Primary Key 自動建立
PRIMARY KEY (id)  -- B-tree index
```

### 建議新增索引

#### 1. completed 狀態索引（如果需要過濾功能）

```sql
-- 如果經常查詢 "未完成的待辦事項"
CREATE INDEX idx_todos_completed ON todos (completed);

-- 更好的方式：Partial Index（只索引 active 任務）
CREATE INDEX idx_todos_pending ON todos (created_at DESC) 
WHERE completed = false;
```

**適用場景：**
```sql
SELECT * FROM todos WHERE completed = false ORDER BY created_at DESC;
```

#### 2. 時間排序索引

```sql
-- 如果按建立時間排序很頻繁
CREATE INDEX idx_todos_created_at ON todos (created_at DESC);
```

#### 3. 複合索引（未來擴展用）

```sql
-- 如果加入 user_id
CREATE INDEX idx_todos_user_completed ON todos (user_id, completed);
```

---

## 🚀 查詢優化建議

### ✅ 好的做法

```sql
-- 使用 Index Scan
SELECT id, title, completed FROM todos WHERE id = 1;

-- 使用 LIMIT 避免全表掃描
SELECT * FROM todos ORDER BY created_at DESC LIMIT 50;
```

### ❌ 避免的做法

```sql
-- 避免 SELECT * 取不需要的欄位
SELECT * FROM todos;  -- 改為 SELECT id, title, completed

-- 避免在 WHERE 中使用函式
SELECT * FROM todos WHERE DATE(created_at) = '2025-01-29';
-- 改為範圍查詢
SELECT * FROM todos 
WHERE created_at >= '2025-01-29' AND created_at < '2025-01-30';
```

---

## 💾 快取策略

對於 Todo API 這種小型應用，簡單的策略：

### Cache-Aside Pattern

```python
async def get_todos() -> list[Todo]:
    # 1. 檢查 cache
    cached = await redis.get("todos:all")
    if cached:
        return json.loads(cached)
    
    # 2. 查詢資料庫
    todos = await db.query(Todo).all()
    
    # 3. 寫入 cache (TTL 60 秒)
    await redis.set("todos:all", json.dumps(todos), ex=60)
    
    return todos
```

### Cache Invalidation

```python
# 建立/更新/刪除時清除 cache
async def invalidate_todos_cache():
    await redis.delete("todos:all")
```

---

## 📈 效能監控

### 關鍵指標

| 指標 | 目標值 | 說明 |
|------|--------|------|
| 平均查詢時間 | < 10ms | GET /todos 應該很快 |
| 索引使用率 | > 95% | 避免 Sequential Scan |
| 連線池使用率 | < 80% | 避免連線耗盡 |

### 監控查詢

```sql
-- PostgreSQL: 查看最慢的查詢
SELECT query, calls, total_time / calls as avg_time_ms
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 5;
```

---

## 📝 總結

對於這個簡單的 Todo API：

1. **Primary Key 足夠** - `id` 的 B-tree 索引能處理大部分查詢
2. **暫不需要額外索引** - 資料量小時，全表掃描也很快
3. **未來擴展時再加** - 當資料量增長或加入 user_id 時再優化
4. **考慮 Redis 快取** - 如果讀取頻繁，可加入簡單快取

**最佳實踐：先做對，再做快。過早優化是萬惡之源。** 🎯
