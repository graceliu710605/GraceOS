# RUNTIME_ERROR_FIX_REPORT.md

**日期**: 2026-06-13
**问题**: 多个页面无法打开，NameError/AttributeError

---

## 错误清单

| # | 错误 | 位置 | 原因 | 修复 |
|---|------|------|------|------|
| 1 | `NameError: name 'total_groups' is not defined` | 重复文件 ~L186 | fix脚本字符串替换失败，`total_groups = len(df_dup)` 未写入 | 补充计算 |
| 2 | `NameError: name 'total_saved_bytes' is not defined` | 重复文件 ~L187 | 同上，`total_saved_bytes` 未计算 | 补充计算 |
| 3 | `NameError: name 'del_mb' is not defined` | 重复文件 ~L195 | `del_mb` 已改名 `del_bytes`，但 f-string 未更新 | 改为 `_format_size(del_bytes)` |

## 验证结果

Playwright 自动化逐 Tab 验证（8 个 Tab）：

| Tab | 结果 |
|-----|------|
| 🏠 首页 | ✅ OK |
| 📂 文件 | ✅ OK |
| 📋 软件 | ✅ OK |
| 📑 磁盘 | ✅ OK |
| 📊 存储 | ✅ OK |
| 💾 备份 | ✅ OK |
| 📁 项目 | ✅ OK |
| 🧠 知识库 | ✅ OK |

- ✅ 所有页面可进入
- ✅ 所有页面不报异常
- ✅ `py_compile` 编译通过

## 根因

FIX_IMPLEMENTATION_REPORT 执行时，Python fix 脚本的字符串替换因 `size_mb` 已被第一次 `apply_patch` 改为 `file_size` 而匹配失败，导致 `total_groups` 和 `total_saved_bytes` 计算代码未写入文件。