# BUG-001 - disks 表不存在导致磁盘分析 Tab 崩溃

> 状态: resolved
> 发现日期: 2026-06-14
> 修复日期: 2026-06-14
> 严重级别: P0
> 报告人: Claude Code 调查

---

## 触发条件（复现步骤）

1. 启动 `dashboard.py`
2. 点击 Tab 3（磁盘分析）
3. 查询 `SELECT COUNT(*) FROM disks` 时报错

## 预期行为

- 磁盘分析 Tab 正常显示磁盘概览

## 实际行为

```
sqlite3.OperationalError: no such table: disks
```

## 影响范围

- 受影响表: `disks`、`software`、`digital_assets`、`health_scores`、`backup_history`、`knowledge_stats`、`project_assets`、`prompt_assets` — 新库仅含 `files` + `sqlite_sequence`
- 受影响 Tab: Tab 2 (软件)、Tab 3 (磁盘)、Tab 5 (数字资产)、Tab 0 (健康评分)
- 是否阻断: ✅ 是 — 多 Tab 不可用

---

## 数据库对比（2026-06-14）

| 维度 | 旧库（完整） | 新库（残缺） |
|------|-------------|-------------|
| 路径 | `E:\创业项目\GraceOS\09_Database\graceos.db` | `E:\知识库obsidian\02_Projects\graceos\09_Database\graceos.db` |
| 大小 | 312 MB | 365 MB |
| 表数 | 11 | 2 |
| 包含表 | files, disks, software, digital_assets, health_scores, backup_history, knowledge_stats, project_assets, prompt_assets | files (大), sqlite_sequence |

---

## 根因分析

用户手工误删除 `E:\创业项目\GraceOS` 项目目录，随后执行路径迁移将全部代码引用改为新路径 `E:\知识库obsidian\02_Projects\graceos`。但新路径下的 `09_Database/graceos.db` 是一个不完整的数据库（仅含 `files` 表，365MB），由某次孤立文件扫描生成，缺少 `disks`、`software`、`digital_assets`、`health_scores` 等核心业务表。

## 修复方案

用户手工将旧路径的完整数据库 (`E:\创业项目\GraceOS\09_Database\graceos.db`, 312MB, 11 表) 恢复到新路径 `E:\知识库obsidian\02_Projects\graceos\09_Database\graceos.db`，覆盖残缺库。

## 修复 commit

- 无代码变更（数据恢复，非代码修复）

## 验证方法

1. ✅ 连接目标 DB，执行 `.tables` 确认 11 张表全部存在
2. ✅ 启动 dashboard.py，遍历 7 个 Tab 无报错
3. ✅ 磁盘分析 Tab 显示 C/D/E 盘数据

---

## 生命周期

| 日期 | 状态变更 | 备注 |
|------|----------|------|
| 2026-06-14 | 创建 (active) | 路径迁移后发现 DB 不完整 |
| 2026-06-14 | active → resolved | 用户手工恢复完整数据库，系统验证通过 |
