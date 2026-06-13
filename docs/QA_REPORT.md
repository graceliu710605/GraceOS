# GraceOS QA 测试报告

> 日期: 2026-06-13 | 版本: V2.2-stable
> 按 DEVELOPMENT_RULES.md 规范生成
> Sanity Test run via automated DB query checks

## Sanity Test 结果

| # | 模块 | 数据 | 耗时 | 结果 |
|---|------|------|------|------|
| 1 | Tab 0 Home - Health score | 26/100 | 7.5s | PASS |
| 2 | Tab 1 Files - Stats | 1,155,164 files / 154,048 dup groups | 0.5s | PASS |
| 3 | Tab 1 Files - Dup query | 5 groups (test) | 4.0s | PASS |
| 4 | Tab 1 Files - Top100 | 100 rows / 59 live on disk | <0.1s | PASS |
| 5 | Tab 1 Files - Unused | 100 rows / 69 live on disk | <0.1s | PASS |
| 6 | Tab 2 Software - Count | 142 total | <0.1s | PASS |
| 7 | Tab 2 Software - Multi-ver | 17 dup | <0.1s | PASS |
| 8 | Tab 3 Disks - Overview | 3 disks | <0.1s | PASS |
| 9 | Tab 5 Assets - Digital | 23 items | <0.1s | PASS |
| 10 | Indexes | 3 (name+size, last_modified, size) | - | PASS |
| 11 | dashboard.py AST | 613 lines | - | PASS |

**11/11 PASS**

## HTTP Smoke Test

| 检查项 | 结果 |
|--------|------|
| Streamlit 启动 | PASS |
| Port 8520 LISTENING | PASS |
| HTTP 200 | PASS |
| Page content > 0 | PASS (1522 bytes) |
| No error/traceback in page | PASS |

## 本轮修复验证

| 修复项 | 验证方式 | 结果 |
|--------|----------|------|
| 删除后 DB 记录同步清除 | _safe_delete(fp, conn) 传入 conn | PASS |
| 0-byte 文件过滤 | file_size > 0 in all 4 queries | PASS |
| 过时文件过滤 | df[...exists(p)] post-filter in all tables | PASS |
| 空 DataFrame 后保护 | double if not empty guard | PASS |
| 批量删除按钮始终可见 | to_del=[] else 分支 + button disabled | PASS |
| 文件搜索目录列 | h4='所在目录' + os.path.dirname | PASS |
| 重复文件日期列 | del_date from MAX(last_modified) | PASS |
| 健康评分缓存 | session_state.cached_score | PASS |
| 存储扫描缓存 | session_state.cached_storage | PASS |
| 软件搜索安装日期列 | 替换空"建议"列为 install_date | PASS |
| 多版本卸载确认 | button text shows software names | PASS |
| 最早安装软件排序 + 启动 | radio toggle + launch button + path | PASS |
