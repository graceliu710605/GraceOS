# GraceOS Performance Analysis

**日期**: 2026-06-13

---

## Top 10 耗时 SQL

| # | 耗时 | 操作 |
|---|------|------|
| 1 | 4.82s | 重复文件大小统计 (Correlated subquery) |
| 2 | 3.99s | 重复文件全量分组 (FULL GROUP BY 1.1M rows) |
| 3 | 1.98s | 重复文件计数 (GROUP BY HAVING) |
| 4 | 1.85s | 重复文件组数 (GROUP BY HAVING subquery) |
| 5 | 1.49s | 长期未使用文件 (LIKE filters + ORDER BY) |
| 6 | 0.83s | Top100 大文件 (ORDER BY DESC) |
| 7 | 0.44s | 未使用文件统计 (WHERE last_modified) |
| 8 | 0.32s | 文件总数 HOME |
| 9 | 0.27s | 文件总数 FILE TAB |
| 10 | 0.01s | 软件列表 |

## 根因

**files 表（115万行）零索引。** 重复文件 4 个查询串行全表扫描，累计 12.6s。

## 建议

| 优先级 | 方案 | 预期 | 风险 |
|--------|------|------|------|
| P0 | C: 建索引 files(file_name/file_size/last_modified) | 13s->2s | 低 |
| P1 | A: 延迟加载 | 首页<1s | 低 |