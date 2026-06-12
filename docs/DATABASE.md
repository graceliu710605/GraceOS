# GraceOS V2 数据库设计

## 概述

V2 在 V1 基础上新增 6 张业务表、2 张系统表。总表数从 3 增至 11。

## V1 现有表（保留）

### files（文件资产）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| file_name | TEXT | 文件名 |
| file_path | TEXT | 完整路径 |
| file_size | INTEGER | 字节数 |
| last_modified | TEXT | ISO 时间 |
| file_type | TEXT | 扩展名 |

### software（软件资产）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| name | TEXT | 软件名称 |
| id_name | TEXT | winget ID |
| version | TEXT | 版本号 |
| source | TEXT | 来源（winget/ARP） |
| publisher | TEXT | 发布商 |
| install_date | TEXT | 安装日期（YYYYMMDD） |
| install_path | TEXT | 安装路径 |
| size_bytes | INTEGER | 大小（字节） |
| raw | TEXT | 原始输出 |
| scan_time | TEXT | 扫描时间 |

### disks（磁盘资产）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| name | TEXT | 盘符 |
| total_gb | REAL | 总容量 |
| used_gb | REAL | 已使用 |
| free_gb | REAL | 剩余 |
| usage_pct | REAL | 使用率% |
| root | TEXT | 根路径 |
| description | TEXT | 描述 |
| scan_time | TEXT | 扫描时间 |

---

## V2 新增表

### 1. scores（健康评分）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| score_date | TEXT | 评分日期（YYYY-MM-DD） |
| total_score | INTEGER | 综合得分（0-100） |
| dup_score | INTEGER | 重复文件得分 |
| disk_score | INTEGER | 磁盘空间得分 |
| unused_score | INTEGER | 未使用文件得分 |
| sw_score | INTEGER | 软件健康得分 |
| dup_count | INTEGER | 重复文件组数 |
| dup_files | INTEGER | 重复文件总数 |
| dup_size_mb | REAL | 重复文件占用（MB） |
| c_usage_pct | REAL | C盘使用率 |
| unused_count | INTEGER | 长期未使用文件数 |
| sw_expired | INTEGER | 过期软件数 |
| sw_unknown | INTEGER | 未知发布商软件数 |
| created_at | TEXT | 创建时间 |

### 2. ai_suggestions（AI 建议）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| category | TEXT | 分类（空间/重复/归档/软件） |
| title | TEXT | 建议标题 |
| description | TEXT | 详细说明 |
| impact_mb | REAL | 预计释放空间（MB） |
| file_count | INTEGER | 涉及文件数 |
| status | TEXT | 状态（pending/accepted/dismissed/executed） |
| details_json | TEXT | 详细数据（JSON） |
| created_at | TEXT | 创建时间 |
| executed_at | TEXT | 执行时间 |

### 3. auto_rules（自动整理规则）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| name | TEXT | 规则名称 |
| source_dir | TEXT | 源目录 |
| target_dir | TEXT | 目标目录 |
| condition | TEXT | 条件（older_than_days:N / file_type:X / regex:Y） |
| enabled | INTEGER | 启用（0/1） |
| preview_mode | INTEGER | 预览模式（0/1） |
| last_run | TEXT | 上次执行时间 |
| created_at | TEXT | 创建时间 |

### 4. projects（项目管理）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| name | TEXT | 项目名称 |
| path | TEXT | 项目路径 |
| is_git_repo | INTEGER | 是否 Git 仓库 |
| git_branch | TEXT | 当前分支 |
| git_status | TEXT | Git 状态（clean/dirty/behind/ahead） |
| last_modified | TEXT | 最后修改时间 |
| size_mb | REAL | 项目大小（MB） |
| tags | TEXT | 标签（逗号分隔） |
| status | TEXT | 项目状态（active/archived） |
| scan_time | TEXT | 扫描时间 |

### 5. prompts（Prompt 资产）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| title | TEXT | Prompt 标题 |
| content | TEXT | Prompt 内容 |
| category | TEXT | 分类（coding/writing/analysis/automation） |
| tags | TEXT | 标签 |
| version | INTEGER | 版本号 |
| usage_count | INTEGER | 使用次数 |
| last_used | TEXT | 最后使用时间 |
| rating | INTEGER | 评分（1-5） |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### 6. obsidian_stats（知识库统计）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| vault_name | TEXT | 仓库名称 |
| vault_path | TEXT | 仓库路径 |
| note_count | INTEGER | 笔记总数 |
| tag_count | INTEGER | 标签总数 |
| link_count | INTEGER | 链接总数 |
| last_modified | TEXT | 最后修改时间 |
| size_mb | REAL | 总大小（MB） |
| scan_time | TEXT | 扫描时间 |

### 7. backup_logs（备份日志）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| backup_type | TEXT | 类型（git/sqlite/config） |
| target | TEXT | 备份目标 |
| file_count | INTEGER | 文件数 |
| size_mb | REAL | 大小 |
| status | TEXT | 状态（success/failed） |
| error_msg | TEXT | 错误信息 |
| created_at | TEXT | 备份时间 |

### 8. workflow_logs（工作流日志）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 自增主键 |
| workflow_name | TEXT | 工作流名称 |
| trigger | TEXT | 触发方式（manual/scheduled/webhook） |
| status | TEXT | 状态 |
| result | TEXT | 执行结果 |
| started_at | TEXT | 开始时间 |
| finished_at | TEXT | 结束时间 |

---

## 表关系

```
files ──────────────────────────────┐
software ───────────────────────────┤
disks ──────────────────────────────┤
                                    ↓
                              scores（评分引擎聚合）
                                    ↓
                           ai_suggestions（AI 分析生成）
                                    ↓
                    ┌───────────────┼───────────────┐
                    ↓               ↓               ↓
              auto_rules        backup_logs     workflow_logs

projects ─── 独立（项目管理）
prompts ──── 独立（Prompt 管理）
obsidian_stats ─ 独立（知识库）
```

## 索引策略

| 表 | 索引 |
|------|------|
| scores | score_date, total_score |
| ai_suggestions | category, status, created_at |
| auto_rules | enabled, last_run |
| projects | is_git_repo, status, last_modified |
| prompts | category, usage_count |
| backup_logs | backup_type, created_at |

## 迁移方案

从 V1 到 V2 数据库升级：

```sql
-- V2 新增表（在现有 graceos.db 中创建）
CREATE TABLE IF NOT EXISTS scores (...);
CREATE TABLE IF NOT EXISTS ai_suggestions (...);
CREATE TABLE IF NOT EXISTS auto_rules (...);
CREATE TABLE IF NOT EXISTS projects (...);
CREATE TABLE IF NOT EXISTS prompts (...);
CREATE TABLE IF NOT EXISTS obsidian_stats (...);
CREATE TABLE IF NOT EXISTS backup_logs (...);
CREATE TABLE IF NOT EXISTS workflow_logs (...);
```

**迁移策略**：增量添加，不删除 V1 表。所有新表用 IF NOT EXISTS，向前兼容。
