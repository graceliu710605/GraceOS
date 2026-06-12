import re

P = r"e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1\dashboard.py"
with open(P, "r", encoding="utf-8") as f:
    c = f.read()

# Fix expander labels (exact f-string match)
c = c.replace('f"[files] {file_count:,}"', 'f"\u6587\u4ef6\u603b\u6570: {file_count:,}"')
c = c.replace('f"[dup] groups: {dup_groups:,}"', 'f"\u91cd\u590d\u7ec4\u6570: {dup_groups:,}"')
c = c.replace('f"[dup] files: {dup_files:,}"', 'f"\u91cd\u590d\u6587\u4ef6: {dup_files:,}"')
c = c.replace('f"[sw] installed: {sw_count}"', 'f"\u5df2\u5b89\u88c5\u8f6f\u4ef6: {sw_count}"')
c = c.replace('f"[sw] publisher: {sw_with_publisher}"', 'f"\u6709\u53d1\u5e03\u5546: {sw_with_publisher}"')
c = c.replace('f"[sw] date: {sw_with_date}"', 'f"\u6709\u5b89\u88c5\u65e5\u671f: {sw_with_date}"')
c = c.replace('f"[sw] size: {sw_with_size}"', 'f"\u6709\u5927\u5c0f: {sw_with_size}"')
c = c.replace('"database", "SQLite"', '"\u6570\u636e\u5e93", "SQLite"')
c = c.replace('[search] results:', '\u641c\u7d22\u7ed3\u679c:')

# Add install path to _render_software_rows
c = c.replace(
    'c1.caption(f"{pb} | v{vr}")\n\n        if c2.button(',
    'c1.caption(f"{pb} | v{vr}")\n        if src:\n            c1.code(src, language=None)\n\n        if c2.button('
)

# Fix _open_file
c = c.replace(
    'def _open_file(path):\n    os.startfile(path)',
    'def _open_file(path):\n    import subprocess as _sp2\n    _sp2.run(["explorer", path], shell=True)'
)

with open(P, "w", encoding="utf-8") as f:
    f.write(c)

print("OK - labels fixed")
print("Run: streamlit run dashboard.py")
