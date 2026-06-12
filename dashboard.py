"""
GraceOS Dashboard V3 - 个人数字资产管理
Tab 1: 文件资产 | Tab 2: 软件资产中心 | Tab 3: 磁盘资产中心
"""
import streamlit as st
import sqlite3
import pandas as pd
import os
import subprocess

DB_FILE = r"E:\创业项目\GraceOS\09_Database\graceos.db"

# 过滤快捷方式/协议字符串
SHORTCUT_FILTER = " AND file_name NOT LIKE '%=%' AND file_name NOT LIKE 'ms-%' AND file_name NOT LIKE 'shell:%' AND file_name NOT LIKE 'file:///%'"

def _open_file(path):
    norm = os.path.normpath(path)
    if os.path.exists(norm): os.startfile(norm)
    else: st.toast("文件不存在")

def _open_folder(path):
    norm = os.path.normpath(path)
    if os.path.exists(norm): os.startfile(norm)
    else: st.toast("路径不存在")

def _format_install_date(val):
    s = str(val).strip()
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s

def _render_file_table(df, section_key, max_rows=50):
    """表格模式显示文件列表，点击行打开文件"""
    if df.empty:
        st.info("没有找到匹配的文件")
        return
    display = df.head(max_rows).copy()
    display = display[["file_name", "size_mb", "file_path"]]
    display.columns = ["文件名", "大小(MB)", "路径"]
    
    sel_key = f"filesel_{section_key}"
    event = st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        height=min(35 * len(display) + 38, 600),
        on_select="rerun",
        selection_mode="single-row",
        key=f"tbl_{section_key}",
    )
    if event.selection.rows:
        idx = event.selection.rows[0]
        last = st.session_state.get(sel_key, -1)
        if idx != last:
            st.session_state[sel_key] = idx
            fp = df.iloc[idx]["file_path"]
            _open_file(fp)

def _render_sw_table(df_sw, section_key):
    """表格模式显示软件列表，点击行打开安装目录"""
    if df_sw.empty:
        st.info("未找到匹配的软件")
        return
    display = df_sw.copy()
    display.columns = ["软件名称", "安装日期", "安装路径"]
    
    sel_key = f"swsel_{section_key}"
    event = st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        height=min(35 * len(display) + 38, 600),
        on_select="rerun",
        selection_mode="single-row",
        key=f"swtbl_{section_key}",
    )
    if event.selection.rows:
        idx = event.selection.rows[0]
        last = st.session_state.get(sel_key, -1)
        if idx != last:
            st.session_state[sel_key] = idx
            ip = df_sw.iloc[idx].get("install_path") or ""
            if ip and os.path.exists(ip):
                _open_folder(ip)
            else:
                st.toast("无安装路径或路径不存在")

# ===== 页面配置 =====
st.set_page_config(page_title="GraceOS V1", layout="wide")
st.title("GraceOS V1 - 个人数字资产管理")

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

tab1, tab2, tab3 = st.tabs(["📂 文件资产", "📋 软件资产中心", "📑 磁盘资产中心"])

