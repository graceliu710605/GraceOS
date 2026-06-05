import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

# 文件路径
BASE_DIR = os.path.join(os.getcwd())
SOFTWARE_FILE = os.path.join(BASE_DIR, "09_Database", "software_assets", "software_inventory.json")
DISK_FILE = os.path.join(BASE_DIR, "09_Database", "disk_assets", "disk_inventory.json")
FILE_FILE = os.path.join(BASE_DIR, "09_Database", "file_assets", "file_inventory.json")

st.set_page_config(page_title="GraceOS Dashboard", layout="wide")

st.title("📊 GraceOS Dashboard V2")
st.subheader("Personal Digital Asset Management")

# -----------------------------
# 加载数据
# -----------------------------
def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

software_data = load_json(SOFTWARE_FILE)
disk_data = load_json(DISK_FILE)
file_data = load_json(FILE_FILE)

# -----------------------------
# 状态卡片
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🖥 软件资产数量", len(software_data))

with col2:
    st.metric("💽 磁盘数量", len(disk_data))

with col3:
    # 健康度计算：简单示例
    health = 100
    for disk in disk_data:
        free = disk.get("Free") or disk.get("free_size") or 0
        total = disk.get("Used",0) + free
        if total > 0:
            health = int(min(health, free / total * 100))
    st.metric("🟢 系统健康度", f"{health}%")

st.markdown("---")

# -----------------------------
# 文件搜索
# -----------------------------
st.subheader("🔍 文件搜索")
search_query = st.text_input("输入文件名或关键字")

if search_query:
    results = [f"{f['file_name']} ({f['file_size']/1024:.1f} KB) - {f['file_path']}" 
               for f in file_data if search_query.lower() in f["file_name"].lower()]
    if results:
        for r in results:
            st.write(r)
    else:
        st.info("未找到匹配文件")

st.markdown("---")

# -----------------------------
# 重复文件
# -----------------------------
st.subheader("⚠ 重复文件")
name_count = defaultdict(list)
for f in file_data:
    name_count[f["file_name"]].append(f["file_path"])

duplicates = {k:v for k,v in name_count.items() if len(v) > 1}
if duplicates:
    for k, paths in duplicates.items():
        st.write(f"📄 {k}")
        for p in paths:
            st.text(f"   {p}")
else:
    st.write("无重复文件")

st.markdown("---")

# -----------------------------
# 长期未使用文件
# -----------------------------
st.subheader("⏳ 长期未使用文件 (30 天未修改)")
threshold = datetime.now() - timedelta(days=30)
old_files = []
for f in file_data:
    try:
        lm = datetime.fromisoformat(f.get("last_modified"))
        if lm < threshold:
            old_files.append(f)
    except:
        pass

if old_files:
    for f in old_files:
        st.write(f"{f['file_name']} - {f['file_path']} (最后修改: {f['last_modified']})")
else:
    st.write("无长期未使用文件")

st.markdown("---")

# -----------------------------
# 软件资产展示
# -----------------------------
st.subheader("💻 软件资产列表")
for s in software_data:
    name = s.get("raw") or s.get("name")
    st.text(f"{name}")

# -----------------------------
# 磁盘资产展示
# -----------------------------
st.subheader("💽 磁盘状态")
for d in disk_data:
    name = d.get("Name") or d.get("drive")
    free = d.get("Free") or d.get("free_size",0)
    used = d.get("Used") or d.get("used_size",0)
    total = used + free
    st.text(f"{name}: 已用 {used/1e9:.2f} GB / 总 {total/1e9:.2f} GB | 可用 {free/1e9:.2f} GB")