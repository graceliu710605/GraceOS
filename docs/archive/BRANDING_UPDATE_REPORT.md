# 品牌统一更新报告

> 日期: 2026-06-12 | 任务: 统一产品品牌命名

## 命名规则

| 场景 | 名称 |
|------|------|
| 对外产品名 | **个人数字资产管家** |
| 项目代号 / GitHub 仓库 | GraceOS（保留不变） |
| 发布文件 | 个人数字资产管家_Portable.zip / Setup.exe |

## 修改文件清单

| 文件 | 修改内容 |
|------|---------|
| `dashboard.py` | Docstring → "个人数字资产管家 (GraceOS V2 Beta)" \n page_title → "个人数字资产管家" \n st.title → "个人数字资产管家" |
| `Start_GraceOS.bat` | title + echo → "个人数字资产管家" |
| `README.md` | 标题 → "个人数字资产管家" + 副标题 GraceOS |
| `INSTALL_GUIDE.md` | 标题 + 正文 → "个人数字资产管家" |
| `docs/RELEASE_NOTE.md` | 标题 + 正文 → "个人数字资产管家" |
| `docs/PACKAGE_PLAN.md` | 标题 + 打包名 → "个人数字资产管家" |
| `docs/DEMO_MODE_DESIGN.md` | 标题 + Welcome → "个人数字资产管家" |
| `DEVELOPMENT_RULES.md` | 标题 → "个人数字资产管家 开发规范" |
| `docs/RELEASE_CHECKLIST.md` | 标题 → "个人数字资产管家 发布检查清单" |

## 验证

```bash
# 检查 dashboard.py 不再包含对外 GraceOS 引用
grep "GraceOS" dashboard.py
# 应只保留 DB_FILE 路径 (graceos.db) 和 docstring 中的 (GraceOS V2 Beta)
```

## 未修改

- 数据库路径保持 `graceos.db`（内部实现，不对外展示）
- GitHub 仓库名保持 `GraceOS`
- 代码注释中的 GraceOS 保持（不影响用户可见）
