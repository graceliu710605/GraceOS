# GraceOS 规则更新报告

**日期**: 2026-06-13

---

## 更新文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `PROJECT_HANDOVER.md` | 修改 | 新增「组织规范」章节，引用 AI 组织 |
| `PROJECT_OPERATING_RULES.md` | 重写 | 删除重复内容，仅保留 GraceOS 特有规则 |

## 规则迁移明细

### 从 GraceOS 移除（进入 AI 组织）

| 规则 | 原因 | 新位置 |
|------|------|--------|
| 角色分工 | 通用规则，所有项目适用 | `AI_TEAM.md` |
| 标准开发流程 | 通用规则 | `AI_WORKFLOW.md` |
| 完成必须有证据 | 通用规则 | `AI_WORKFLOW.md` 完成标准 |
| 跨项目复用声明 | 通用规则，不应在项目中声明 | 不再保留 |

### 保留在 GraceOS（项目特有）

| 规则 | 原因 |
|------|------|
| 发布标准（无需Python、双击安装） | GraceOS 产品特有 |
| 产品阶段冻结机制 | GraceOS 产品管理特有 |
| Codex 自测规范 | GraceOS 实施细节 |
| 文档验收规范 | GraceOS 文档清单 |

## PROJECT_HANDOVER.md 变更

新增章节：

```markdown
## 组织规范

本项目遵循 `E:\创业项目\00_AI组织` 中的组织规范与工作流程。
详见：AI_TEAM.md / AI_WORKFLOW.md / PROJECT_OPERATING_RULES.md
```

## PROJECT_OPERATING_RULES.md 变更

- 删除: 角色分工、标准开发流程、跨项目复用（已进入 AI 组织）
- 新增: 引用说明（指向 AI 组织）
- 保留: 发布标准、冻结机制、自测规范、文档验收规范