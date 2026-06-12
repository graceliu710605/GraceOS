import re

P = r"e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1\dashboard.py"
with open(P, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Update _render_software_rows: plain text + date format + click icon
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
        dt = _format_date(row.get("install_date"))
        cols = st.columns([4, 1])
        cols[0].markdown(f"{nm}")
        cols[1].markdown(dt)
        if st.button("\\u6253\\u5f00\\u76ee\\u5f55", key=f"swdir_{bk}"):
            pf = _os2.environ.get("ProgramFiles", "C:\\\\Program Files")
            _open_folder(pf)
        st.markdown("---")'''

c = c.replace(old_sw, new_sw)

# 2. Add _format_date helper
old_fmt = '''def _format_install_date(val):'''
new_fmt = '''def _format_date(val):
    if val is None or val == "":
        return "-"
    v = str(val).strip().replace("-", "").replace("/", "")
    if len(v) == 8:
        return f"{v[:4]}-{v[4:6]}-{v[6:8]}"
    return str(val)[:10]

def _format_install_date(val):'''

c = c.replace(old_fmt, new_fmt)

# 3. Change search results caption
c = c.replace('st.caption("找到 {len(df_sw)} 条软件记录")',
              'st.caption(f"\\u5171 {len(df_sw)} \\u4e2a\\u8f6f\\u4ef6")')

# 4. Remove publisher section
old_pub = '''        # -- \\u53d1\\u5e03\\u5546\\u5206\\u5e03
        st.divider()
        st.header("\\ud83d\\udcca \\u53d1\\u5e03\\u5546 Top 20")'''

c = c.replace(old_pub, "        ")

# Remove the rest of publisher section
c = re.sub(
    r'\n        df_pub = pd\.read_sql_query.*?(?=\n\n# TAB 3)',
    '',
    c,
    flags=re.DOTALL
)

with open(P, "w", encoding="utf-8") as f:
    f.write(c)

print("OK - final polish applied")
print("Run: streamlit run dashboard.py")
