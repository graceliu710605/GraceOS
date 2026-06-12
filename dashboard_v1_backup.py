import streamlit as st
import sqlite3
import pandas as pd

DB_FILE = r"E:\创业项目\GraceOS\09_Database\graceos.db"

st.set_page_config(
    page_title="GraceOS V3",
    layout="wide"
)

st.title("GraceOS V3")
st.subheader("SQLite Edition")

conn = sqlite3.connect(DB_FILE)

# =========================
# 首页统计
# =========================

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM files"
)

file_count = cursor.fetchone()[0]

col1, col2 = st.columns(2)

col1.metric(
    "文件总数",
    f"{file_count:,}"
)

col2.metric(
    "数据库",
    "SQLite"
)

st.divider()

# =========================
# 文件搜索
# =========================

st.header("文件搜索")

keyword = st.text_input(
    "输入文件名关键字"
)

if keyword:

    sql = """
    SELECT
        file_name,
        file_path,
        ROUND(file_size/1024.0/1024.0,2)
    FROM files
    WHERE file_name LIKE ?
    LIMIT 100
    """

    df = pd.read_sql_query(
        sql,
        conn,
        params=[f"%{keyword}%"]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

st.divider()

# =========================
# Top100大文件
# =========================

st.header("Top100大文件")

sql = """
SELECT
    file_name,
    file_path,
    ROUND(file_size/1024.0/1024.0,2) AS size_mb
FROM files
ORDER BY file_size DESC
LIMIT 100
"""

df_big = pd.read_sql_query(
    sql,
    conn
)

st.dataframe(
    df_big,
    use_container_width=True
)

st.divider()

# =========================
# 重复文件统计
# =========================

st.header("重复文件统计")

sql = """
SELECT
    file_name,
    file_size,
    COUNT(*) AS cnt
FROM files
GROUP BY file_name,file_size
HAVING cnt > 1
ORDER BY cnt DESC
LIMIT 100
"""

df_dup = pd.read_sql_query(
    sql,
    conn
)

st.dataframe(
    df_dup,
    use_container_width=True
)

st.divider()

# =========================
# 长期未使用文件
# =========================

st.header("长期未使用文件")

sql = """
SELECT
    file_name,
    file_path,
    last_modified
FROM files
ORDER BY last_modified ASC
LIMIT 100
"""

df_old = pd.read_sql_query(
    sql,
    conn
)

st.dataframe(
    df_old,
    use_container_width=True
)

conn.close()