# GraceOS V1 启动失败根因分析

> 日期: 2026-06-13
> 版本: V2 Beta
> 严重级别: P0 阻塞

---

## 1. 现象

1. Setup.exe 安装成功
2. 浏览器自动打开 http://localhost:8501
3. 页面显示 "localhost 拒绝连接"
4. 安装目录存在，文件完整
5. port 8501 无监听进程

**结论**: Streamlit 服务未启动，浏览器打开但无后端。

---

## 2. 诊断过程

### 检查项结果

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 安装目录完整结构 | 通过 | 10,133 文件，Python 3.13.13 embedded + streamlit 1.58 + 所有依赖 |
| dashboard.py 存在 | 通过 | `app/dashboard.py` 存在，19KB |
| Python 环境 | 通过 | embedded python.exe 可正常运行 |
| Streamlit 可用 | 通过 | `..\Scripts\streamlit.exe --version` 输出 "Streamlit, version 1.58.0" |
| 依赖完整 | 通过 | pandas, pywin32, GitPython 等均已安装 |
| BAT 文件 | **不通过** | 两个致命 Bug |

---

## 3. 根因分析

### 安装目录结构

```
E:\Program Files (x86)\个人数字资产管家\
├── python.exe          ← Python 3.13.13 embedded
├── python313.dll
├── Scripts\
│   └── streamlit.exe   ← Streamlit 启动器
├── Lib\site-packages\  ← 所有依赖
└── app\
    ├── dashboard.py
    ├── scanners\
    ├── analyzers\
    └── 启动个人数字资产管家.bat   ← 问题文件
```

### Bug 1: Python 路径错误 (致命)

**BAT 原文:**
```bat
"%~dp0..\python\python.exe" "%~dp0dashboard.py"
```

解析: `%~dp0` = `E:\...\app\`，`..` = 父目录(`个人数字资产管家\`)
最终路径: `E:\...\个人数字资产管家\python\python.exe` (不存在)

**实际位置:**
`E:\...\个人数字资产管家\python.exe` (根目录，无 `python\` 子目录)

**验证:**
```
cmd> "E:\...\个人数字资产管家\app\..\python\python.exe"
系统找不到指定的路径。
```

### Bug 2: 启动命令错误 (致命)

**BAT 原文:**
```bat
python.exe dashboard.py
```

Streamlit 脚本需要 `streamlit run` 命令才能启动 Web 服务。直接用 `python.exe` 运行只在脚本上下文执行，不会启动 HTTP 服务器。

**正确命令:**
```bat
python.exe -m streamlit run dashboard.py --server.port 8501
```

**验证:**
```
# 错误方式
cmd> python dashboard.py           → 立即退出，无监听端口

# 正确方式
cmd> python -m streamlit run dashboard.py --server.port 8501
→ HTTP 200, Server: uvicorn, 端口 8501 LISTENING
```

### 两个 Bug 的关系

Bug 1 直接导致 BAT 执行失败（找不到文件），Bug 2 是即使路径正确也不会启动服务。两者独立且均为致命：

```
双击快捷方式
  ↓
BAT 执行: "..\python\python.exe" dashboard.py
  ↓
Bug 1: ..\python\python.exe 不存在
  ↓
系统报错: 找不到文件
  ↓
浏览器打开 (start http 在 python 命令之前执行)
  ↓
localhost:8501 → 拒绝连接
```

---

## 4. 修复方案

### 修复后的 BAT

```bat
@echo off
cd /d "%~dp0"
start "" http://localhost:8501
"%~dp0..\python.exe" -m streamlit run "%~dp0dashboard.py" --server.port 8501
```

修改内容:
1. `..\python\python.exe` → `..\python.exe` (修正路径)
2. `"dashboard.py"` → `-m streamlit run "dashboard.py" --server.port 8501` (修正启动命令)

---

## 5. 验证结果

```
Streamlit LISTENING on port 8501 after 4 seconds
HTTP 200 - Server: uvicorn
Content length: 1522 bytes
=== VERIFICATION PASSED ===
```

| 验证项 | 状态 | 结果 |
|--------|------|------|
| 端口 8501 监听 | 通过 | TCP 0.0.0.0:8501 LISTENING |
| HTTP 请求 | 通过 | 200 OK |
| 服务响应 | 通过 | HTML 1522 bytes, Server: uvicorn |
| 首次运行扫描 | 通过 | software + disk scan 正常执行 |
| 浏览器访问 | 通过 | Dashboard 首页正常显示 |

---

## 6. 影响范围

| 影响 | 说明 |
|------|------|
| 当前安装 | 已修复，系统正常运行 |
| Setup.exe | **仍包含错误的 BAT**，重新安装会再次出现相同问题 |
| 便携版 ZIP | 不受影响（使用 `streamlit run` 正确命令） |
| 项目源码 BAT | 不受影响（`Start_GraceOS.bat` 使用正确命令） |

---

## 7. 后续行动

| 优先级 | 行动 | 说明 |
|--------|------|------|
| P0 | 修复已安装的 BAT | **已完成** - 当前系统可正常使用 |
| P0 | 重建 Setup.exe | 修复 NSIS 脚本中的 BAT 生成逻辑，重建安装包 |
| P1 | 保留 NSIS 源脚本 | 将 .nsi 脚本纳入版本控制，避免下次重建 |

### 重建 Setup.exe 要点

NSIS 脚本中生成 BAT 的部分需要改为:
```nsis
; 错误写法:
FileWrite $0 '"$INSTDIR\python\python.exe" "dashboard.py"$\r$\n'

; 正确写法:
FileWrite $0 '"$INSTDIR\python.exe" -m streamlit run "$INSTDIR\app\dashboard.py" --server.port 8501$\r$\n'
```

由于 NSIS .nsi 源文件未保留在项目中，重建时需要重新编写 NSIS 安装脚本。

---

## 8. 总结

- **根因**: 安装包内启动 BAT 有两个独立致命错误
  1. Python 可执行文件路径多了一层 `python\` 子目录
  2. 直接用 `python.exe` 运行而非 `python -m streamlit run`
- **当前状态**: 已安装系统修复完成，可正常使用
- **阻塞项**: Setup.exe 需重建，否则全新安装仍会失败
