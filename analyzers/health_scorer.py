"""
GraceOS V2 Health Scorer
计算数字资产健康评分（0-100）
"""
import sqlite3
from datetime import date

DB_FILE = r"E:\创业项目\GraceOS\09_Database\graceos.db"

def calculate(conn=None):
    """计算并保存健康评分，返回评分字典"""
    close_later = False
    if conn is None:
        conn = sqlite3.connect(DB_FILE)
        close_later = True

    try:
        cur = conn.cursor()

        # File duplication
        cur.execute("SELECT COUNT(*) FROM files")
        total_files = cur.fetchone()[0] or 1
        cur.execute("SELECT COALESCE(SUM(cnt),0) FROM (SELECT COUNT(*) AS cnt FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1)")
        dup_files = cur.fetchone()[0] or 0
        cur.execute("SELECT COUNT(*) FROM (SELECT file_name, file_size FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1)")
        dup_count = cur.fetchone()[0] or 0
        cur.execute("SELECT COALESCE(SUM(file_size),0) FROM files WHERE (file_name, file_size) IN (SELECT file_name, file_size FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1)")
        dup_mb = round(cur.fetchone()[0] / 1048576, 2)

        # Unused files (>90 days)
        cur.execute("SELECT COUNT(*), COALESCE(SUM(file_size),0) FROM files WHERE last_modified < date('now','-90 days')")
        unused_count, unused_bytes = cur.fetchone()
        unused_mb = round((unused_bytes or 0) / 1048576, 2)

        # Disk
        cur.execute("SELECT usage_pct FROM disks WHERE name='C'")
        row = cur.fetchone()
        c_pct = row[0] if row else 50

        # Software
        cur.execute("SELECT COUNT(*) FROM software")
        sw_count = cur.fetchone()[0] or 0
        cur.execute("SELECT COUNT(*) FROM (SELECT name FROM software GROUP BY name HAVING COUNT(*)>1)")
        sw_multi = cur.fetchone()[0] or 0

        # Scoring (each dimension 25 max, total 100)
        dup_ratio = dup_files / max(total_files, 1)
        dup_score = max(0, min(25, int(25 * (1 - dup_ratio * 8))))

        unused_gb = unused_mb / 1024
        unused_score = max(0, min(25, int(25 * (1 - min(unused_gb, 100) / 100))))

        disk_score = max(0, min(25, int(25 * (1 - max(0, c_pct - 70) / 30))))

        sw_score = max(0, min(25, 25 - min(sw_multi * 3, 25)))

        total = dup_score + unused_score + disk_score + sw_score

        cur.execute("""
            INSERT INTO health_scores
            (score_date, total_score, file_dup_score, file_unused_score, disk_score, sw_score,
             dup_count, dup_files, dup_size_mb, unused_count, unused_size_mb,
             c_usage_pct, sw_count, sw_multi_ver, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now','localtime'))
        """, (date.today().isoformat(), total, dup_score, unused_score, disk_score, sw_score,
              dup_count, dup_files, dup_mb, unused_count, unused_mb,
              c_pct, sw_count, sw_multi))
        conn.commit()

        return {
            "total": total, "dup_score": dup_score, "unused_score": unused_score,
            "disk_score": disk_score, "sw_score": sw_score,
            "dup_count": dup_count, "dup_files": dup_files, "dup_mb": dup_mb,
            "unused_count": unused_count, "unused_mb": unused_mb,
            "c_pct": c_pct, "sw_count": sw_count, "sw_multi": sw_multi,
            "total_files": total_files
        }
    finally:
        if close_later:
            conn.close()

def get_latest(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM health_scores ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    if not row: return None
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, row))

def get_history(conn, days=7):
    import pandas as pd
    return pd.read_sql_query(
        "SELECT score_date, total_score, file_dup_score, file_unused_score, disk_score, sw_score FROM health_scores ORDER BY score_date DESC LIMIT ?",
        conn, params=[days]
    )

if __name__ == "__main__":
    result = calculate()
    print(f"Health Score: {result['total']}/100")
    print(f"  Dup: {result['dup_score']}/25, Unused: {result['unused_score']}/25")
    print(f"  Disk: {result['disk_score']}/25, SW: {result['sw_score']}/25")
