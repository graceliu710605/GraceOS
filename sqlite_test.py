import sqlite3

conn = sqlite3.connect("graceos.db")

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

cursor.execute("""
INSERT INTO files
(
    file_name,
    file_path,
    file_size,
    last_modified,
    file_type
)
VALUES
(
    'test.xlsx',
    'E:\\test.xlsx',
    12345,
    '2026-06-05',
    '.xlsx'
)
""")

conn.commit()

cursor.execute("SELECT * FROM files")

rows = cursor.fetchall()

print(rows)

conn.close()