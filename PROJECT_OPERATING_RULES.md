# 项目运营规范

> 维护日期: 2026-06-13
> 适用项目: GraceOS

---

## 引用说明

本项目遵循 `E:\创业项目\00_AI组织` 中的通用规范。

**通用规则（引用）**:
| 规则 | 位置 |
|------|------|
| RULE-030 回归测试 | `AI_WORKFLOW.md` |
| RULE-031 测试证据 | `AI_WORKFLOW.md` |
| 角色分工 | `AI_TEAM.md` |
| 经验沉淀 | `LESSONS_LEARNED.md` |

---

## GraceOS 特有规则

### 提交前强制报告

任何功能开发完成后**必须**提交以下三份报告：

| 报告 | 文件名 |
|------|--------|
| 回归测试报告 | `REGRESSION_TEST_REPORT.md` |
| 功能验证报告 | `FUNCTION_VERIFICATION_REPORT.md` |
| UI 验证报告 | `UI_VERIFICATION_REPORT.md` |

**缺少任一报告 → 视为未完成，禁止提交。**

### 发布标准
非开发人员电脑可直接安装运行。

### 产品阶段冻结机制
进入发布阶段后禁止新增功能。

### Codex 自测规范
每次开发完成必须生成 `SELF_TEST_REPORT.md`。