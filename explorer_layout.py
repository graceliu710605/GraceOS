import re

P = r"e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1\dashboard.py"
with open(P, "r", encoding="utf-8") as f:
    c = f.read()

# New _render_rows: single line, clickable name opens file
new_rows = '''def _render_rows(df, section_key, max_rows=50):
    if df.empty:
        st.info("\u6ca1\u6709\u627e\u5230\u5339\u914d\u7684\u6587\u4ef6")
        return
    for idx, row in df.head(max_rows).iterrows():
        bk = f"{section_key}_{idx}"
        fn = row["file_name"]
        fp = row["file_path"]
        sz = f'{row["size_mb"]} MB' if "size_mb" in row and pd.notna(row["size_mb"]) else ""
        cols = st.columns([3, 1, 4])
        if cols[0].button(fn, key=f"fn_{bk}", use_container_width=True):
            _open_file(fp)
        cols[1].caption(sz)
        cols[2].caption(fp)
'''

# New _render_software_rows: single line, clickable name opens install dir
new_sw = '''def _render_software_rows(df_sw, prefix):
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
        cols[2].caption(src)
'''

# Replace _render_rows: from "def _render_rows" to "def _render_software_rows"
old_rows_re = r'def _render_rows\(df, section_key, max_rows=\d+\):.*?(?=def _render_software_rows)'
c = re.sub(old_rows_re, new_rows, c, flags=re.DOTALL)

# Replace _render_software_rows: from its def to next section
old_sw_re = r'def _render_software_rows\(df_sw, prefix\):.*?(?=# -- \u9875\u9762\u914d\u7f6e)'
c = re.sub(old_sw_re, new_sw, c, flags=re.DOTALL)

with open(P, "w", encoding="utf-8") as f:
    f.write(c)

print("OK - explorer layout applied")
print("Run: streamlit run dashboard.py")
