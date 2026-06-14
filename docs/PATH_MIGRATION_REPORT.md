# 路径迁移报告

> **日期**: 2026-06-14
> **触发原因**: 用户手工删除旧项目目录 `E:\创业项目\GraceOS`，全局替换为新路径
> **类型**: 配置变更 / 路径迁移

---

## 变更概览

| 项目 | 旧值 | 新值 |
|------|------|------|
| 项目根目录 | `E:\创业项目\GraceOS` | `E:\知识库obsidian\02_Projects\graceos` |
| 组织规则目录 | `E:\创业项目\00_AI组织` | `E:\知识库obsidian\02_Projects\graceos\00_AI组织` |
| STORAGE_DIRS Projects | `E:/创业项目` | `E:/知识库obsidian/02_Projects/graceos` |
| 数据库位置 | `E:\创业项目\GraceOS\09_Database\graceos.db` | `E:\知识库obsidian\02_Projects\graceos\09_Database\graceos.db` |

---

## 修改清单（27 个文件）

### 1. 核心配置
| 文件 | 修改点 |
|------|--------|
| `config/pyths.py` | `PROJECT_ROOT` |

### 2. Dashboard
| 文件 | 修改点 |
|------|--------|
| `dashboard.py` | `DB_FILE` + `STORAGE_DIRS` (第21行 Projects) |

### 3. Analyzers
| 文件 | 修改点 |
|------|--------|
| `analyzers/health_scorer.py` | `DB_FILE` |
| `analyzers/software_search.py` | JSON 路径 |

### 4. Scanners
| 文件 | 修改点 |
|------|--------|
| `scanners/file_scanner.py` | `OUTPUT_FILE` |
| `scanners/disk_scanner.py` | `output_dir` |
| `scanners/software_scanner.py` | `output_dir` |

### 5. 根目录导入器
| 文件 | 修改点 |
|------|--------|
| `json_to_sqlite.py` | `JSON_FILE` + `DB_FILE` |
| `json_to_sqlite_v1.py` | `JSON_FILE` + `DB_FILE` |
| `json_to_sqlite_smoke_test.py` | `JSON_FILE` + `DB_FILE` |
| `software_to_sqlite.py` | `JSON_FILE` + `DB_FILE` |
| `disk_to_sqlite.py` | `JSON_FILE` + `DB_FILE` |
| `dashboard_v1_backup.py` | `DB_FILE` |

### 6. Setup Build 打包套件
| 文件 | 修改点 |
|------|--------|
| `setup_build/app/dashboard.py` | `DB_FILE` + `STORAGE_DIRS` |
| `setup_build/app/json_to_sqlite.py` | `JSON_FILE` + `DB_FILE` |
| `setup_build/app/software_to_sqlite.py` | `JSON_FILE` + `DB_FILE` |
| `setup_build/app/disk_to_sqlite.py` | `JSON_FILE` + `DB_FILE` |
| `setup_build/app/analyzers/health_scorer.py` | `DB_FILE` |
| `setup_build/app/analyzers/software_search.py` | JSON 路径 |
| `setup_build/app/scanners/file_scanner.py` | `OUTPUT_FILE` |
| `setup_build/app/scanners/disk_scanner.py` | `output_dir` |
| `setup_build/app/scanners/software_scanner.py` | `output_dir` |

### 7. Markdown 文档
| 文件 | 修改点 |
|------|--------|
| `PROJECT_HANDOVER.md` | 数据库位置 + 组织规范路径（3处） |
| `PROJECT_STATUS.md` | 组织规则路径 |
| `PROJECT_OPERATING_RULES.md` | 组织规则路径 |
| `DEVELOPMENT_RULES.md` | 白名单目录 |

---

## 验证结果

```
grep "创业项目" -- **/*.py → 0 matches ✅
grep "创业项目" -- **/*.md → 0 matches ✅
```

### dashboard.py DB_FILE 确认

```python
# 第24行
DB_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\graceos.db"
```

---

## 影响范围

- **无功能变更** — 纯路径替换，不改变任何业务逻辑
- **无数据库结构变更** — 仅变更引用路径，数据库文件本身不变
- **默认复用已有数据库** — 新路径 `09_Database/` 目录已存在
