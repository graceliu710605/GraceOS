import streamlit as st
import json
from pathlib import Path
from datetime import datetime, timedelta

# 数据文件路径
SOFTWARE_FILE = Path("../09_Database/software_assets/software_inventory.json")
FILE_FILE = Path("../09_Database/file_assets/file_inventory.json")
DISK_FILE = Path("../09_Database/disk_assets/disk_inventory.json")

# Streamlit 页面配置
st.set_page_config(
    page_title="GraceOS v3 Dashboard",
    layout="wide"
)

st.title("📊 GraceOS Dashboard V3")
st.subheader("Personal Digital Asset Management")

# ------------------ 软件资产 ------------------
software_count = 0
try:
    with open(SOFTWARE_FILE, "r", encoding="utf-8") as f:
        software_data = json.load(f)
        software_count = len(software_data)
except Exception:
    software_data = []

# ------------------ 磁盘资产 ------------------
disk_count = 0
try:
    with open(DISK_FILE, "r", encoding="utf-8") as f:
        disk_data = json.load(f)
        disk_count = len(disk_data)
except Exception:
    disk_data = []

# ------------------ 系统健康度计算 ------------------
health_score = 100  # 简单示例，可根据文件/磁盘状态计算

# ------------------ 概览展示 ------------------
col1, col2, col3 = st.columns(3)
col1.metric("🖥 软件资产数量", software_count)
col2.metric("💽 磁盘数量", disk_count)
col3.metric("🟢 系统健康度", f"{health_score}%")

st.markdown("---")

# ------------------ 文件搜索 ------------------
st.header("🔍 文件搜索")
search_keyword = st.text_input("输入文件名或关键字")

file_results = []
try:
    with open(FILE_FILE, "r", encoding="utf-8") as f:
        file_data = json.load(f)
    if search_keyword:
        for item in file_data:
            if search_keyword.lower() in item["file_name"].lower():
                file_results.append(item)
except Exception:
    file_data = []

if search_keyword:
    if file_results:
        st.success(f"找到 {len(file_results)} 个匹配文件")
        for item in file_results[:20]:  # 前 20 个显示
            st.write(f'{item["file_name"]} | {item["file_path"]} | {item["file_size"]/1024:.1f} KB')
    else:
        st.warning("未找到匹配文件")

# ------------------ 重复文件 ------------------
st.header("⚠ 重复文件")
duplicate_files = []
seen_paths = set()
for item in file_data:
    key = (item["file_name"], item["file_size"])
    if key in seen_paths:
        duplicate_files.append(item)
    else:
        seen_paths.add(key)

if duplicate_files:
    st.warning(f"找到 {len(duplicate_files)} 个重复文件")
    for f in duplicate_files:
        st.write(f'{f["file_name"]} | {f["file_path"]}')
else:
    st.info("无重复文件")

# ------------------ 长期未使用文件 ------------------
st.header("⏳ 长期未使用文件 (30 天未修改)")
old_files = []
threshold_date = datetime.now() - timedelta(days=30)
for item in file_data:
    try:
        lm = datetime.fromisoformat(item["last_modified"])
        if lm < threshold_date:
            old_files.append(item)
    except:
        continue

if old_files:
    st.warning(f"找到 {len(old_files)} 个长期未使用文件")
    for f in old_files[:20]:
        st.write(f'{f["file_name"]} | {f["file_path"]} | 最后修改: {f["last_modified"]}')
else:
    st.info("无长期未使用文件")

# ------------------ 软件资产列表展示 ------------------
st.header("💻 软件资产列表")
if software_data:
    for s in software_data[:20]:  # 显示前 20 条
        st.write(f'{s.get("name","")} | {s.get("version","")} | {s.get("install_path","")} | {s.get("source","")}')
else:
    st.info("无软件资产数据")

# ------------------ 磁盘状态 ------------------
st.header("💽 磁盘状态")
if disk_data:
    for d in disk_data:
        used = d.get("Used",0)
        free = d.get("Free",0)
        total = used + free
        st.write(f'{d.get("Name","")} | 已用: {used/1024/1024:.2f} MB | 可用: {free/1024/1024:.2f} MB | 总量: {total/1024/1024:.2f} MB')
else:
    st.info("无磁盘数据")