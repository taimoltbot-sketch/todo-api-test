# Verification Steps for Todo API

根據 `verify` skill 的 6 階段驗證流程。

---

## 驗證流程

### Phase 1: Build Verification 🏗️

```bash
# Python 專案
uv run python -m py_compile app/**/*.py 2>&1

# 或 Node.js 專案
npm run build 2>&1 | tail -20
```

**判定：** 如果 build 失敗，立即停止並修復。

---

### Phase 2: Type Check 📝

```bash
# Python (mypy)
uv run mypy app/ --ignore-missing-imports 2>&1 | head -30

# 或 TypeScript
npx tsc --noEmit 2>&1 | head -30
```

**判定：** 報告所有型別錯誤，Critical 必須修復。

---

### Phase 3: Lint Check 🧹

```bash
# Python
uv run ruff check app/ 2>&1 | head -30
uv run ruff format --check app/ 2>&1

# 或 TypeScript
eslint . --ext .ts 2>&1 | head -30
```

**判定：** 修復嚴重違規，警告可延後處理。

---

### Phase 4: Test Suite 🧪

```bash
# Python
uv run pytest tests/test_todos.py --cov=app --cov-report=term-missing --cov-fail-under=80 2>&1 | tail -50

# 或 Node.js
npm test -- --coverage 2>&1 | tail -50
```

**Coverage 要求：**
- 最低: 80%
- 目標: 90%+

---

### Phase 5: Security Scan 🔐

```bash
# 檢查硬編碼 secrets
grep -rn "sk-\|api_key\|password\s*=" --include="*.py" app/ 2>/dev/null | head -10

# 檢查 debug 程式碼
grep -rn "print(" --include="*.py" app/ 2>/dev/null | grep -v __pycache__ | head -10

# Python 安全掃描
bandit -r app/ -f json 2>/dev/null | jq '.results | length'
```

**針對 Todo API 的安全檢查：**
- [ ] SQL Injection 防護（使用 ORM 參數化查詢）
- [ ] 輸入驗證（title 長度限制）
- [ ] ID 參數驗證（避免非法 ID）

---

### Phase 6: Diff Review 📋

```bash
# 變更統計
git diff --stat

# 變更的檔案
git diff HEAD --name-only
```

**Review 重點：**
- 是否有非預期的變更？
- API endpoint 是否符合 RFC 規格？
- 錯誤處理是否完整？

---

## 預期輸出報告

```
╔══════════════════════════════════════════╗
║         VERIFICATION REPORT              ║
╠══════════════════════════════════════════╣
║ Build:     ✅ PASS                       ║
║ Types:     ✅ PASS (0 errors)            ║
║ Lint:      ✅ PASS (0 warnings)          ║
║ Tests:     ✅ PASS (12/12, 95.2%)        ║
║ Security:  ✅ PASS (0 issues)            ║
║ Diff:      📝 4 files changed            ║
╠══════════════════════════════════════════╣
║ Overall:   ✅ READY for commit           ║
╚══════════════════════════════════════════╝
```

---

## 狀態定義

| 狀態 | 意義 |
|------|------|
| ✅ PASS | 完全通過 |
| ⚠️ WARN | 有警告但可接受 |
| ❌ FAIL | 失敗，必須修復 |

## 整體判定

| 條件 | 結果 |
|------|------|
| 任何 ❌ FAIL | NOT READY - 不可 commit |
| 只有 ⚠️ WARN | READY (建議修復) |
| 全部 ✅ PASS | READY - 可以 commit |
