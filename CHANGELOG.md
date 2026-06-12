# Changelog

## [Unreleased]

### Added (2026-06-12 磁盘资产中心)

- 磁盘资产中心: Dashboard 新增独立「💾 磁盘资产中心」Tab
  - 显示所有磁盘（C盘、D盘等）的容量、已用、剩余空间
  - 使用率进度条 + 颜色提示（绿 <70% / 黄 70-90% / 红 >90%）
- 磁盘导入器: 新增 `disk_to_sqlite.py`，将 PowerShell Get-PSDrive JSON 转换为 SQLite `disks` 表

### Fixed (2026-06-12)

- `software_scanner.py`: 修复扫描结果始终为 0 的 Bug
  - 根因 1: `encoding="utf-8"` 强制 UTF-8 解码中文 Windows 的 GBK 输出，`errors="ignore"` 静默丢弃所有字符
  - 根因 2: 只读 `result.stdout`，部分 winget 版本将输出写入 `stderr`
  - 修复: 移除强制 UTF-8 编码；`errors` 改为 `replace`；优先读 stdout，回退 stderr

### Added (2026-06-12)

- 软件资产中心: Dashboard 新增独立「💻 软件资产中心」页面
- 软件扫描器 V2: `software_scanner.py` 重写，支持结构化解析
  - 解析 `winget list` 输出为 Name / Id / Version / Source 字段
  - 查询 Windows 注册表获取 Publisher / InstallDate / EstimatedSize
  - 自动合并 winget 和注册表数据
- 软件导入器: 新增 `software_to_sqlite.py`，将结构化数据导入 `software` 表
- 软件搜索: 支持按软件名称或发布商搜索
- 软件排序: 支持按名称、安装日期、大小排序
- 发布商统计: 显示发布商 Top 20 分布

### Added (2026-06-11)

- Dashboard: 文件操作按钮 -- 打开文件、打开目录、复制路径
- Dashboard: 文件搜索结果按文件大小降序排列
- Dashboard: 版本号从 V3 修正为 V1
- Dashboard: 每行文件额外显示大小和修改时间信息

### Changed (2026-06-11)

- Dashboard: `st.dataframe` 替换为逐行渲染 + 每行三个操作按钮
- Dashboard: 各板块默认显示 Top 50（原 Top 100）以提升交互性能
- Dashboard: 重复文件统计增加 `MIN(file_path)` 以支持操作按钮

## [V1] - 2026-06-10

### Added

- GraceOS 项目初始化
- 软件扫描器 (winget)
- 软件搜索 (JSON 原始字符串)
- 磁盘扫描器 (PowerShell Get-PSDrive)
- 文件扫描器 (os.walk C:/D:/E:)
- 大文件分析器
- JSON 到 SQLite 导入器 (流式, 批量 5000)
- Streamlit Dashboard (文件搜索、大文件、重复文件、长期未使用)
- CLI 入口 main.py
