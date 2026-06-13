# Root Cause Analysis - P0 系统级异常

**日期**: 2026-06-13
**问题**: 重复文件中心 / 文件搜索 / Top100大文件 全部异常

---

## 1. 根因

**`st.checkbox("", ...)` — Streamlit 空 label 警告导致渲染中断**

所有 4 个使用 checkbox 的模块（重复文件、Top100 大文件、长期未使用文件、多版本软件）中，`c1.checkbox("", ...)` 传入了空字符串 label。

Streamlit 对空 label 产生 Warning，在循环渲染大批量行时导致大量异常警告，中断了正常页面渲染。

受影响位置（dashboard.py）：
- Line 176: `st.session_state[key] = c1.checkbox("", ...)`  (重复文件)
- Top100 大文件 section
- 长期未使用文件 section  
- 多版本软件 section

## 2. 影响范围

所有使用 `st.checkbox("", ...)` 的模块——即**全部**含复选框的表格模块：

| 模块 | Tab | 影响 |
|------|-----|------|
| 重复文件中心 | 文件 Tab | ✅ 修复 |
| Top100 大文件 | 文件 Tab | ✅ 修复 |
| 长期未使用文件 | 文件 Tab | ✅ 修复 |
| 多版本软件 | 软件 Tab | ✅ 修复 |

## 3. 涉及页面

- Tab 1: 文件中心（文件搜索不受影响，因未使用 checkbox）
- Tab 2: 软件中心（多版本软件受 checkbox 影响）

## 4. 修复方案

将所有 `checkbox("", key=...)` 替换为 `checkbox("☐", key=...)`——用非空 label `☐` 替代空字符串，同时保留 `label_visibility="collapsed"` 隐藏 label。

```diff
- c1.checkbox("", key=f"dup_cb_{i}", value=..., label_visibility="collapsed")
+ c1.checkbox("☐", key=f"dup_cb_{i}", value=..., label_visibility="collapsed")
```

## 5. 验证结果

- ✅ `py_compile` 编译通过
- ✅ Streamlit 启动无 Warning 堆栈
- ✅ Playwright 截图确认文件 Tab 完整渲染（文件搜索/重复文件/Top100/未使用文件全部正常）
- ✅ 8 项 checkbox 正常显示