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
| `dashboard.py` | Streamlit Web 主应用 (~22KB) |
| `main.py` | CLI 扫描入口 |
| `scanners/software_scanner.py` | 软件扫描 (winget + 注册表) |
| `scanners/file_scanner.py` | 文件扫描 |
| `scanners/disk_scanner.py` | 磁盘扫描 |
| `analyzers/health_scorer.py` | 健康评分引擎 |
| `PROJECT_STATUS.md` | 项目当前状态 |
| `ROADMAP.md` | 路线图 |
| `CHANGELOG.md` | 变更记录 |
| `DEVELOPMENT_RULES.md` | 开发规范 |

## Git 信息

| 项目 | 值 |
|------|-----|
| 仓库路径 | `e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1` |
| 分支 | main |
| 远程 | `graceliu710605/GraceOS` (可能不可达) |

## 安装构建

```powershell
cd setup_build
.\build.ps1          # 下载 Python embed + 安装依赖
makensis setup.nsi   # 生成 Setup.exe
```

## 冻结模块

以下模块不在此版本开发范围，显示 "Future Module":
- 备份中心 (Tab 5)
- 项目管理中心 (Tab 6)
- 知识库中心 (Tab 7)
- Prompt 管理中心 (Tab 8)
- 设置中心 (Tab 9)

## V3 冻结功能

以下功能已明确进入 V3 路线图，当前版本禁止开发:
- 软件最后运行时间
- GitHub/B站/Youtube/小红书资产管理
- 云资产管理 (百度网盘等)

## 设计原则

- 闭环: 发现问题 → 分析问题 → 给出建议 → 执行处理
- 安全: 删除移至 E:\回收站，系统路径自动保护
- 稳定性优先: 禁止新增大型功能，仅处理可用性问题
