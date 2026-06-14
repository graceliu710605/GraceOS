"""
磁盘资产导入器: JSON → SQLite

从 disk_inventory.json (PowerShell Get-PSDrive 原始输出) 读取数据，
转换为 GB 单位后写入 graceos.db 的 disks 表。
"""
import json
import sqlite3
from pathlib import Path

DB_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\graceos.db"
JSON_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\disk_assets\disk_inventory.json"


def create_table(conn):
    """创建 disks 表（如不存在）。"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS disks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            total_gb    REAL,
            used_gb     REAL,
            free_gb     REAL,
            usage_pct   REAL,
            root        TEXT,
            description TEXT,
            scan_time   TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_disks_name ON disks(name)")


def import_data(conn, data):
    """导入磁盘数据，全量替换旧数据。"""
    conn.execute("DELETE FROM disks")

    rows = []
    for disk in data:
        name = disk.get("Name", "?")
        used_bytes = disk.get("Used") or 0
        free_bytes = disk.get("Free") or 0
        total_bytes = used_bytes + free_bytes

        total_gb = total_bytes / (1024**3)
        used_gb = used_bytes / (1024**3)
        free_gb = free_bytes / (1024**3)
        usage_pct = (used_gb / total_gb * 100) if total_gb > 0 else 0

        root = disk.get("Root", "")
        description = disk.get("Description", "")

        rows.append((name, round(total_gb, 2), round(used_gb, 2),
                     round(free_gb, 2), round(usage_pct, 1),
                     root, description, None))

    conn.executemany(
        """INSERT INTO disks
           (name, total_gb, used_gb, free_gb, usage_pct, root, description, scan_time)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        rows
    )
    conn.commit()
    return len(rows)


def main():
    json_path = Path(JSON_FILE)
    if not json_path.exists():
        print(f"JSON 文件不存在: {JSON_FILE}")
        print("请先运行: python scanners/disk_scanner.py")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        data = [data]

    print(f"读取到 {len(data)} 个磁盘记录")

    conn = sqlite3.connect(DB_FILE)
    try:
        create_table(conn)
        count = import_data(conn, data)
        print(f"成功导入 {count} 条记录到 disks 表")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
