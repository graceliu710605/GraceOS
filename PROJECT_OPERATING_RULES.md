# 项目运营规范

> 维护日期: 2026-06-13
> 适用项目: GraceOS

---

## 引用说明

本项目遵循 `E:\创业项目\00_AI组织` 规范。

| RULE | 位置 | 说明 |
|------|------|------|
| 030 | `AI_WORKFLOW.md` | 回归测试 |
| 031 | `AI_WORKFLOW.md` | 测试证据 |
| 032 | `AI_WORKFLOW.md` | L1/L2/L3 风险分级 |
| 033 | `AI_WORKFLOW.md` | Stable Baseline |
| 034 | `AI_WORKFLOW.md` | AI 启动检查 |
| 035 | `AI_WORKFLOW.md` | Smoke Test |
| 036 | `AI_WORKFLOW.md` | Root Cause Analysis |
| 037 | `AI_WORKFLOW.md` | UI First |

---

## GraceOS Smoke Test 清单

首页 / 文件搜索 / 重复文件 / Top100 / 未使用 / 软件 / 磁盘

---

## UI First 开发流程

```
需求定义 → UI草图 → Grace确认 → UI冻结 → 功能开发 → Smoke Test → 发布
```

## GraceOS 特有规则

- 发布标准: 非开发人员可直接安装运行
- 产品冻结: 发布阶段禁止新增功能
- Codex 自测: 提交前生成 SELF_TEST_REPORT.md