<!--
  PROJECT_STATUS.md - GraceOS V2.1
  生成日期: 2026-06-13
-->

## 📄 文档导航

> **入口文件**: [PROJECT_HANDOVER.md](PROJECT_HANDOVER.md) — 项目唯一入口
> **产品介绍**: [README.md](README.md)
> **路线图**: [ROADMAP.md](ROADMAP.md)
> **变更记录**: [CHANGELOG.md](CHANGELOG.md)
> **开发规范**: [DEVELOPMENT_RULES.md](DEVELOPMENT_RULES.md)

---

# GraceOS V2.1 - 项目状态报告

## 1. 当前版本

**版本**: V2.1  
**日期**: 2026-06-13  
**状态**: Sprint 完成，进入下一轮 Beta 测试

## 2. V2.1 Sprint 完成项

| 优先级 | 模块 | 完成内容 |
|--------|------|----------|
| P1 | 首页导航 | 资产中心卡片点击跳转到对应模块 |
| P1 | 文件搜索 | 增加生成日期列、删除按钮（单个+批量） |
| P1 | 软件中心 | 点击软件名启动软件、安装路径匹配增强 |
| P2 | 重复文件 | 建议保留/建议删除、单个+批量删除、多行选择 |
| P2 | Top 100 大文件 | 生成日期、单个+批量删除 |
| P2 | 长期未使用文件 | 生成日期、单个+批量删除、多行选择 |
| P2 | 软件重复版本 | 建议保留（最新）/建议卸载（最旧）、卸载按钮 |
| P3 | 评分展示 | 所有分项统一 /100，综合评分=平均值 |
| P3 | 字段中文化 | 软件名称/版本号/安装日期 |
| P3 | 安装程序 | 安装完成页自动运行复选框（默认勾选） |

## 3. 已冻结功能（进入 V3 ROADMAP）

- 软件最后运行时间
- GitHub 资产管理
- B站资产管理
- Youtube 资产管理
- 小红书资产管理
- 云资产管理

## 4. 数据库

**数据库**: `E:\创业项目\GraceOS\09_Database\graceos.db`  
**引擎**: SQLite  
**数据**: software=142 | disks=3 | files=1,155,164

## 5. 修改文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `dashboard.py` | ~22KB | V2.1 全功能重写 |
| `analyzers/health_scorer.py` | 4.5KB | /100 评分 |
| `scanners/software_scanner.py` | 8KB | 注册表匹配增强 |
| `setup_build/setup.nsi` | 2.3KB | 自动运行复选框 |

## 6. 启动方式

```powershell
cd "e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1"
streamlit run dashboard.py
```

## 7. 下一步

- 进入下一轮 Beta 测试
- 收集用户反馈
- 根据反馈决定 V2.2 内容
- V3 路线图中功能暂不启动
