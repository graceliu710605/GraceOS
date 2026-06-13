# GraceOS V2 RC2 发布说明

> 发布日期: 2026-06-13
> 版本: V2 RC2
> 基于: V2 Beta (registry fix)

---

## 本次发布目标

**完整性交付** — 停止碎片化修复，进行一次完整的产品化交付。

---

## 关键变更

### P0: 启动失败修复

| 问题 | 根因 | 修复 |
|------|------|------|
| Setup.exe 安装后浏览器打开 localhost:8501 拒绝连接 | BAT 中 Python 路径 `..\python\python.exe` 不存在 | Python 嵌入环境移至 `python/` 子目录，BAT 路径匹配 |
| | BAT 直接运行 `python.exe dashboard.py` 不启动 Streamlit 服务 | 改为 `python -m streamlit run dashboard.py --server.port 8501` |

### 安装目录结构优化

旧版根目录散落 35+ 个 .pyd/.dll 文件。新版仅 2 个子目录：

```
个人数字资产管家/
├── python/    ← Python 3.13 嵌入环境
└── app/       ← GraceOS 应用
```

### 发布门禁

新增 `RELEASE_CHECKLIST.md` 强制门禁规则，`DEVELOPMENT_RULES.md` 新增发布门禁章节。详情见 [INSTALL_TEST_REPORT.md](docs/INSTALL_TEST_REPORT.md)。

---

## 交付物

| 文件 | 大小 | 说明 |
|------|------|------|
| 个人数字资产管家_Setup.exe | 71.1 MB | NSIS 安装包 |
| setup_build/ | - | 构建源码 (NSIS + build.ps1) |

---

## 安装验证 (5 项门禁全部通过)

| 门禁 | 结果 |
|------|------|
| 1. 全新安装 | ✅ 目录结构整洁 |
| 2. 启动测试 | ✅ BAT 路径正确，无错误 |
| 3. localhost 服务 | ✅ 8501 LISTENING, HTTP 200 |
| 4. 首页访问 | ✅ 页面正常渲染 |
| 5. 卸载测试 | ✅ 无残留 |

---

## 已知限制

- 未在全新 Windows 虚拟机中验证安装流程
- 安装需要管理员权限 (NSIS RequestExecutionLevel admin)
- 建议发布前在全新环境中执行一次完整用户验收测试
