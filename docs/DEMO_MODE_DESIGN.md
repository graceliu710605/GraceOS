# GraceOS Demo Mode 设计方案

> 设计日期: 2026-06-12 | 版本: V2.1 规划
> 状态: 设计阶段（不实现）

## 目标

解决首次启动体验问题：用户不想等扫描就能看到系统全貌。

## 方案设计

### 启动流程

```
双击 Start_GraceOS.bat
    ↓
┌──────────────────────────────────┐
│    Welcome to GraceOS            │
│                                  │
│  🔍 体验模式 (推荐)              │
│  使用示例数据，立即体验          │
│  无需扫描，2秒进入系统           │
│                                  │
│  ⚡ 真实扫描模式                  │
│  扫描本机数据，获取真实报告       │
│  预计 2-5 分钟                   │
│                                  │
│  □ 下次不再询问                   │
└──────────────────────────────────┘
    ↓
Dashboard 启动
```

### 体验模式数据

| 维度 | 示例值 | 说明 |
|------|--------|------|
| 文件总数 | 152,847 | 模拟数据 |
| 重复文件 | 12,034 | 模拟 |
| 软件总数 | 48 | 模拟 |
| 磁盘 | C: 256GB / D: 512GB | 模拟 |
| 健康评分 | 72/100 | 演示评分逻辑 |

### 技术实现

```python
# demo_mode.py (伪代码)

DEMO_DATA = {
    "files": [
        {"name": "report_2024.pdf", "size_mb": 2.3, "path": "C:/Documents/report_2024.pdf"},
        ...
    ],
    "software": [
        {"name": "VS Code", "version": "1.95", "install_date": "2024-12-01"},
        ...
    ],
    "health": {"total": 72, "dup": 20, "unused": 18, "disk": 19, "sw": 15},
}

def is_demo_mode():
    return os.path.exists("demo_mode.lock")

def enable_demo():
    # Create demo_mode.lock
    # Return True
    pass
```

### UI 改动

1. **启动选择页**: 新 Streamlit 页面或 .bat 对话框
2. **Dashboard 顶部标签**: "🔍 Demo Mode" 或 "⚡ Live Mode"
3. **数据切换按钮**: 在设置页面切换模式

### 开发计划

| 阶段 | 内容 | 时间 |
|------|------|------|
| Phase 1 | 设计确认 | ✅ |
| Phase 2 | 实现 demo 数据模块 | 0.5天 |
| Phase 3 | 实现模式切换 | 0.5天 |
| Phase 4 | 测试 + 文档 | 0.5天 |

### 注意事项

- Demo 模式不连接真实数据库
- 模式切换后需重启 Dashboard
- 设置"下次不再询问"后自动选择上次模式
