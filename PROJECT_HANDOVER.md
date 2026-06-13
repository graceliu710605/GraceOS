<!--
  PROJECT_HANDOVER.md — 个人数字资产管家 (GraceOS) 项目唯一入口
  创建日期: 2026-06-13
  版本: V2 RC2
  用途: 任何新人/新会话/新工具从此文件开始，无需询问。
-->

# 个人数字资产管家 — 项目交接文档

> 项目代号: GraceOS
> 当前版本: V2 RC2
> 最后更新: 2026-06-13

---

## 一、这是什么？

个人数字资产管家是一套**个人数字资产管理平台**。自动扫描本地文件、软件、磁盘，给出健康评分和AI整理建议，支持一键执行清理。

**一句话**: 你电脑的数字仪表盘——发现 → 分析 → 建议 → 执行，形成闭环。

---

## 二、快速开始（新人必读）

### 安装方式

| 方式 | 适用 | 文件 |
|------|------|------|
| Setup.exe 安装（推荐） | 普通用户 | 个人数字资产管家_Setup.exe (71.1 MB) |
| 便携版 | 开发者/无需安装 | 个人数字资产管家_Portable.zip (18 KB) |
| 源码启动 | 开发者 | `streamlit run dashboard.py` |

### 安装后启动

```
双击桌面快捷方式 / 开始菜单快捷方式
  → 浏览器自动打开 http://localhost:8501
  → 首次运行自动扫描软件+磁盘 (~2分钟)
  → 进入仪表盘首页
```

---

## 三、文档导航

按阅读优先级排列：

| 优先级 | 文档 | 用途 |
|--------|------|------|
| 1 | `PROJECT_HANDOVER.md` | 👈 **你在这里**，项目入口 |
| 2 | `PROJECT_STATUS.md` | 当前版本状态、已完成/待办 |
| 3 | `README.md` | 产品介绍、快速开始 |
| 4 | `ROADMAP.md` | 版本路线图、未来计划 |
| 5 | `CHANGELOG.md` | 各版本变更记录 |

| 类别 | 文档 | 说明 |
|------|------|------|
| 开发规范 | `DEVELOPMENT_RULES.md` | 产品定位、开发原则、AI建议规范、删除安全、发布门禁 |
| 运营规范 | `PROJECT_OPERATING_RULES.md` | 角色分工、开发流程、文档优先、自测标准、冻结机制 |
| 构建 | `setup_build/README_BUILD.md` | 如何从源码构建 Setup.exe |
| 安装 | `INSTALL_GUIDE.md` | 用户安装说明 |

| 类别 | 文档 | 说明 |
|------|------|------|
| 产品需求 | `docs/PRD.md` | V2 产品需求 |
| 系统架构 | `docs/GraceOS_V2_ARCHITECTURE.md` | 系统架构设计 |
| 数据库设计 | `docs/DATABASE.md` | 数据库表结构 |
| UI 设计 | `docs/UI_DESIGN.md` | 界面设计规范 |
| 商业计划 | `docs/BUSINESS_PLAN.md` | 商业模式分析 |

| 类别 | 文档 | 说明 |
|------|------|------|
| 发布检查 | `docs/RELEASE_CHECKLIST.md` | 5项门禁规则 |
| 安装测试 | `docs/INSTALL_TEST_REPORT.md` | 最新安装测试证据 |
| 启动分析 | `docs/STARTUP_FAILURE_ANALYSIS.md` | P0 启动失败根因 |
| QA 报告 | `docs/QA_REPORT.md` | 功能测试报告 |
| 发布说明 | `docs/RELEASE_NOTE.md` | 最新发布说明 |
| 发行清单 | `docs/RELEASE_CHECKLIST.md` | 发布前检查项 |

---

## 四、当前版本状态

| 项目 | 值 |
|------|-----|
| 版本号 | V2 RC2 |
| Setup.exe | 71.1 MB |
| 数据库 | SQLite (graceos.db) |
| 软件资产 | 142 条 |
| 文件索引 | 1,155,164 条 |
| 磁盘 | 3 个 (C/D/E) |
| Python | 3.13.13 (嵌入) |
| Streamlit | 1.58.0 |

### 5项门禁状态

| 门禁 | 状态 |
|------|------|
| 全新安装 | ✅ |
| 启动测试 | ✅ |
| localhost 服务 | ✅ |
| 首页访问 | ✅ |
| 卸载测试 | ✅ |

---

## 五、技术栈

| 层 | 技术 |
|----|------|
| 前端 | Streamlit 1.58 |
| 数据库 | SQLite |
| 扫描器 | winget + winreg + os.walk + PowerShell |
| 打包 | NSIS 3.x + Python 3.13 Embeddable |
| 截图 | Playwright |

---

## 六、启动命令

```powershell
# 开发模式
cd GraceOS_V1
streamlit run dashboard.py

# 生产模式（嵌入Python）
{安装目录}\python\python.exe -m streamlit run {安装目录}\app\dashboard.py --server.port 8501
```

---

## 七、已知问题

1. 文件扫描需单独运行 `python main.py`（未集成到 Dashboard）
2. 跨平台不支持（依赖 winget + winreg，仅 Windows）
3. 未在全新 Windows 虚拟机中做过完整验收

---

## 八、下一步

- 进入 Beta 用户测试阶段
- 收集用户反馈
- 修复发现的问题
- 规划 V2.1

---

*此文件是项目的唯一入口。任何问题先查此文件。*
