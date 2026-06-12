# GraceOS V2 数据库设计

## 设计原则

- V1 表保留不变
- 新表以 IF NOT EXISTS 增量添加
- 新表名统一：<domain>_assets 或 <domain>_<purpose>

## V2 新增表

### 1. health_scores（健康评分历史）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增 |
| score_date | TEXT | 日期 YYYY-MM-DD |
| total_score | INTEGER | 综合评分 0-100 |
| file_dup_score | INTEGER | 重复文件维度 |
| file_unused_score | INTEGER | 未使用文件维度 |
| disk_score | INTEGER | 磁盘空间维度 |
| sw_score | INTEGER | 软件健康维度 |
| dup_count | INTEGER | 重复文件组数 |
| dup_files | INTEGER | 重复文件总数 |
| dup_size_mb | REAL | 重复占用(MB) |
| unused_count | INTEGER | 未使用文件数 |
| unused_size_mb | REAL | 未使用占用(MB) |
| c_usage_pct | REAL | C盘使用率 |
| sw_count | INTEGER | 软件总数 |
| sw_multi_ver | INTEGER | 多版本软件数 |
| created_at | TEXT | 创建时间 |

### 2. project_assets（项目资产）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增 |
| name | TEXT | 项目名 |
| path | TEXT | 完整路径 |
| is_git | INTEGER | 是否 Git 仓库 |
| git_branch | TEXT | 当前分支 |
| git_status | TEXT | clean/dirty/behind/ahead |
| last_commit | TEXT | 最后提交时间 |
| last_modified | TEXT | 最后修改时间 |
| size_mb | REAL | 项目大小 |
| tags | TEXT | 逗号分隔标签 |
| status | TEXT | active/archived |
| scan_time | TEXT | 扫描时间 |

### 3. prompt_assets（Prompt 资产）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增 |
| title | TEXT | 标题 |
| content | TEXT | 内容 |
| category | TEXT | 分类 |
| tags | TEXT | 标签 |
| version | INTEGER | 版本号 |
| usage_count | INTEGER | 使用次数 |
| last_used | TEXT | 最后使用 |
| rating | INTEGER | 评分 1-5 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### 4. knowledge_stats（知识库统计）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增 |
| vault_name | TEXT | 仓库名 |
| vault_path | TEXT | 路径 |
| note_count | INTEGER | 笔记数 |
| attachment_count | INTEGER | 附件数 |
| tag_count | INTEGER | 标签数 |
| size_mb | REAL | 总大小 |
| scan_time | TEXT | 扫描时间 |

### 5. backup_history（备份历史）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增 |
| backup_type | TEXT | git/sqlite/config |
| target | TEXT | 目标路径 |
| status | TEXT | success/failed |
| details | TEXT | 详细信息 |
| created_at | TEXT | 备份时间 |

## 索引策略

```sql
CREATE INDEX idx_scores_date ON health_scores(score_date);
CREATE INDEX idx_projects_status ON project_assets(status);
CREATE INDEX idx_prompts_category ON prompt_assets(category);
CREATE INDEX idx_prompts_tags ON prompt_assets(tags);
CREATE INDEX idx_backup_type ON backup_history(backup_type);
```

## 迁移方案

V1 → V2 数据库升级（增量，不删旧表）：

```sql
CREATE TABLE IF NOT EXISTS health_scores (...);
CREATE TABLE IF NOT EXISTS project_assets (...);
CREATE TABLE IF NOT EXISTS prompt_assets (...);
CREATE TABLE IF NOT EXISTS knowledge_stats (...);
CREATE TABLE IF NOT EXISTS backup_history (...);
```
