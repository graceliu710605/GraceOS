# GraceOS V2.1 - Project File Tree

**生成日期**: 2026-06-13

---

## 根目录

`
GraceOS_V1/
├── CHANGELOG.md                    # 变更日志
├── CURRENT_SPRINT.md               # 当前 Sprint 任务
├── DEVELOPMENT_RULES.md            # 开发规范
├── INSTALL_GUIDE.md                # 安装指南
├── PROJECT_HANDOVER.md             # 项目交接文档 (入口)
├── PROJECT_OPERATING_RULES.md      # 项目运营规范
├── PROJECT_STATUS.md               # 项目状态
├── README.md                       # 产品介绍
├── ROADMAP.md                      # 路线图
├── requirements.txt                # Python 依赖
├── main.py                         # CLI 扫描入口
├── dashboard.py                    # Streamlit 主应用 (V2.1)
├── json_to_sqlite.py               # JSON -> SQLite 导入
├── software_to_sqlite.py           # 软件数据导入
├── disk_to_sqlite.py               # 磁盘数据导入
├── Start_GraceOS.bat               # 一键启动脚本
├── package.json / package-lock.json # Node 依赖
├── .gitignore
├── GraceOS_V1.zip                  # 旧版打包 (可清理)
├── dashboard_v1_backup.py          # 旧版备份 (可清理)
├── json_to_sqlite_v1.py            # 旧版 (可清理)
├── clean_sw_final.py               # 临时脚本 (可清理)
├── final_fix.py                    # 临时脚本 (可清理)
├── final_polish.py                 # 临时脚本 (可清理)
├── fix_labels.py                   # 临时脚本 (可清理)
├── simplify_sw.py                  # 临时脚本 (可清理)
├── sqlite_test.py                  # 临时测试 (可清理)
├── json_to_sqlite_smoke_test.py    # 临时测试 (可清理)
├── explorer_layout.py              # 资源管理器布局
├── database_builder.py             # 数据库构建器
├── 个人数字资产管家_Setup.exe       # 安装包
├── 个人数字资产管家_Setup_V2.1.exe  # V2.1 安装包
├── 个人数字资产管家_Portable.zip    # 便携版
├── scanners/                       # 扫描器
│   ├── software_scanner.py         # 软件扫描 (winget + 注册表)
│   ├── file_scanner.py             # 文件扫描
│   └── disk_scanner.py             # 磁盘扫描
├── analyzers/                      # 分析器
│   ├── health_scorer.py            # 健康评分引擎
│   ├── large_file_analyzer.py      # 大文件分析
│   └── software_search.py          # 软件搜索
├── config/                         # 配置文件
├── reports/                        # 报告
├── screenshots/                    # 截图
├── tests/                          # 测试
├── node_modules/                   # Node 依赖
├── setup_build/                    # 安装构建
│   ├── setup.nsi                   # NSIS 安装脚本
│   ├── build.ps1                   # 构建脚本
│   ├── README_BUILD.md             # 构建说明
│   ├── python313._pth.template     # Python 路径模板
│   ├── app/                        # 应用副本
│   │   ├── dashboard.py
│   │   ├── main.py
│   │   ├── analyzers/
│   │   ├── scanners/
│   │   └── 启动个人数字资产管家.bat
│   └── build/                      # 构建输出
│       ├── app/
│       └── python/
└── docs/                           # 文档中心
    ├── BETA_USER_FEEDBACK.md       # Beta 用户反馈
    ├── PRD.md                      # 产品需求文档
    ├── DATABASE.md                 # 数据库设计
    ├── BUSINESS_PLAN.md            # 商业计划
    ├── QA_REPORT.md                # 测试报告
    ├── UI_REVIEW.md                # UI 巡检报告
    ├── RELEASE_CHECKLIST.md        # 发布检查清单
    ├── RELEASE_NOTE.md             # 发布说明
    ├── V2_1_SPRINT_REPORT.md       # V2.1 Sprint 报告
    ├── V2_RC2_FINAL_REPORT.md      # V2 RC2 最终报告
    ├── image.png / image-1.png     # 反馈截图
    ├── templates/                  # 文档模板
    │   ├── BETA_USER_FEEDBACK_TEMPLATE.md
    │   ├── CURRENT_SPRINT_TEMPLATE.md
    │   ├── INSTALL_TEST_REPORT_TEMPLATE.md
    │   ├── PROJECT_HANDOVER_TEMPLATE.md
    │   └── PROJECT_STATUS_TEMPLATE.md
    └── archive/                    # 历史归档
        ├── BRANDING_UPDATE_REPORT.md
        ├── DEMO_MODE_DESIGN.md
        ├── GIT_NETWORK_FIX_REPORT.md
        ├── GraceOS_V2_ARCHITECTURE.md
        ├── GraceOS_V2_DATABASE.md
        ├── GraceOS_V2_PRD.md
        ├── INSTALL_PACKAGE_PLAN.md
        ├── PACKAGE_PLAN.md
        ├── PORTABLE_BUILD_REPORT.md
        ├── PORTABLE_STATUS.md
        ├── RULES_GAP_ANALYSIS.md
        ├── SETUP_BUILD_REPORT.md
        ├── STARTUP_FAILURE_ANALYSIS.md
        └── UI_DESIGN.md
`

## 文档用途速查

| 文档 | 用途 | 谁读 |
|------|------|------|
| PROJECT_HANDOVER.md | 项目入口，新会话必读 | AI Agent |
| CURRENT_SPRINT.md | 当前开发任务 | AI Agent / 开发者 |
| PROJECT_STATUS.md | 项目当前状态 | AI Agent |
| ROADMAP.md | 路线图 | 产品负责人 |
| DEVELOPMENT_RULES.md | 开发规范 | AI Agent |
| CHANGELOG.md | 变更日志 | 所有人 |
| docs/PRD.md | 产品需求 | 产品负责人 |
| docs/BETA_USER_FEEDBACK.md | Beta 反馈 | 产品负责人 |
| docs/templates/ | 文档模板 | AI Agent |

## 可清理文件

以下为旧备份/临时文件，确认无用后可删除：

| 文件 | 说明 |
|------|------|
| dashboard_v1_backup.py | V1 备份 |
| json_to_sqlite_v1.py | 旧版导入器 (含 DROP TABLE) |
| clean_sw_final.py | 临时修复脚本 |
| inal_fix.py | 临时修复脚本 |
| inal_polish.py | 临时修复脚本 |
| ix_labels.py | 临时修复脚本 |
| simplify_sw.py | 临时修复脚本 |
| sqlite_test.py | 临时测试 |
| json_to_sqlite_smoke_test.py | 临时测试 |
| GraceOS_V1.zip | 旧版打包 |