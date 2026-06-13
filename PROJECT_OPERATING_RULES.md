# 项目运营规范

> 维护日期: 2026-06-13
> 适用项目: GraceOS

---

## 引用说明

本项目遵循 `E:\创业项目\00_AI组织` 中的通用规范。本文件仅记录 **GraceOS 项目特有规则**。

**通用规则**（见 AI 组织）:
- 角色分工 → `AI_TEAM.md`
- 开发流程 → `AI_WORKFLOW.md`
- 验收标准 → `AI_WORKFLOW.md` 

---

## GraceOS 特有规则

### 发布标准

非开发人员电脑可直接安装运行。

- ✅ 无需Python
- ✅ 无需命令行
- ✅ 无需联网安装依赖
- ✅ 双击安装
- ✅ 双击使用

### 产品阶段冻结机制

进入发布阶段后 **禁止新增功能**。

仅允许: Bug修复 / 性能优化 / 用户体验优化 / 打包发布

### Codex 自测规范

每次开发完成必须生成 `SELF_TEST_REPORT.md`，包含测试项列表、结果、通过状态。

### 文档验收规范

优先通过文档验收。标准文档包括:

| 文档 | 用途 |
|------|------|
| `FUNCTION_VERIFICATION_REPORT.md` | 功能验证报告 |
| `UI_VERIFICATION_REPORT.md` | UI 验证报告 |
| `QA_REPORT.md` | 测试报告 |
| `INSTALL_TEST_REPORT.md` | 安装测试报告 |
| `RELEASE_NOTE.md` | 发布说明 |