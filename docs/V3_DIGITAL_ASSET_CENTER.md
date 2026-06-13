# V3 数字资产中心 — 需求与 UI 设计

**版本**: V3 Alpha
**日期**: 2026-06-13
**状态**: UI 已确认（方案C），等待 V2.1 稳定后进入开发

---

## 产品定位

**个人数字资产入口中心** — 统一管理所有互联网平台登录入口和访问凭证。

不是固定网址导航。用户可完全自定义。

---

## 1. 最终 UI 设计稿（方案C：导航版）

### 页面布局

```
┌──────────────────────────────────────────────────────────┐
│  🌐 数字资产中心                                          │
│                                                          │
│ ┌──────────────┬───────────────────────────────────────┐ │
│ │ 分类导航      │  资产列表                              │ │
│ │              │                                       │ │
│ │ 📱 内容平台 (5)│┌──────┬──────┬──────────┬────┬────┐  │ │
│ │              ││ 名称  │ 网址  │ 账号     │备注 │操作│  │ │
│ │ 🤖 AI平台 (5) │├──────┼──────┼──────────┼────┼────┤  │ │
│ │              ││B站   │bili..│—         │视频 │🚀✏️🗑️│  │ │
│ │ ☁️ 云服务 (5) ││小红书│xia.. │myaccount│图文 │🚀✏️🗑️│  │ │
│ │              ││抖音  │dou.. │—         │短视│🚀✏️🗑️│  │ │
│ │ 💻 开发平台(3)│└──────┴──────┴──────────┴────┴────┘  │ │
│ │              │                                       │ │
│ │ 📊 办公平台(4)│ [新增分类]  [新增资产]       共 N 条   │ │
│ │              │                                       │ │
│ │ ➕ 自定义 (0) │                                       │ │
│ └──────────────┴───────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### 左侧分类树

5 个系统预置分类 + 1 个用户自定义分类：

```
📱  内容平台 (5)        ← 点击筛选
🤖  AI 平台 (5)
☁️  云服务 (5)
💻  开发平台 (3)
📊  办公平台 (4)
──────────────
➕ 自定义分类 (0)        ← 用户可新增子分类
```

- 点击分类 → 筛选右侧列表
- 「全部」恢复显示所有
- 自定义分类下用户可新增子分类（如：猎头平台、金融平台等）

### 右侧资产列表

| 列 | 字段 | 说明 |
|----|------|------|
| 名称 | name | 可点击打开 URL |
| 网址 | url | 显示简短 URL |
| 账号 | username | —（无则显示） |
| 备注 | remark | 简短描述 |
| 操作 | — | 🚀 打开 ✏️ 编辑 🗑️ 删除 |

### 新增/编辑弹窗

```
┌──────────────────────────────────────┐
│  新增资产 / 编辑资产                  │
│                                      │
│  名称 *      [_______________]       │
│  网址 *      [_______________]       │
│  分类 *      [内容平台         ▼]    │
│  账号        [_______________]       │
│  密码/Token  [_______________]       │
│  API Key     [_______________]       │
│  备注        [_______________]       │
│                                      │
│  ── 新增分类（如分类不存在） ──       │
│  新分类名    [_______________]       │
│                                      │
│          [取消]    [保存]            │
└──────────────────────────────────────┘
```

- 分类下拉包含所有已有分类 + 「新增分类」选项
- 选「新增分类」时下方出现新分类名输入框
- 保存后分类自动出现在左侧树

---

## 2. 系统预置资产（首次安装自动导入）

共 24 个预置资产，仅含名称和 URL，账号/密码/备注为空，用户自行补充。

### 📱 内容平台 (5)

| 名称 | URL |
|------|-----|
| 小红书 | https://www.xiaohongshu.com |
| B站 | https://www.bilibili.com |
| YouTube | https://www.youtube.com |
| 抖音 | https://www.douyin.com |
| 视频号 | https://channels.weixin.qq.com |

### 🤖 AI 平台 (5)

| 名称 | URL |
|------|-----|
| ChatGPT | https://chat.openai.com |
| Claude | https://claude.ai |
| DeepSeek | https://chat.deepseek.com |
| Gemini | https://gemini.google.com |
| 豆包 | https://www.doubao.com |

### ☁️ 云服务 (5)

| 名称 | URL |
|------|-----|
| 腾讯云 | https://cloud.tencent.com |
| 阿里云 | https://aliyun.com |
| 七牛云 | https://www.qiniu.com |
| Cloudflare | https://dash.cloudflare.com |
| 华为云 | https://www.huaweicloud.com |

### 💻 开发平台 (3)

| 名称 | URL |
|------|-----|
| GitHub | https://github.com |
| VS Code | https://code.visualstudio.com |
| Docker Hub | https://hub.docker.com |

### 📊 办公平台 (4)

| 名称 | URL |
|------|-----|
| 飞书 | https://www.feishu.cn |
| Notion | https://www.notion.so |
| Obsidian Sync | https://obsidian.md |
| 企业微信 | https://work.weixin.qq.com |

---

## 3. 数据库设计

### 表: digital_assets

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER PK | ✅ | 自增 |
| category | TEXT | ✅ | 分类名 |
| name | TEXT | ✅ | 资产名称 |
| url | TEXT | ✅ | 完整 URL |
| username | TEXT | — | 用户名 |
| password | TEXT | — | 密码/Token |
| api_key | TEXT | — | API Key |
| remark | TEXT | — | 备注 |
| sort_order | INTEGER | — | 排序 |
| created_at | TEXT | — | ISO |
| updated_at | TEXT | — | ISO |

### 建表 SQL（仅供引用，禁止执行）

```sql
CREATE TABLE IF NOT EXISTS digital_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    username TEXT,
    password TEXT,
    api_key TEXT,
    remark TEXT,
    sort_order INTEGER DEFAULT 0,
    created_at TEXT,
    updated_at TEXT
);
```

### 预置数据首次导入

首次启动时检查 `digital_assets` 为空 → 自动插入 24 条预置记录。已存在数据 → 跳过。

---

## 4. 用户操作流程

- 新增资产：点击新建 → 填表单 → 保存
- 编辑资产：点击 ✏️ → 修改 → 保存
- 删除资产：点击 🗑️ → 确认 → 删除
- 打开网址：点击 🚀 或名称 → `webbrowser.open(url)`
- 分类筛选：左侧点击分类 → 右侧过滤
- 新增分类：弹窗中选「新增分类」→ 输入名称 → 保存

---

## 5. 风险评估

| 评估项 | 风险 |
|--------|------|
| 影响现有模块 | 🟢 无 — 仅新增 Tab |
| 影响数据库 | 🟢 低 — 新表，不影响现有 |
| 影响文件管理 | 🟢 无 |
| 影响软件管理 | 🟢 无 |

---

## 6. 当前状态

- ✅ UI 方案确认（方案C）
- ✅ 系统预置资产设计
- ✅ 数据库设计
- ✅ 自定义分类支持
- ⏳ 等待 V2.1 稳定
- ⏳ 等待 Grace 确认 → 启动开发