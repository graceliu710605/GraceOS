import re

P = r"e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1\dashboard.py"
with open(P, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Remove extra count queries (publisher/date/size)
old_queries = '''        cursor.execute(
            "SELECT COUNT(*) FROM software WHERE publisher IS NOT NULL AND publisher != ''"
        )
        sw_with_publisher = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM software WHERE install_date IS NOT NULL AND install_date != ''"
        )
        sw_with_date = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM software WHERE size_bytes IS NOT NULL AND size_bytes > 0"
        )
        sw_with_size = cursor.fetchone()[0]

        st.metric("\\u8f6f\\u4ef6\\u603b\\u6570", f"{sw_count}")
        st.caption(f"\\u6709\\u53d1\\u5e03\\u5546: {sw_with_publisher} | \\u6709\\u5b89\\u88c5\\u65e5\\u671f: {sw_with_date} | \\u6709\\u5927\\u5c0f: {sw_with_size}")'''

new_metric = '''        st.metric("\\u8f6f\\u4ef6\\u603b\\u6570", f"{sw_count}")'''

c = c.replace(old_queries, new_metric)

# 2. Simplify _render_software_rows: remove source column
old_sw = '''def _render_software_rows(df_sw, prefix):
    import subprocess as _sp, os as _os2
    for idx, row in df_sw.iterrows():
        bk = f"{prefix}_{idx}"
        nm = row.get("name", "?")
        dt = row.get("install_date") or "-"
        src = row.get("source") or ""
        cols = st.columns([3, 1, 4])
        if cols[0].button(nm, key=f"swbtn_{bk}", use_container_width=True):
            pf = _os2.environ.get("ProgramFiles", "C:\\\\Program Files")
            _open_folder(pf)
        cols[1].caption(dt)
        cols[2].caption(src)'''

new_sw = '''def _render_software_rows(df_sw, prefix):
    import os as _os2
    for idx, row in df_sw.iterrows():
        bk = f"{prefix}_{idx}"
        nm = row.get("name", "?")
        dt = row.get("install_date") or "-"
        cols = st.columns([4, 2])
        if cols[0].button(nm, key=f"swbtn_{bk}", use_container_width=True):
            pf = _os2.environ.get("ProgramFiles", "C:\\\\Program Files")
            _open_folder(pf)
        cols[1].caption(dt)'''

c = c.replace(old_sw, new_sw)

with open(P, "w", encoding="utf-8") as f:
    f.write(c)

print("OK - software center finalized")
print("Run: streamlit run dashboard.py")
