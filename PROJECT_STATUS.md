<!--
  PROJECT_STATUS.md - GraceOS V2.1
  生成日期: 2026-06-13
-->

## 📄 文档导航

> **入口文件**: [PROJECT_HANDOVER.md](PROJECT_HANDOVER.md) — 项目唯一入口

---

# GraceOS V2.1 - 项目状态报告

## 1. 当前版本

**版本**: V2.2-stable
**日期**: 2026-06-13
**状态**: Beta 测试 — 14 个 commit 已推送到 GitHub

## 2. Stable Baseline

| Commit | 说明 |
|--------|------|
| `bdbfd72` | v2.2-digital-assets: V2.1 + 数字资产中心 (tagged) |
| `HEAD` (`947ae2f`) | fix: prevent empty DataFrame after stale filtering |

### 2026-06-13 V2.2 修复记录 (14 commits)

| # | Commit | 说明 |
|---|--------|------|
| 1 | `e7143cb` | P0: size_mb KeyError + dup LIMIT + UI cleanup |
| 2 | `f81d890` | perf: @st.cache_data for Tab1 stats |
| 3 | `ab08a51` | refactor: STORAGE_DIRS config |
| 4-6 | `c429910`→`c1675de` | fix: dir column + stale disable + software table |
| 7 | `eea334a` | fix: h7 NameError in dup header |
| 8 | `af409f8` | feat: old files sort toggle |
| 9 | `3c49f5d` | feat: oldest software sort + launch + path |
| 10 | `1f6d2f3` | batch fixes #1-11 |
| 11 | `9eebd45` | fix: #4 delete removes DB record |
| 12 | `b19d3ab` | fix: 0-byte filter in search |
| 13 | `b1fa84f` | fix: stale record filter all tables |
| 14 | `947ae2f` | fix: empty DataFrame guard after filter |

### Sanity Test (2026-06-13 23:07)

**11/11 PASS** — 见 [QA_REPORT.md](docs/QA_REPORT.md)

| 维度 | 说明 |
|------|------|
| **故障** | dashboard.py 出现 NameError: df_dup/df_dup_page not defined |
| **根因** | commit de1fd5a (perf) 引入懒加载重构，else 块只包裹 df_dup 查询行，后续 50+ 行处理代码仍然在 else 外执行 |
| **恢复方案** | 方案A: 回退到 bdbfd72 (v2.2-digital-assets stable) |
| **执行** | `git reset --hard bdbfd72` + cherry-pick 52918d4 (性能分析文档) + bc562d1 (规则同步) |
| **丢弃** | de1fd5a (perf indexes+lazy load+cache) + 3dcdbca (fix indentation) — 两个 commit 均为问题源头 |
| **结果** | AST 验证通过，无 lazy load/session_state 污染代码 |

## 3. V2.1 功能清单

| 模块 | 功能 |
|------|------|
| 首页 | 健康评分 /100, AI 建议 |
| 文件搜索 | 删除/文件名/日期/自适应大小/目录列 |
| 重复文件 | 建议保留/删除/批量删除/分页 |
| Top100 大文件 | 删除/批量删除/自适应大小 |
| 长期未使用文件 | 删除/批量删除/自适应大小 |
| 软件中心 | 卸载/建议/名称启动/版本/安装路径 |
| 磁盘分析 | 容量/使用率颜色 |

## 4. Sanity Test 结果 (2026-06-13)

| 模块 | 结果 |
|------|------|
| 首页 | ✅ PASS |
| 文件搜索 | ✅ PASS |
| 重复文件 | ✅ PASS |
| Top100 | ✅ PASS |
| 未使用文件 | ✅ PASS |
| 软件中心 | ✅ PASS |
| 磁盘分析 | ✅ PASS |

## 5. 组织规则

本项目遵循 `E:\知识库obsidian\02_Projects\graceos\00_AI组织`:
- RULE-030 回归测试
- RULE-031 测试证据
- RULE-032 风险分级
- **RULE-033 Stable Baseline 管理
- RULE-034 AI 任务启动检查
- RULE-035 修改后 Smoke Test
- RULE-036 Root Cause Analysis
- RULE-037 UI First
- RULE-038 Definition of Done
- RULE-039 任务输出格式**