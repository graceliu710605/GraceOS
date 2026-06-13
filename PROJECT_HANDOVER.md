# GraceOS 项目交接文档

> **唯一入口** — 所有 Codex 会话必须先读本文档
> **最后更新**: 2026-06-13

---

## 项目概览

| 项目 | 值 |
|------|-----|
| 项目名称 | GraceOS / 个人数字资产管家 |
| 当前版本 | V2.1 |
| 产品类型 | 个人数字资产管理系统 |
| 技术栈 | Python + Streamlit + SQLite + NSIS |
| 代码位置 | `e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1` |
| 数据库位置 | `E:\创业项目\GraceOS\09_Database\graceos.db` |

## 快速启动

```powershell
cd "e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1"
streamlit run dashboard.py
```

## 核心文件

| 文件 | 用途 |
|------|------|
| `dashboard.py` | Streamlit Web 主应用 (~26KB) |
| `main.py` | CLI 扫描入口 |
| `scanners/software_scanner.py` | 软件扫描 (winget + 注册表) |
| `scanners/file_scanner.py` | 文件扫描 |
| `scanners/disk_scanner.py` | 磁盘扫描 |
| `analyzers/health_scorer.py` | 健康评分引擎 |

## 文档导航

| 文档 | 位置 | 用途 |
|------|------|------|
| 项目状态 | `PROJECT_STATUS.md` | 当前版本/完成项/已知问题 |
| 路线图 | `ROADMAP.md` | V1→V4 规划 |
| 变更日志 | `CHANGELOG.md` | 所有版本变更 |
| 开发规范 | `DEVELOPMENT_RULES.md` | 开发流程/安全/发布规范 |
| 当前 Sprint | `CURRENT_SPRINT.md` | 当前开发任务 |
| 文件树 | `PROJECT_FILE_TREE.md` | 完整目录结构 |
| 产品需求 | `docs/PRD.md` | PRD |
| 数据库设计 | `docs/DATABASE.md` | 数据库 Schema |
| 商业计划 | `docs/BUSINESS_PLAN.md` | 商业分析 |
| Beta 反馈 | `docs/BETA_USER_FEEDBACK.md` | 用户反馈汇总 |
| 文档模板 | `docs/templates/` | 各类文档模板 |
| 历史归档 | `docs/archive/` | V1/V2 旧版设计文档 |

## Git 信息

| 项目 | 值 |
|------|-----|
| 仓库路径 | `e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1` |
| 分支 | main |

## 安装构建

```powershell
cd setup_build
.\build.ps1          # 下载 Python embed + 安装依赖
makensis setup.nsi   # 生成 Setup.exe
```

## 冻结模块 (Tab 5-9)

备份中心 / 项目管理中心 / 知识库中心 / Prompt 管理中心 / 设置中心 — 显示 "Future Module"

## V3 冻结功能

软件最后运行时间 / GitHub/B站/Youtube/小红书 / 云资产管理 — 禁止当前版本开发

## 设计原则

- 闭环: 发现问题 -> 分析问题 -> 给出建议 -> 执行处理
- 安全: 删除移至回收站，系统路径自动保护
- 稳定: 禁止新增大型功能，仅处理可用性问题