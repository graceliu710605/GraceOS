# 项目运营规范

> 维护日期: 2026-06-13
> 适用项目: GraceOS

---

## 引用说明

本项目遵循 `E:\创业项目\00_AI组织` 中的通用规范。

| 规则 | 位置 | 说明 |
|------|------|------|
| RULE-030 | `AI_WORKFLOW.md` | 回归测试 |
| RULE-031 | `AI_WORKFLOW.md` | 测试证据 |
| RULE-032 | `AI_WORKFLOW.md` | L1/L2/L3 风险分级 |
| RULE-033 | `AI_WORKFLOW.md` | Stable Baseline 管理 |
| RULE-034 | `AI_WORKFLOW.md` | AI 任务启动检查 |
| RULE-035 | `AI_WORKFLOW.md` | 修改后 Smoke Test |
| RULE-036 | `AI_WORKFLOW.md` | Root Cause Analysis |

---

## GraceOS Smoke Test 清单 (RULE-035)

任何代码修改后必须验证以下 7 个核心模块可打开：

| 模块 | 验证 |
|------|------|
| 🏠 首页 | 评分显示 / AI 建议 |
| 🔍 文件搜索 | 搜索框可输入 |
| 🔧 重复文件 | 列表正常 + 分页 |
| 📦 Top100 | 列表正常 |
| 🕐 未使用文件 | 列表正常 |
| 📋 软件中心 | 列表正常 |
| 📑 磁盘分析 | 容量显示 |

---

## GraceOS 特有规则

### 发布标准
非开发人员电脑可直接安装运行。

### 产品阶段冻结
进入发布阶段后禁止新增功能。

### Codex 自测
每次开发完成必须生成 `SELF_TEST_REPORT.md`。