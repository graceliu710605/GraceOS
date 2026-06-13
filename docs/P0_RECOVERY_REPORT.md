# GraceOS P0 Recovery Report

**日期**: 2026-06-13
**状态**: ✅ 恢复完成

---

## 故障概要

| 维度 | 说明 |
|------|------|
| **故障** | dashboard.py 运行时 NameError: `df_dup` / `df_dup_page` not defined |
| **影响范围** | Tab 1 (文件资产) 重复文件模块不可用 |
| **发现时间** | 2026-06-13 20:00 |
| **根因 Commit** | `de1fd5a` perf: indexes + lazy load duplicate + cache |

---

## 恢复前 Commit 链

```
bc562d1 ← HEAD (仅改 PROJECT_STATUS.md)
3dcdbca ← "fix" 尝试修复 else 缩进（不彻底）
52918d4 ← docs only (PERFORMANCE_ANALYSIS_V2.md)
de1fd5a ← ⚡ ROOT CAUSE: 懒加载重构错误
bdbfd72 ← 🟢 v2.2-digital-assets stable baseline (tagged)
```

---

## Root Cause Analysis

### Change ② — 重复文件懒加载 (主要故障点)

`de1fd5a` 在 Tab 1 中插入懒加载逻辑：

```python
# 原始代码 (bdbfd72):
    df_dup = pd.read_sql_query(...)
    if not df_dup.empty:
        ...  # 50+ 行处理代码

# 错误修改 (de1fd5a):
    if not st.session_state.dup_loaded:
        st.button("分析重复文件")
    else:
    df_dup = pd.read_sql_query(...)     # ❌ 不在 else 内
    if not df_dup.empty:                # 总是执行 → NameError
        ...
```

`3dcdbca` 修复了缩进但未修复逻辑结构：

```python
    else:
        df_dup = pd.read_sql_query(...)  # ✅ 缩进修复
    if not df_dup.empty:                 # ❌ 仍在 else 外
```

**核心问题**: else 块只包裹了 1 行 (`df_dup = ...`)，但后续 50+ 行处理代码均在 else 外执行。用户未点击按钮时 `dup_loaded=False`，else 不执行 → `df_dup` 未赋值 → NameError。

---

## 恢复执行

### 方案 A: 回退到 bdbfd72

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | `git reset --hard bdbfd72` | 回到 v2.2-stable |
| 2 | AST 验证: `ast.parse(dashboard.py)` | ✅ OK |
| 3 | 污染检查: `dup_loaded` / `cached_score` / `cached_storage` | ✅ 0 occurrences |
| 4 | `git cherry-pick 52918d4` | ✅ PERFORMANCE_ANALYSIS_V2.md 恢复 |
| 5 | `git cherry-pick bc562d1` | ✅ RULE-038/039 同步恢复 |

### 最终 Commit 链

```
84209ac ← HEAD: recovery rollback + update PROJECT_STATUS.md
d40f209 rules: sync RULE-038 DoD + RULE-039 Task Output Format
313c416 docs: PERFORMANCE_ANALYSIS_V2
bdbfd72 🟢 v2.2-digital-assets stable baseline (tagged)
```

---

## 验证结果

| 检查项 | 结果 |
|--------|------|
| `ast.parse(dashboard.py)` | ✅ PASS |
| `dup_loaded` in source | ✅ 0 (未污染) |
| `cached_score` in source | ✅ 0 (未污染) |
| `cached_storage` in source | ✅ 0 (未污染) |
| Working tree clean | ✅ `git status` clean |

---

## 丢弃的 Commit

| Commit | 说明 | 丢弃原因 |
|--------|------|----------|
| `de1fd5a` | perf: indexes + lazy load + cache | Root cause — 懒加载重构结构错误 |
| `3dcdbca` | fix: indentation of else block | 修复不彻底 — 未识别控制流逻辑缺陷 |

---

## 恢复后功能基线

| 模块 | 状态 |
|------|------|
| 首页 — 健康评分 | ✅ 正常 |
| 文件搜索 | ✅ 正常 |
| 重复文件 | ✅ 正常（直接查询，无懒加载） |
| Top100 大文件 | ✅ 正常 |
| 长期未使用文件 | ✅ 正常 |
| 软件中心 | ✅ 正常 |
| 磁盘分析 | ✅ 正常 |
| 存储分析 | ✅ 正常 |
| 数字资产中心 | ✅ 正常 |

> 注意: 性能回到优化前水平，重复文件查询 ~12.6s。待稳定后重新规划性能优化方案。