# ============================================================
# TAB 1: 文件资产
# ============================================================
with tab1:
    cursor.execute("SELECT COUNT(*) FROM files")
    file_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM (SELECT file_name, file_size FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1)")
    dup_groups = cursor.fetchone()[0]
    cursor.execute("SELECT COALESCE(SUM(cnt), 0) FROM (SELECT COUNT(*) AS cnt FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1)")
    dup_files = cursor.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.expander(f"文件总数: {file_count:,}"):
            df_detail = pd.read_sql_query("SELECT file_name, file_path, ROUND(file_size/1024.0/1024.0,2) AS size_mb, last_modified FROM files ORDER BY file_size DESC LIMIT 200", conn)
            st.dataframe(df_detail, use_container_width=True, hide_index=True, height=400)
    with col2:
        with st.expander(f"重复组数: {dup_groups:,}"):
            df_dd = pd.read_sql_query("SELECT file_name, ROUND(file_size/1024.0/1024.0,2) AS size_mb, COUNT(*) AS dc, MIN(file_path) AS sample_path FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1 ORDER BY dc DESC LIMIT 100", conn)
            st.dataframe(df_dd, use_container_width=True, hide_index=True, height=400)
    with col3:
        with st.expander(f"重复文件: {dup_files:,}"):
            df_od = pd.read_sql_query("SELECT file_name, file_path, ROUND(file_size/1024.0/1024.0,2) AS size_mb, last_modified FROM files ORDER BY last_modified ASC LIMIT 200", conn)
            st.dataframe(df_od, use_container_width=True, hide_index=True, height=400)
    col4.metric("数据库", "SQLite")

    st.divider()
    st.header("🔍 文件搜索")
    file_keyword = st.text_input("输入文件名称关键字", placeholder="如: .pdf, 报告, photo...", key="file_search")
    if file_keyword:
        sql = f"SELECT file_name, file_path, ROUND(file_size/1024.0/1024.0,2) AS size_mb FROM files WHERE file_name LIKE ? {SHORTCUT_FILTER} ORDER BY file_size DESC LIMIT 100"
        df_s = pd.read_sql_query(sql, conn, params=[f"%{file_keyword}%"])
        st.caption(f"找到 {len(df_s)} 条结果")
        _render_file_table(df_s, "search")

    st.divider()
    st.header("📦 Top 100 大文件")
    sql_big = f"SELECT file_name, file_path, ROUND(file_size/1024.0/1024.0,2) AS size_mb FROM files WHERE 1=1 {SHORTCUT_FILTER} ORDER BY file_size DESC LIMIT 100"
    df_big = pd.read_sql_query(sql_big, conn)
    _render_file_table(df_big, "big")

    st.divider()
    st.header("🔧 重复文件统计")
    df_dup = pd.read_sql_query("SELECT file_name, ROUND(file_size/1024.0/1024.0,2) AS size_mb, COUNT(*) AS duplicate_count, MIN(file_path) AS file_path FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1 ORDER BY duplicate_count DESC LIMIT 50", conn)
    display_dup = df_dup.head(50).copy()
    display_dup = display_dup[["file_name", "size_mb", "duplicate_count", "file_path"]]
    display_dup.columns = ["文件名", "大小(MB)", "重复次数", "示例路径"]
    st.dataframe(display_dup, use_container_width=True, hide_index=True, height=400)

    st.divider()
    st.header("🕐 长期未使用文件")
    sql_old = f"SELECT file_name, file_path, last_modified, ROUND(file_size/1024.0/1024.0,2) AS size_mb FROM files WHERE 1=1 {SHORTCUT_FILTER} ORDER BY last_modified ASC LIMIT 50"
    df_old = pd.read_sql_query(sql_old, conn)
    display_old = df_old.head(50).copy()
    display_old = display_old[["file_name", "size_mb", "file_path"]]
    display_old.columns = ["文件名", "大小(MB)", "路径"]
    if not display_old.empty:
        sel_key_old = "filesel_old"
        event_old = st.dataframe(
            display_old, use_container_width=True, hide_index=True,
            height=min(35 * len(display_old) + 38, 600),
            on_select="rerun", selection_mode="single-row", key="tbl_old"
        )
        if event_old.selection.rows:
            idx = event_old.selection.rows[0]
            last = st.session_state.get(sel_key_old, -1)
            if idx != last:
                st.session_state[sel_key_old] = idx
                _open_file(df_old.iloc[idx]["file_path"])

