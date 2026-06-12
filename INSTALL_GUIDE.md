# 个人数字资产管家 安装指南

> 版本: V2 Beta | 最后更新: 2026-06-12

## 系统要求

| 项目 | 最低要求 |
|------|---------|
| 操作系统 | Windows 10 / 11 (64-bit) |
| Python | 3.10 或更高 |
| 磁盘空间 | 500 MB (不含数据库) |
| 网络 | 首次运行需联网安装依赖 |

## 一键安装

### 方法 1: 双击启动（推荐）

1. 解压 个人数字资产管家到任意目录
2. 双击 `Start_GraceOS.bat`
3. 首次运行自动完成：
   - 安装 Python 依赖
   - 扫描软件和磁盘
   - 导入数据库
   - 启动 Dashboard
4. 浏览器自动打开 `http://localhost:8501`

### 方法 2: 命令行

```powershell
cd GraceOS_V1
pip install -r requirements.txt
python main.py
python json_to_sqlite.py
python software_to_sqlite.py
python disk_to_sqlite.py
streamlit run dashboard.py
```

## 首次运行时间

| 步骤 | 预计时间 |
|------|---------|
| 安装依赖 | 1-2 分钟 |
| 软件扫描 | 10-15 秒 |
| 磁盘扫描 | 2-3 秒 |
| Dashboard 启动 | 5-10 秒 |
| **总计** | **约 2 分钟** |

> 注意：文件扫描器 (file_scanner) 首次运行需要扫描 C:/D:/E: 全盘，可能需要 10-30 分钟。默认不自动运行。

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| Python 未找到 | 安装 Python 3.10+ 并勾选 "Add to PATH" |
| pip install 失败 | 检查网络连接, 尝试 `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` |
| Streamlit 端口占用 | 修改 `--server.port` 参数 |
| Dashboard 打不开 | 确认防火墙未阻止 Python, 手动打开 http://localhost:8501 |
