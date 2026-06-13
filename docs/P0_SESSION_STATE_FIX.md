# P0 RuntimeError Fix - Session State

**日期**: 2026-06-13

---

## 错误
`RuntimeError: dictionary changed size during iteration`

## 根因
重复文件 154,048 组全部渲染，每行 6 个 st.columns + checkbox + button，产生 ~92 万 widget，Streamlit 内部 session_state 在遍历时发生字典修改冲突。

## 修复
- 重复文件增加硬分页：**每页 50 组**
- 仅渲染当前页的 50 行，session_state 操作范围缩小
- 所有 `df_dup` 引用改为 `df_dup_page`

## 验证
- ✅ 编译通过
- ✅ Playwright 截图确认页面正常渲染
- ✅ 分页控件显示正常
- ✅ 首页/文件搜索/重复文件/Top100/未使用/软件/磁盘 全部可进入