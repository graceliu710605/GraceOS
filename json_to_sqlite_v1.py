import sqlite3
import ijson
import time

JSON_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\file_assets\file_inventory.json"
DB_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\graceos.db"

print("连接数据库...")

start_time = time.time()

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS files")

cursor.execute("""
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT,
    file_path TEXT,
    file_size INTEGER,
    last_modified TEXT,
    file_type TEXT
)
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_filename
ON files(file_name)
""")

conn.commit()

print("开始导入全部文件...")

count = 0
batch = []

with open(JSON_FILE, "rb") as f:

    for item in ijson.items(f, "item"):

        batch.append(
            (
                item.get("file_name"),
                item.get("file_path"),
                item.get("file_size"),
                item.get("last_modified"),
                item.get("file_type")
            )
        )

        if len(batch) >= 5000:

            cursor.executemany(
                """
                INSERT INTO files
                (
                    file_name,
                    file_path,
                    file_size,
                    last_modified,
                    file_type
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                batch
            )

            conn.commit()

            count += len(batch)

            print(f"已导入 {count:,} 条")

            batch = []

if batch:

    cursor.executemany(
        """
        INSERT INTO files
        (
            file_name,
            file_path,
            file_size,
            last_modified,
            file_type
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        batch
    )

    conn.commit()

    count += len(batch)

cursor.execute("SELECT COUNT(*) FROM files")

total = cursor.fetchone()[0]

elapsed = round(time.time() - start_time, 1)

print()
print("===================================")
print(f"数据库记录数: {total:,}")
print(f"耗时: {elapsed} 秒")
print("SQLite导入完成")
print("===================================")

conn.close()