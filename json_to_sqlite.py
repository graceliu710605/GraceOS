import sqlite3
import ijson

JSON_FILE = r"E:\创业项目\GraceOS\09_Database\file_assets\file_inventory.json"

DB_FILE = r"E:\创业项目\GraceOS\09_Database\graceos.db"

print("连接数据库...")

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
id INTEGER PRIMARY KEY AUTOINCREMENT,
file_name TEXT,
file_path TEXT,
file_size INTEGER,
last_modified TEXT,
file_type TEXT
)
""")

conn.commit()

print("开始导入JSON -> SQLite")

count = 0

with open(JSON_FILE, "rb") as f:

```
objects = ijson.items(f, "item")

batch = []

for item in objects:

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
```

if batch:

```
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
```

cursor.execute(
"SELECT COUNT(*) FROM files"
)

total = cursor.fetchone()[0]

print()
print("导入完成")
print(f"数据库记录数: {total:,}")

conn.close()
