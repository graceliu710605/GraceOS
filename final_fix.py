import re

P = r"e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1\dashboard.py"
with open(P, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find and replace software expanders (col1-col4 block)
new_lines = []
skip = False
skip_until_divider = False
for i, line in enumerate(lines):
    if "        col1, col2, col3, col4 = st.columns(4)" in line and "with col1:" in lines[i+1] if i+1 < len(lines) else False:
        # This is the SW expanders block - replace with simple metric
        new_lines.append('        st.metric("\\u8f6f\\u4ef6\\u603b\\u6570", f"{sw_count}")\n')
        new_lines.append('        st.caption(f"\\u6709\\u53d1\\u5e03\\u5546: {sw_with_publisher} | \\u6709\\u5b89\\u88c5\\u65e5\\u671f: {sw_with_date} | \\u6709\\u5927\\u5c0f: {sw_with_size}")\n')
        new_lines.append('\n')
        # Skip all lines until the next st.divider()
        skip_until_divider = True
        continue
    if skip_until_divider:
        if "        st.divider()" in line:
            new_lines.append(line)  # keep the divider
            skip_until_divider = False
        continue
    # Remove publisher section
    if "        # -- \\u53d1\\u5e03\\u5546\\u5206\\u5e03" in line:
        skip = True
        continue
    if skip:
        if "with tab3:" in line:
            skip = False
            new_lines.append(line)
        continue
    new_lines.append(line)

with open(P, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("OK - expanders removed, publisher removed")
print("Run: streamlit run dashboard.py")
