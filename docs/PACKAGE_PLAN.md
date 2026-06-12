# GraceOS Windows EXE 打包方案

> 研究日期: 2026-06-12

## 方案对比

| 方案 | 工具 | 大小 | 速度 | 难度 | 推荐 |
|------|------|------|------|------|------|
| A | PyInstaller | ~50MB | 慢(5-10min) | 低 | ⭐⭐⭐ |
| B | Nuitka | ~30MB | 很慢(20-40min) | 中 | ⭐⭐ |
| C | NSIS + venv | ~20MB | 快(2min) | 高 | ⭐⭐⭐⭐ |
| D | Bat 启动器 | 0MB | 即时 | 极低 | ⭐⭐⭐⭐⭐ (当前) |

## 推荐方案: D → C → A

### 当前 (P0): Bat 启动器 ✅
- 零打包成本
- 双击即用
- 需要 Python 环境
- **已实现**: `Start_GraceOS.bat`

### 近期 (P1): NSIS + 嵌入式 Python
- 使用 `python-embed` 嵌入 Python 3.13
- NSIS 制作安装包
- 用户无需安装 Python
- 预计包大小: ~40MB
- 开发时间: 2-3 天

### 远期 (P2): PyInstaller
- 单一 `.exe` 文件
- 双击启动，无需任何依赖
- 包大小: ~50-60MB
- 启动时间: 5-8 秒
- 开发时间: 1-2 天调试

## 实施计划

| 阶段 | 内容 | 时间 |
|------|------|------|
| 已完成 | Bat 一键启动 | ✅ |
| Phase 1 | NSIS + python-embed 安装包 | 2-3 天 |
| Phase 2 | PyInstaller .exe 单文件 | 1-2 天 |
| Phase 3 | 自动更新机制 | 3-5 天 |

## 技术细节: PyInstaller

```bash
# 安装
pip install pyinstaller

# 打包
pyinstaller --onefile \
  --name GraceOS \
  --add-data "scanners;scanners" \
  --add-data "analyzers;analyzers" \
  --hidden-import streamlit \
  dashboard.py

# 输出: dist/GraceOS.exe (~55MB)
```

## 注意事项

- Streamlit 打包可能存在兼容性问题, 需额外配置
- 中文路径支持需测试
- 数据库路径需可配置
- 首次启动扫描耗时较长, 需进度提示