# ============================================================
# TAB 2: 软件资产中心
# ============================================================
with tab2:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='software'")
    if cursor.fetchone() is None:
        st.warning("软件数据表尚未创建。请先运行: `python software_to_sqlite.py`")
    else:
        cursor.execute("SELECT COUNT(*) FROM software")
        sw_count = cursor.fetchone()[0]
        st.metric("软件总数", f"{sw_count}")
        st.divider()
        st.header("🔍 软件搜索")
        c1, c2 = st.columns([3, 1])
        with c1:
            sw_keyword = st.text_input("搜索软件名称", placeholder="例: Python, Docker, VS Code...", key="sw_search")
        with c2:
            sort_by = st.selectbox("排序方式", ["名称 A-Z", "名称 Z-A", "安装日期 新→旧", "安装日期 旧→新"], key="sw_sort")
        where_clause = "WHERE name LIKE ?" if sw_keyword else ""
        params = [f"%{sw_keyword}%"] if sw_keyword else []
        sort_map = {"名称 A-Z": "name ASC", "名称 Z-A": "name DESC", "安装日期 新→旧": "install_date DESC", "安装日期 旧→新": "install_date ASC"}
        order_clause = sort_map.get(sort_by, "name ASC")
        sql = f"SELECT name, install_date, install_path FROM software {where_clause} ORDER BY {order_clause} LIMIT 200"
        df_sw = pd.read_sql_query(sql, conn, params=params)
        
        # 格式化日期
        if not df_sw.empty:
            df_sw["install_date"] = df_sw["install_date"].apply(lambda x: _format_install_date(x) if pd.notna(x) else "-")
        
        st.caption(f"找到 {len(df_sw)} 条软件记录")
        _render_sw_table(df_sw, "swsearch")

# ============================================================
# TAB 3: 磁盘资产中心
# ============================================================
with tab3:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='disks'")
    if cursor.fetchone() is None:
        st.warning("磁盘数据表尚未创建。请先运行: `python disk_to_sqlite.py`")
    else:
        cursor.execute("SELECT COUNT(*) FROM disks")
        if cursor.fetchone()[0] == 0:
            st.info("磁盘数据为空。请先运行: `python scanners/disk_scanner.py` 然后 `python disk_to_sqlite.py`")
        else:
            df_disks = pd.read_sql_query("SELECT name, total_gb, used_gb, free_gb, usage_pct, root, description FROM disks ORDER BY name", conn)
            st.header("📑 磁盘概览")

            # C盘预警
            c_row = df_disks[df_disks["name"].str.upper() == "C"]
            if not c_row.empty and c_row.iloc[0]["usage_pct"] > 80:
                st.warning(f"⚠️ C盘空间不足！已用 {c_row.iloc[0]['usage_pct']:.1f}%，剩余 {c_row.iloc[0]['free_gb']:.1f} GB")

            for _, row in df_disks.iterrows():
                name = row["name"]
                total = row["total_gb"]
                used = row["used_gb"]
                free = row["free_gb"]
                pct = row["usage_pct"]
                root = row.get("root") or ""
                desc = row.get("description") or ""

                if pct < 70: color = "#28a745"
                elif pct < 90: color = "#ffc107"
                else: color = "#dc3545"

                col_a, col_b = st.columns([3, 1])
                with col_a:
                    if root and os.path.exists(root):
                        if st.button(f"📁 {name} 盘 ({desc})" if desc else f"📁 {name} 盘", key=f"disk_{name}", use_container_width=True):
                            os.startfile(root)
                    else:
                        st.markdown(f"**{name} 盘** {desc}")
                    st.markdown(
                        f"""<div style='background:#e9ecef;border-radius:4px;height:20px;width:100%'>
                        <div style='background:{color};border-radius:4px;height:20px;width:{min(pct,100):.1f}%;text-align:center;color:#fff;font-size:12px;line-height:20px'>
                        {pct:.1f}%</div></div>""",
                        unsafe_allow_html=True
                    )
                with col_b:
                    st.metric(f"{name}:", f"{used:.1f} GB / {total:.1f} GB", f"剩余 {free:.1f} GB")
                st.caption(f"已用 {used:.1f} GB · 剩余 {free:.1f} GB · 共 {total:.1f} GB")
                st.divider()

conn.close()
