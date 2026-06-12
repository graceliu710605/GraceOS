# GraceOS 开发规范

## 产品定位

GraceOS 是数字资产管理系统。

目标：**发现问题 → 分析问题 → 解决问题**

### 优先开发
- 文件资产管理
- 软件资产管理
- 磁盘资产管理
- AI 分析建议
- 自动整理
- 资产处理

### 暂缓开发（保留页面，不继续开发）
- 知识库中心
- Prompt 中心
- 项目中心
- 工作流中心

---

## 开发完成后必须执行

每次开发完成后更新以下文件：

| 文件 | 说明 |
|------|------|
| `PROJECT_STATUS.md` | 项目状态（当前版本/已完成功能/待办事项） |
| `docs/UI_REVIEW.md` | UI 巡检报告 |
| `docs/QA_REPORT.md` | 测试报告 |
| `docs/RELEASE_NOTE.md` | 发布说明 |

---

## 删除安全规范

所有删除操作必须：

1. **显示预计删除数量**
2. **显示预计释放空间**
3. **操作前确认**

支持三种删除模式：

| 模式 | 说明 |
|------|------|
| 回收站 | 移至 `E:\回收站` 目录（可恢复） |
| 直接删除 | 永久删除（谨慎使用） |
| 归档 | 移至 `E:\归档` 目录（保留结构） |

---

## 白名单机制

支持设置**永不清理目录**：

- 知识库（`E:\知识库obsidian`）
- 创业项目（`E:\创业项目`）
- 照片目录
- 用户自定义目录

---

## 系统保护

禁止推荐删除以下系统路径：

- `C:\Windows`
- `C:\Windows\System32`
- `pagefile.sys`
- `hiberfil.sys`
- `swapfile.sys`
- `C:\Program Files\WindowsApps`

---

## Git 规范

每完成一个模块：

```bash
git add .
git commit -m "描述本次变更"
```

Commit 信息格式：`模块名: 变更说明`

---

## 目录结构

```
GraceOS_V1/
├── dashboard.py          # 主应用
├── main.py               # 入口
├── scanners/             # 扫描器
├── analyzers/            # 分析器
├── docs/                 # 设计文档和报告
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE.md
│   ├── UI_REVIEW.md
│   ├── QA_REPORT.md
│   └── RELEASE_NOTE.md
├── screenshots/          # 截图
├── PROJECT_STATUS.md     # 项目状态
├── ROADMAP.md            # 路线图
├── DEVELOPMENT_RULES.md  # 开发规范（本文件）
└── CHANGELOG.md          # 变更日志
```
