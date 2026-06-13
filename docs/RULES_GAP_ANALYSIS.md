# RULES_GAP_ANALYSIS.md

> 分析日期: 2026-06-12
> 分析文件: DEVELOPMENT_RULES.md + PROJECT_OPERATING_RULES.md

## 检查结果

| # | 要求 | 状态 | 位置 |
|---|------|------|------|
| 1 | 文档优先验收原则 | ✅ 已存在 | DEVELOPMENT_RULES.md §文档规范 + PROJECT_OPERATING_RULES.md §文档优先原则 |
| 2 | 禁止仅通过截图验收 | ✅ 已存在 | PROJECT_OPERATING_RULES.md L28: "禁止截图验收。优先通过文档验收" |
| 3 | 完成必须提供证据 | ✅ 已存在 | PROJECT_OPERATING_RULES.md §完成必须有证据 + DEVELOPMENT_RULES.md §验收规范 |
| 4 | SELF_TEST_REPORT.md 强制 | ✅ 已存在 | PROJECT_OPERATING_RULES.md §Codex自测规范: "未通过不得进入验收阶段" + DEVELOPMENT_RULES.md §文档规范 |
| 5 | RELEASE_CHECKLIST.md 强制 | ✅ 已存在 | PROJECT_OPERATING_RULES.md §发布规范 + DEVELOPMENT_RULES.md §发布规范 |
| 6 | 发布阶段冻结机制 | ✅ 已存在 | PROJECT_OPERATING_RULES.md §产品阶段冻结机制: "禁止新增功能" |
| 7 | ChatGPT验收流程 | ✅ 已存在 | PROJECT_OPERATING_RULES.md §标准开发流程: "Codex自测 → 生成验收文档 → ChatGPT验收 → 修复问题 → 发布" |

## 已存在规则详情

### 1. 文档优先验收原则
- PROJECT_OPERATING_RULES.md: "禁止截图验收。优先通过文档验收。ChatGPT优先阅读文档。截图仅作为辅助。"
- DEVELOPMENT_RULES.md: "每次开发完成必须更新 PROJECT_STATUS.md，并根据任务生成 QA_REPORT.md / UI_REVIEW.md / BUILD_REPORT.md / SELF_TEST_REPORT.md / RELEASE_NOTE.md"

### 2. 禁止仅通过截图验收
- PROJECT_OPERATING_RULES.md §文档优先原则: "禁止截图验收。优先通过文档验收。"

### 3. 完成必须提供证据
- PROJECT_OPERATING_RULES.md §完成必须有证据: 明确列出文件路径/文件大小/测试结果/运行结果/下载链接五项证据
- DEVELOPMENT_RULES.md §验收规范: "禁止仅回复已完成/已修复/已发布，必须提供文件路径/文件大小/测试结果/下载链接/验证报告"

### 4. SELF_TEST_REPORT.md 强制
- PROJECT_OPERATING_RULES.md §Codex自测规范: "每次开发完成必须生成 SELF_TEST_REPORT.md。未通过不得进入验收阶段。"
- DEVELOPMENT_RULES.md §文档规范: 列出 SELF_TEST_REPORT.md 为必须文档

### 5. RELEASE_CHECKLIST.md 强制
- PROJECT_OPERATING_RULES.md §发布规范: "发布前必须生成 RELEASE_CHECKLIST.md，全部通过后方可发布"
- DEVELOPMENT_RULES.md §发布规范: "发布前必须生成 RELEASE_CHECKLIST.md"

### 6. 发布阶段冻结机制
- PROJECT_OPERATING_RULES.md §产品阶段冻结机制: "进入发布阶段后禁止新增功能。仅允许 Bug修复/性能优化/用户体验优化/打包发布。"

### 7. ChatGPT验收流程
- PROJECT_OPERATING_RULES.md §标准开发流程: "Codex自测 → 生成验收文档 → ChatGPT验收 → 修复问题 → 发布"
- PROJECT_OPERATING_RULES.md §角色分工: 明确 ChatGPT 负责"验收、QA评审、发布评审"

## 缺失规则

**无缺失。** 全部 7 项要求均已在两个规范文件中明确覆盖。

## 建议补充规则

以下为当前规范中已隐含但可进一步强化的建议：

| 建议 | 优先级 | 说明 |
|------|--------|------|
| 为"证据不足"定义量化标准 | P2 | 例如：测试报告至少包含 N 项测试 |
| 添加验收超时机制 | P2 | ChatGPT验收超过 N 小时未响应视为通过 |
| 规范版本管理 | P2 | PROJECT_OPERATING_RULES.md 添加版本号和更新日志 |
| 规范执行审计 | P3 | 定期检查开发任务是否严格遵守规范 |
