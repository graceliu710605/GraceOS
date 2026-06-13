# 项目运营规范

> 维护日期: 2026-06-13
> 适用项目: GraceOS

---

## 引用说明

本项目遵循 `E:\创业项目\00_AI组织` 中的通用规范。本文件仅记录 **GraceOS 项目特有规则**。

**通用规则（引用）**:
| 规则 | 位置 |
|------|------|
| 角色分工与职责边界 | `AI_TEAM.md` |
| 开发流程与验收规则 | `AI_WORKFLOW.md` (含 RULE-030) |
| 经验沉淀 | `LESSONS_LEARNED.md` |

---

## GraceOS 特有规则

### 发布标准
非开发人员电脑可直接安装运行。
- ✅ 无需Python / 无需命令行 / 无需联网安装依赖 / 双击安装 / 双击使用

### 产品阶段冻结机制
进入发布阶段后禁止新增功能。仅允许 Bug修复/性能优化/UX优化/打包发布。

### Codex 自测规范
每次开发完成必须生成 `SELF_TEST_REPORT.md`。

### 文档验收规范
标准文档: FUNCTION_VERIFICATION_REPORT / UI_VERIFICATION_REPORT / QA_REPORT / INSTALL_TEST_REPORT / RELEASE_NOTE