# GraceOS V2 Beta (Registry Fix) Release Notes

> 日期: 2026-06-12 | Commit: (pending)
> 按 DEVELOPMENT_RULES.md 规范生成

## 版本定位
GraceOS V2 Beta (Registry Fix) — 核心BUG修复版本

## 关键修复
- 🔴 **软件安装路径**: 用winreg替代PowerShell注册表查询，消除JSON编码BUG
  - 修复前: 0/142有安装路径
  - 修复后: 36/142有安装路径

## 功能验证
- ✅ 重复文件处理: 保留/删除/归档 + 空间预估
- ✅ 未使用文件处理: 删除/归档/打开 + 系统保护
- ✅ 多版本软件: 检测17个 + 建议保留最新
- ✅ AI建议中心: 4维度自动分析
- ✅ 冻结模块: 5个Future Module正常显示

## 数据
| 维度 | 值 |
|------|-----|
| 文件 | 1,155,164 |
| 软件 | 142 (36含路径) |
| 磁盘 | 3 |
| 健康分 | 需刷新 |

## 启动
```powershell
streamlit run dashboard.py
```
