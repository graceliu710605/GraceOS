import re

P = r"e:\知识库obsidian\02_Projects\graceos\05_Code\GraceOS_V1\dashboard.py"
with open(P, "r", encoding="utf-8") as f:
    c = f.read()

# Step 1: Replace 4 expanders with single metric + caption
old_expanders = r'        col1, col2, col3, col4 = st\.columns\(4\)\n        with col1:.*?st\.dataframe\(df_sw_size, use_container_width=True, hide_index=True, height=400\)'

new_metric = '        st.metric("\\u8f6f\\u4ef6\\u603b\\u6570", f"{sw_count}")\n        st.caption(f"\\u6709\\u53d1\\u5e03\\u5546: {sw_with_publisher} | \\u6709\\u5b89\\u88c5\\u65e5\\u671f: {sw_with_date} | \\u6709\\u5927\\u5c0f: {sw_with_size}")'

c = re.sub(old_expanders, new_metric, c, flags=re.DOTALL)

# Step 2: Remove publisher distribution section
old_pub = r'\n        # -- .*?\n        st\.divider\(\)\n        st\.header\(".*?\\u53d1\\u5e03\\u5546.*?"\).*?(?=\n\n# TAB 3)'
c = re.sub(old_pub, '', c, flags=re.DOTALL)

with open(P, "w", encoding="utf-8") as f:
    f.write(c)

print("OK - software section simplified")
print("Run: streamlit run dashboard.py")
