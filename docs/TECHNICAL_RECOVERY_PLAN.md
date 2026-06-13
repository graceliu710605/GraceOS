# TECHNICAL_RECOVERY_PLAN.md

**日期**: 2026-06-13

---

## 最近稳定版本

| Commit | 说明 | 验证状态 |
|--------|------|----------|
| `3eb26dd` | P0 fix: checkbox empty label | ✅ Playwright 截图确认全部 Tab 正常 |

该版本是最后一个经过完整 Playwright 逐 Tab 验证的版本。

## 当前版本问题范围

自 `3eb26dd`（稳定版）之后，经历了 **3 轮代码修改 + 3 轮修复**：

| 轮次 | Commit | 变更 | 引入问题 |
|------|--------|------|----------|
| 1 | `5d7e139` | 7 项修复（自适应大小/目录列/分页/存在性检查）通过 fix 脚本批量修改 | NameError: total_groups/del_mb 未定义 |
| 2 | `d2e2f42` | 补充 total_groups/del_bytes 补丁 | 15 万行全渲染导致 session_state RuntimeError |
| 3 | `f83f710` | 加分页 50 组/页 | StreamlitDuplicateElementKey: dup_cb_49 |

当前 `HEAD` 已修复前两轮问题，但仍有 DuplicateElementKey 未修 + 磁盘 Tab 导航失效。

## 方案对比

| | 方案 A: 继续修复 | 方案 B: 回退 + 重新合并 |
|---|---|---|
| **做法** | 修复 DupKey + 磁盘导航 | 回退到 `3eb26dd`，逐项重新实现需求 |
| **风险** | 高 — 每次 fix 脚本可能引入新问题，已有 3 轮先例 | 低 — 从已验证基线出发，增量可控 |
| **预计工作量** | 1-2 轮（4-6 小时） | 1 轮重新实现（2-3 小时） |
| **代码质量** | 累积 3 层补丁，可维护性差 | 清晰、单次实现 |
| **可预测性** | 不确定 — 下一轮可能再引入新 Bug | 高 — 每项功能增量验证 |

## 推荐方案: **方案 B**

**回退到 `3eb26dd`**，在该基础上逐项实现以下需求：

| 需求 | 说明 | 实现方式 |
|------|------|----------|
| 自适应文件大小 | Bytes/KB/MB/GB | 新增 `_format_size()` 函数 |
| 目录列 | 文件搜索增加所在目录列 | 新增 Column 5 |
| 重复文件分页 | 50 组/页 | 新增 `dup_page` session_state |
| 文件存在性检查 | 不存在文件显示 ⚠️ | 新增 `_file_exists()` |
| 安全删除 | 删除前检查 os.path.exists | 修改 `_safe_delete()` |

## 执行步骤

```powershell
# 1. 回退到稳定版本
git checkout 3eb26dd -- dashboard.py

# 2. 逐项实现（每次提交后回归测试）
# 3. 完成后执行 L2 Sanity Test
# 4. 提交最终版本
```

## 风险评估

- ✅ `3eb26dd` 已经过 Playwright 全 Tab 验证
- ✅ 5 项需求均为独立增量，互不依赖
- ✅ 每项可实现后立即回归测试，不累积风险
- ⚠️ 唯一风险：重复文件 15 万行渲染问题。但 `3eb26dd` 基线只渲染 50 组，不触发此问题。分页需求再精确添加时可控