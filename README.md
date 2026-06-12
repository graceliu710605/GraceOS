# GraceOS — Personal Digital Operating System

> **发现问题 → 分析问题 → 给出建议 → 执行处理**

GraceOS 是个人数字资产管理系统，帮助你统一管理文件、软件、磁盘资产，并通过 AI 建议实现自动整理。

## 功能

| 模块 | 说明 |
|------|------|
| 🏠 首页仪表盘 | 数字健康评分 (0-100) + AI 建议中心 |
| 📂 文件资产中心 | 全盘文件索引 (115万+)、搜索、重复文件处理、未使用文件清理 |
| 📋 软件资产中心 | 已安装软件清单 (142个)、多版本检测、安装路径打开 |
| 📑 磁盘资产中心 | C/D/E 盘容量监控、使用率颜色预警 |
| 📊 存储空间分析 | 目录级别空间统计 |

## 技术栈

| 层面 | 技术 |
|------|------|
| 前端 | Streamlit (Python) |
| 数据库 | SQLite |
| 扫描器 | winget + winreg + PowerShell + os.walk |
| AI | ChatGPT API (评分建议) |

## 快速启动

```powershell
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行扫描器
python main.py

# 3. 导入数据
python json_to_sqlite.py
python software_to_sqlite.py
python disk_to_sqlite.py

# 4. 启动 Dashboard
streamlit run dashboard.py
```

## 项目结构

```
GraceOS_V1/
├── dashboard.py              # 主应用
├── main.py                   # 扫描入口
├── scanners/                 # 扫描器
├── analyzers/                # 分析器 + 评分引擎
├── docs/                     # 设计文档和报告
├── screenshots/              # 页面截图
├── DEVELOPMENT_RULES.md      # 开发规范
├── PROJECT_STATUS.md         # 项目状态
├── ROADMAP.md                # 路线图
└── CHANGELOG.md              # 变更日志
```

## 版本历史

| 版本 | Commit | 说明 |
|------|--------|------|
| V1 RC1 | `797ac7b` | 文件/软件/磁盘资产管理 |
| V2 Alpha | `50795bb` | 健康评分 + 10-tab Dashboard |
| V2 Beta | `adb118f` | 资产处理中心 + AI建议 + 注册表修复 |

## 许可

MIT
