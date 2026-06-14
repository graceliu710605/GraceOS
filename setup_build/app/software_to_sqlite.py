"""
软件资产导入器: JSON -> SQLite
"""
import json, sqlite3
from pathlib import Path

DB_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\graceos.db"
JSON_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\software_assets\software_inventory.json"

def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS software (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, id_name TEXT, version TEXT,
            source TEXT, publisher TEXT, install_date TEXT,
            install_path TEXT, size_bytes INTEGER,
            raw TEXT, scan_time TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_software_name ON software(name)")

def import_data(conn, data):
    conn.execute("DELETE FROM software")
    rows = []
    for sw in data:
        rows.append((
            sw.get("name",""), sw.get("id",""), sw.get("version",""),
            sw.get("source",""), sw.get("publisher"), sw.get("install_date"),
            sw.get("install_path"), sw.get("size_bytes"),
            sw.get("raw"), sw.get("scan_time","")
        ))
    conn.executemany("INSERT INTO software (name,id_name,version,source,publisher,install_date,install_path,size_bytes,raw,scan_time) VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
    conn.commit()
    return len(rows)

def main():
    p = Path(JSON_FILE)
    if not p.exists():
        print(f"JSON not found: {JSON_FILE}")
        return
    with open(p,"r",encoding="utf-8") as f: data = json.load(f)
    print(f"Read {len(data)} records")
    conn = sqlite3.connect(DB_FILE)
    try:
        create_table(conn)
        print(f"Imported {import_data(conn, data)} records")
    finally: conn.close()

if __name__=="__main__": main()
