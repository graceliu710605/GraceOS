# 便携版构建报告

> 日期: 2026-06-12 | 输出: 个人数字资产管家_Portable.zip

## 构建结果

| 指标 | 值 |
|------|-----|
| 文件数 | 17 |
| 压缩大小 | 18 KB |
| 依赖 | Python 3.10+ (用户需安装) |

## 包含内容

```
个人数字资产管家_Portable/
├── Start_个人数字资产管家.bat   # 双击启动
├── README_快速开始.txt          # 使用说明
├── dashboard.py                # 主应用
├── software_to_sqlite.py       # 软件导入
├── disk_to_sqlite.py           # 磁盘导入
├── json_to_sqlite.py           # 文件导入
├── requirements.txt            # Python依赖
├── scanners/ (3个扫描器)
└── analyzers/ (6个分析器+评分引擎)
```

## 排除

- __pycache__/, node_modules/, screenshots/, docs/, .git/, 旧备份文件

## 用户流程

```
下载zip -> 解压 -> 双击 Start_个人数字资产管家.bat -> 使用
```

## 首次启动

自动完成: 安装依赖 -> 扫描软件/磁盘 -> 导入SQLite -> 启动Dashboard (约2分钟)
