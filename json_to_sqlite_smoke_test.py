import sqlite3
import ijson

JSON_FILE = r"E:\创业项目\GraceOS\09_Database\file_assets\file_inventory.json"
DB_FILE = r"E:\创业项目\GraceOS\09_Database\graceos.db"

print("连接数据库...")

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

conn.commit()

print("开始导入前10000条记录...")

count = 0

with open(JSON_FILE, "rb") as f:

    for item in ijson.items(f, "item"):

        cursor.execute(
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
            (
                item.get("file_name"),
                item.get("file_path"),
                item.get("file_size"),
                item.get("last_modified"),
                item.get("file_type")
            )
        )

        count += 1

        if count % 1000 == 0:
            print(f"已导入 {count} 条")

        if count >= 10000:
            break

conn.commit()

cursor.execute("SELECT COUNT(*) FROM files")

total = cursor.fetchone()[0]

print()
print(f"数据库记录数: {total}")
print("测试完成")

conn.close()