"""
个人数字资产管家 (GraceOS V2.1)
Asset Management Platform
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import sqlite3
import pandas as pd
import subprocess, shutil
from datetime import date
from analyzers.health_scorer import calculate as calc_health

DB_FILE = r"E:\创业项目\GraceOS\09_Database\graceos.db"
ARCHIVE_DIR = r"E:\归档"
RECYCLE_DIR = r"E:\回收站"

SYS_PROTECT = ["C:/Windows","C:/Windows/System32","pagefile.sys","hiberfil.sys","swapfile.sys","C:/Program Files/WindowsApps","C:/ProgramData/Microsoft"]
def _is_protected(fp):
    fp_l = fp.lower().replace("\\","/")
    for p in SYS_PROTECT:
        if p.lower() in fp_l: return True
    return False

SHORTCUT_FILTER = " AND file_name NOT LIKE '%=%' AND file_name NOT LIKE 'ms-%' AND file_name NOT LIKE 'shell:%' AND file_name NOT LIKE 'file:///%'"

def _open_file(path):
    norm = os.path.normpath(path)
    if os.path.exists(norm): os.startfile(norm)
    else: st.toast("文件不存在")


def _format_size(size_bytes):
    """Adaptive file size display: Bytes/KB/MB/GB"""
    if size_bytes >= 1073741824:
        return f"{size_bytes/1073741824:.1f} GB"
    elif size_bytes >= 1048576:
        return f"{size_bytes/1048576:.1f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes/1024:.1f} KB"
    else:
        return f"{size_bytes} B"

def _format_date(val):
    if not val: return "-"
    s = str(val).strip()
    if len(s) == 8 and s.isdigit(): return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    if len(s) >= 10: return s[:10]
    return s


def _file_exists(fp):
    """Check file existence, return (exists, display_label)"""
    ok = os.path.exists(fp)
    return ok, "✅" if ok else "⚠️ 已不存在"

def _safe_delete(fp):
    if not os.path.exists(fp):
        return False, "文件已不存在"
    try:
        target = os.path.join(RECYCLE_DIR, os.path.basename(fp))
        os.makedirs(RECYCLE_DIR, exist_ok=True)
        if os.path.exists(target):
            target = os.path.join(RECYCLE_DIR, str(int(os.path.getmtime(fp))) + "_" + os.path.basename(fp))
        shutil.move(fp, target)
        return True, target
    except Exception as e:
        return False, str(e)

def _safe_delete_batch(files):
    ok, fail, skip = 0, 0, 0
    for fp in files:
        if not os.path.exists(fp):
            skip += 1
        else:
            success, _ = _safe_delete(fp)
            if success: ok += 1
            else: fail += 1
    return ok, fail, skip

def _launch_software(install_path, sw_name):
    if install_path and os.path.exists(install_path):
        try:
            exes = []
            for f in os.listdir(install_path):
                fp = os.path.join(install_path, f)
                if f.lower().endswith(".exe") and os.path.isfile(fp):
                    exes.append((f, fp))
            if exes:
                sw_lower = sw_name.lower()
                for fname, fpath in exes:
                    if sw_lower in fname.lower():
                        os.startfile(fpath)
                        return True, fpath
                os.startfile(exes[0][1])
                return True, exes[0][1]
        except: pass
        os.startfile(install_path)
        return True, install_path
    return False, None

st.set_page_config(page_title="个人数字资产管家", layout="wide")
st.title("个人数字资产管家")
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
# P0 perf: ensure indexes exist (idempotent, skipped on subsequent starts)
cur.execute("CREATE INDEX IF NOT EXISTS idx_files_name_size ON files(file_name, file_size)")
cur.execute("CREATE INDEX IF NOT EXISTS idx_files_last_modified ON files(last_modified)")
cur.execute("CREATE INDEX IF NOT EXISTS idx_files_size ON files(file_size)")
conn.commit()
tabs = st.tabs(["🏠 首页", "📂 文件", "📋 软件", "📑 磁盘", "📊 存储", "🌐 资产", "💾 备份", "📁 项目", "🧠 知识库", "📝 Prompt", "⚙️ 设置"])

import webbrowser as _webbrowser
# ===== TAB 0: HOME =====
with tabs[0]:
    st.header("数字健康评分")
    score = calc_health(conn)
    if score:
        col_a, col_b = st.columns([1, 2])
        with col_a:
            grade = "🟢 优秀" if score["total"] >= 80 else ("🟡 良好" if score["total"] >= 60 else "🔴 需改善")
            st.metric("综合评分", f"{score['total']}/100", grade)
        with col_b:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("文件健康度", f"{score['dup_score']}/100", f"{score['dup_files']:,}个重复")
            c2.metric("文件活跃度", f"{score['unused_score']}/100", f"{score['unused_mb']:.0f}MB")
            c3.metric("磁盘健康度", f"{score['disk_score']}/100", f"C盘 {score['c_pct']:.1f}%")
            c4.metric("软件健康度", f"{score['sw_score']}/100", f"{score['sw_multi']}多版本")
        st.divider()
        st.header("AI 建议中心")
        suggestions = []
        if score["dup_score"] < 80:
            suggestions.append(f"⚠️ 重复文件: {score['dup_files']:,}个, 占用 {score['dup_mb']:.0f}MB")
        if score["unused_score"] < 60:
            suggestions.append(f"📦 未使用文件: {score['unused_count']:,}个, 占用 {score['unused_mb']:.0f}MB")
        if score["disk_score"] < 60:
            suggestions.append(f"🔴 C盘不足: 已用 {score['c_pct']:.1f}%")
        if score["sw_score"] < 80:
            suggestions.append(f"🔄 多版本软件: {score['sw_multi']}个")
        if not suggestions:
            st.success("✅ 各项指标良好")
        for s in suggestions:
            st.write(s)
    st.divider()
    if st.button("🔄 刷新评分"):
        st.rerun()

# ===== TAB 1: FILES =====
with tabs[1]:
    cur.execute("SELECT COUNT(*) FROM files"); fc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM (SELECT file_name, file_size FROM files GROUP BY file_name, file_size HAVING COUNT(*)>1)"); dg = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(cnt),0) FROM (SELECT COUNT(*) AS cnt FROM files GROUP BY file_name, file_size HAVING COUNT(*)>1)"); dfc = cur.fetchone()[0]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("文件总数", f"{fc:,}")
    c2.metric("重复组数", f"{dg:,}")
    c3.metric("重复文件", f"{dfc:,}")
    c4.metric("数据库", "SQLite")
    st.divider()
    st.header("🔍 文件搜索")
    kw = st.text_input("搜索文件名关键字", placeholder="如: .pdf, 报告...", key="fs_kw")
    if kw:
        df = pd.read_sql_query(f"SELECT file_name,file_path,last_modified,file_size FROM files WHERE file_name LIKE ? {SHORTCUT_FILTER} ORDER BY file_size DESC LIMIT 50", conn, params=[f"%{kw}%"])
        st.caption(f"找到 {len(df)} 条")
        if not df.empty:
            h1,h2,h3,h4 = st.columns([0.8, 3, 1.2, 1])
            h1.markdown("**删除**"); h2.markdown("**文件名**"); h3.markdown("**日期**"); h4.markdown("**大小(MB)**")
            st.divider()
            for i, row in df.iterrows():
                c1,c2,c3,c4 = st.columns([0.8, 3, 1.2, 1])
                if c1.button("🗑️", key=f"fsdel_{i}"):
                    ok, msg = _safe_delete(row["file_path"])
                    if ok: st.success("已删除"); st.rerun()
                    else: st.error(msg)
                if c2.button(str(row["file_name"]), key=f"fsopen_{i}"):
                    _open_file(row["file_path"])
                c3.write(_format_date(row["last_modified"]))
                c4.write(_format_size(row["file_size"]))
    st.divider()
    st.header("🔧 重复文件")
    df_dup = pd.read_sql_query("""SELECT file_name, file_size, COUNT(*) AS dc, MIN(file_path) AS keep_path, MAX(file_path) AS del_path FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1 ORDER BY dc DESC""", conn)
    if not df_dup.empty:
        total_mb = (df_dup["file_size"] * (df_dup["dc"] - 1)).sum()
        st.caption(f"前50组，保留一份可释放约 {_format_size(int(total_mb*1048576))}")
        total_groups = len(df_dup)
        total_saved_bytes = int((df_dup["file_size"] * (df_dup["dc"] - 1)).sum())
        page_size = 50
        if "dup_page" not in st.session_state:
            st.session_state.dup_page = 0
        total_pages = max(1, (total_groups + page_size - 1) // page_size)
        start = st.session_state.dup_page * page_size
        df_dup_page = df_dup.iloc[start:start+page_size]
        pc1, pc2, pc3 = st.columns([1, 2, 1])
        if pc1.button("◀ 上一页", disabled=st.session_state.dup_page <= 0, key="dup_prev"):
            st.session_state.dup_page -= 1; st.rerun()
        pc2.write(f"第 {st.session_state.dup_page+1}/{total_pages} 页  (共 {total_groups} 组)")
        if pc3.button("下一页 ▶", disabled=st.session_state.dup_page >= total_pages-1, key="dup_next"):
            st.session_state.dup_page += 1; st.rerun()
        page_saved = int((df_dup_page["file_size"] * (df_dup_page["dc"] - 1)).sum())
        st.caption(f"本页保留一份可释放 {_format_size(page_saved)}   |   总计可释放 {_format_size(total_saved_bytes)}")
        sel_key = "dup_checked"
        for i in range(len(df_dup_page)):
            if f"{sel_key}_{i}" not in st.session_state:
                st.session_state[f"{sel_key}_{i}"] = False
        checked = [st.session_state[f"{sel_key}_{i}"] for i in range(len(df_dup_page))]
        if any(checked):
            to_del = [df_dup_page.iloc[i]["del_path"] for i, c in enumerate(checked) if c]
            del_bytes = sum(df_dup_page.iloc[i]["file_size"] for i, c in enumerate(checked) if c)
            if st.button(f"🗑️ 批量删除选中 ({len(to_del)}组, ~{_format_size(del_bytes)})", key="dup_batch"):
                ok, fail, skip = _safe_delete_batch(to_del)
                if fail == 0 and skip == 0: st.success(f"已删除 {ok} 个")
                else: st.warning(f"{ok} 成功, {fail} 失败, {skip} 跳过(不存在)")
                for i in range(len(df_dup_page)):
                    st.session_state[f"{sel_key}_{i}"] = False
                st.rerun()
        h1,h2,h3,h4,h5,h6 = st.columns([0.3, 1, 0.7, 3, 1.2, 1])
        h1.markdown("**选**"); h2.markdown("**建议**"); h3.markdown("**删除**"); h4.markdown("**文件名**"); h5.markdown("**日期**"); h6.markdown("**大小(MB)**")
        st.divider()
        for j, (_, row) in enumerate(df_dup_page.iterrows()):
            c1,c2,c3,c4,c5,c6 = st.columns([0.3, 1, 0.7, 3, 1.2, 1])
            key = f"{sel_key}_{j}"
            st.session_state[key] = c1.checkbox("☐", key=f"dup_cb_{st.session_state.dup_page}_{j}", value=st.session_state[key], label_visibility="collapsed")
            c2.write("建议保留")
            if c3.button("🗑️", key=f"dup_del_{st.session_state.dup_page}_{j}"):
                ok, msg = _safe_delete(row["del_path"])
                if ok: st.success("已删除"); st.rerun()
                else: st.error(msg)
            if c4.button(str(row["file_name"]), key=f"dup_open_{st.session_state.dup_page}_{j}"):
                _open_file(row["keep_path"])
            c5.write(_format_date(""))
            c6.write(_format_size(row["file_size"]))
    else:
        st.info("无重复文件")
    st.divider()
    st.header("📦 Top 100 大文件")
    df_big = pd.read_sql_query(f"SELECT file_name,file_path,last_modified,file_size FROM files WHERE 1=1 {SHORTCUT_FILTER} ORDER BY file_size DESC LIMIT 100", conn)
    if not df_big.empty:
        sel_big = "big_checked"
        for i in range(len(df_big)):
            if f"{sel_big}_{i}" not in st.session_state:
                st.session_state[f"{sel_big}_{i}"] = False
        checked_big = [st.session_state[f"{sel_big}_{i}"] for i in range(len(df_big))]
        if any(checked_big):
            to_del = [df_big.iloc[i]["file_path"] for i, c in enumerate(checked_big) if c]
            del_mb = sum(df_big.iloc[i]["size_mb"] for i, c in enumerate(checked_big) if c)
            if st.button(f"🗑️ 批量删除选中 ({len(to_del)}个, ~{del_mb:.0f}MB)", key="big_batch"):
                ok, fail, skip = _safe_delete_batch(to_del)
                if fail == 0 and skip == 0: st.success(f"已删除 {ok} 个")
                else: st.warning(f"{ok} 成功, {fail} 失败, {skip} 跳过(不存在)")
                for i in range(len(df_big)):
                    st.session_state[f"{sel_big}_{i}"] = False
                st.rerun()
        h1,h2,h3,h4,h5 = st.columns([0.3, 0.7, 3, 1.2, 1])
        h1.markdown("**选**"); h2.markdown("**删除**"); h3.markdown("**文件名**"); h4.markdown("**日期**"); h5.markdown("**大小(MB)**")
        st.divider()
        for i, row in df_big.iterrows():
            c1,c2,c3,c4,c5 = st.columns([0.3, 0.7, 3, 1.2, 1])
            st.session_state[f"{sel_big}_{i}"] = c1.checkbox("☐", key=f"big_cb_{i}", value=st.session_state[f"{sel_big}_{i}"], label_visibility="collapsed")
            if c2.button("🗑️", key=f"big_del_{i}"):
                ok, msg = _safe_delete(row["file_path"])
                if ok: st.success("已删除"); st.rerun()
                else: st.error(msg)
            if c3.button(str(row["file_name"]), key=f"big_open_{i}"):
                _open_file(row["file_path"])
            c4.write(_format_date(row["last_modified"]))
            c5.write(_format_size(row["file_size"]))
    else:
        st.info("无大文件")
    st.divider()
    st.header("🕐 长期未使用文件")
    df_old = pd.read_sql_query(f"SELECT file_name,file_path,last_modified,file_size FROM files WHERE 1=1 AND NOT (file_path LIKE '%Windows%' OR file_path LIKE '%System32%' OR file_name IN ('pagefile.sys','hiberfil.sys','swapfile.sys')) {SHORTCUT_FILTER} ORDER BY last_modified ASC LIMIT 100", conn)
    if not df_old.empty:
        total_old_mb = df_old["file_size"].sum()
        st.caption(f"前100个最久未使用, 共 {total_old_mb:.0f} MB")
        sel_old = "old_checked"
        for i in range(len(df_old)):
            if f"{sel_old}_{i}" not in st.session_state:
                st.session_state[f"{sel_old}_{i}"] = False
        checked_old = [st.session_state[f"{sel_old}_{i}"] for i in range(len(df_old))]
        if any(checked_old):
            to_del = [df_old.iloc[i]["file_path"] for i, c in enumerate(checked_old) if c]
            del_mb = sum(df_old.iloc[i]["size_mb"] for i, c in enumerate(checked_old) if c)
            if st.button(f"🗑️ 批量删除选中 ({len(to_del)}个, ~{del_mb:.0f}MB)", key="old_batch"):
                ok, fail, skip = _safe_delete_batch(to_del)
                if fail == 0 and skip == 0: st.success(f"已删除 {ok} 个")
                else: st.warning(f"{ok} 成功, {fail} 失败, {skip} 跳过(不存在)")
                for i in range(len(df_old)):
                    st.session_state[f"{sel_old}_{i}"] = False
                st.rerun()
        h1,h2,h3,h4,h5 = st.columns([0.3, 0.7, 3, 1.2, 1])
        h1.markdown("**选**"); h2.markdown("**删除**"); h3.markdown("**文件名**"); h4.markdown("**日期**"); h5.markdown("**大小(MB)**")
        st.divider()
        for i, row in df_old.iterrows():
            c1,c2,c3,c4,c5 = st.columns([0.3, 0.7, 3, 1.2, 1])
            st.session_state[f"{sel_old}_{i}"] = c1.checkbox("☐", key=f"old_cb_{i}", value=st.session_state[f"{sel_old}_{i}"], label_visibility="collapsed")
            if c2.button("🗑️", key=f"old_del_{i}"):
                ok, msg = _safe_delete(row["file_path"])
                if ok: st.success("已删除"); st.rerun()
                else: st.error(msg)
            if c3.button(str(row["file_name"]), key=f"old_open_{i}"):
                _open_file(row["file_path"])
            c4.write(_format_date(row["last_modified"]))
            c5.write(_format_size(row["file_size"]))
    else:
        st.info("无长期未使用文件")

# ===== TAB 2: SOFTWARE =====
with tabs[2]:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='software'")
    if cur.fetchone() is None:
        st.warning("软件数据表未创建。运行: python software_to_sqlite.py")
    else:
        cur.execute("SELECT COUNT(*) FROM software"); sw_count = cur.fetchone()[0]
        st.metric("软件总数", f"{sw_count}")
        st.divider()
        st.header("🔍 软件搜索")
        c1, c2 = st.columns([3, 1])
        with c1: sw_kw = st.text_input("搜索软件名称", placeholder="例: Python, Docker...", key="sw_kw")
        with c2: sort_by = st.selectbox("排序", ["名称 A-Z", "名称 Z-A", "安装日期 新→旧", "安装日期 旧→新"], key="sw_sort")
        wc = "WHERE name LIKE ?" if sw_kw else ""
        params_sw = [f"%{sw_kw}%"] if sw_kw else []
        sm = {"名称 A-Z": "name ASC", "名称 Z-A": "name DESC", "安装日期 新→旧": "install_date DESC", "安装日期 旧→新": "install_date ASC"}
        oc = sm.get(sort_by, "name ASC")
        df_sw = pd.read_sql_query(f"SELECT name, install_date, install_path, version FROM software {wc} ORDER BY {oc} LIMIT 100", conn, params=params_sw)
        if not df_sw.empty:
            df_sw["install_date"] = df_sw["install_date"].apply(lambda x: _format_date(x) if pd.notna(x) else "-")
        st.caption(f"找到 {len(df_sw)} 条")
        if not df_sw.empty:
            h1,h2,h3,h4,h5 = st.columns([0.7, 1, 2.5, 1, 2])
            h1.markdown("**卸载**"); h2.markdown("**建议**"); h3.markdown("**软件名称**"); h4.markdown("**版本**"); h5.markdown("**安装路径**")
            st.divider()
            for i, row in df_sw.iterrows():
                c1,c2,c3,c4,c5 = st.columns([0.7, 1, 2.5, 1, 2])
                if c1.button("🗑️", key=f"sw_del_{i}"):
                    try:
                        subprocess.run(["winget", "uninstall", "--name", str(row["name"])], capture_output=True, timeout=30)
                        st.toast(f"已发起卸载: {row['name']}")
                    except Exception as e:
                        st.warning(f"卸载失败: {e}")
                c2.write("-")
                if c3.button(str(row["name"]), key=f"sw_open_{i}"):
                    ip = row.get("install_path") or ""
                    launched, result = _launch_software(ip, str(row["name"]))
                    if launched: st.toast(f"启动: {row['name']}")
                    else: st.toast("无法启动: 无安装路径")
                c4.write(str(row.get("version", "-")))
                c5.write(str(row.get("install_path", "-") or "-"))
        else:
            st.info("无匹配软件")
        st.divider()
        st.header("🔬 多版本软件")
        dup_sw = pd.read_sql_query("SELECT name AS 软件名称, COUNT(*) AS 版本数, GROUP_CONCAT(version,', ') AS 所有版本, MAX(version) AS 最新版本, MIN(version) AS 最旧版本 FROM software GROUP BY name HAVING COUNT(*) > 1 ORDER BY 版本数 DESC", conn)
        if not dup_sw.empty:
            st.caption("同一软件多个版本，建议保留最新")
            sel_mv = "mv_checked"
            for i in range(len(dup_sw)):
                if f"{sel_mv}_{i}" not in st.session_state:
                    st.session_state[f"{sel_mv}_{i}"] = False
            checked_mv = [st.session_state[f"{sel_mv}_{i}"] for i in range(len(dup_sw))]
            if any(checked_mv):
                to_uninstall = [str(dup_sw.iloc[i]["软件名称"]) for i, c in enumerate(checked_mv) if c]
                if st.button(f"🗑️ 批量卸载选中 ({len(to_uninstall)}个)", key="mv_batch"):
                    for name in to_uninstall:
                        try:
                            subprocess.run(["winget", "uninstall", "--name", name], capture_output=True, timeout=30)
                        except: pass
                    st.toast("已发起批量卸载")
                    for i in range(len(dup_sw)):
                        st.session_state[f"{sel_mv}_{i}"] = False
                    st.rerun()
            h1,h2,h3,h4,h5,h6 = st.columns([0.3, 0.7, 1, 2, 1, 1])
            h1.markdown("**选**"); h2.markdown("**卸载**"); h3.markdown("**建议**"); h4.markdown("**软件名称**"); h5.markdown("**最新版**"); h6.markdown("**最旧版**")
            st.divider()
            for i, row in dup_sw.iterrows():
                c1,c2,c3,c4,c5,c6 = st.columns([0.3, 0.7, 1, 2, 1, 1])
                st.session_state[f"{sel_mv}_{i}"] = c1.checkbox("☐", key=f"mv_cb_{i}", value=st.session_state[f"{sel_mv}_{i}"], label_visibility="collapsed")
                if c2.button("🗑️", key=f"mv_del_{i}"):
                    try:
                        subprocess.run(["winget", "uninstall", "--name", str(row["软件名称"]), "--version", str(row["最旧版本"])], capture_output=True, timeout=30)
                        st.toast(f"已发起卸载: {row['软件名称']}")
                    except Exception as e:
                        st.warning(f"卸载失败: {e}")
                c3.write("建议保留最新")
                if c4.button(str(row["软件名称"]), key=f"mv_open_{i}"):
                    st.info(f"版本: {row['所有版本']}")
                c5.write(str(row["最新版本"]))
                c6.write(str(row["最旧版本"]))
        else:
            st.success("✅ 无多版本软件")
        st.divider()
        st.header("最早安装的软件 (Top 30)")
        stale = pd.read_sql_query("SELECT name AS 软件名称, version AS 版本号, install_date AS 安装日期 FROM software WHERE install_date IS NOT NULL AND install_date != '' ORDER BY install_date ASC LIMIT 30", conn)
        if not stale.empty:
            stale["安装日期"] = stale["安装日期"].apply(lambda x: _format_date(x) if pd.notna(x) else "-")
            st.dataframe(stale, use_container_width=True, hide_index=True)

# ===== TAB 3: DISKS =====
with tabs[3]:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='disks'")
    if cur.fetchone() is None:
        st.warning("磁盘数据表未创建。运行: python disk_to_sqlite.py")
    else:
        df_disks = pd.read_sql_query("SELECT name,total_gb,used_gb,free_gb,usage_pct,root,description FROM disks ORDER BY name", conn)
        if df_disks.empty: st.info("磁盘数据为空")
        else:
            st.header("📑 磁盘概览")
            c_row = df_disks[df_disks["name"].str.upper() == "C"]
            if not c_row.empty and c_row.iloc[0]["usage_pct"] > 80:
                st.warning(f"⚠️ C盘空间不足！已用 {c_row.iloc[0]['usage_pct']:.1f}%，剩余 {c_row.iloc[0]['free_gb']:.1f} GB")
            for _, row in df_disks.iterrows():
                name, total, used, free, pct = row["name"], row["total_gb"], row["used_gb"], row["free_gb"], row["usage_pct"]
                root = row.get("root") or ""; desc = row.get("description") or ""
                color = "#28a745" if pct < 70 else ("#ffc107" if pct < 90 else "#dc3545")
                ca, cb = st.columns([3, 1])
                with ca:
                    lb = f"📁 {name} 盘 ({desc})" if desc else f"📁 {name} 盘"
                    if root and os.path.exists(root) and st.button(lb, key=f"disk_{name}", use_container_width=True):
                        os.startfile(root)
                    st.markdown(f"<div style='background:#e9ecef;border-radius:4px;height:20px;width:100%'><div style='background:{color};border-radius:4px;height:20px;width:{min(pct,100):.1f}%;text-align:center;color:#fff;font-size:12px;line-height:20px'>{pct:.1f}%</div></div>", unsafe_allow_html=True)
                with cb: st.metric(f"{name}:", f"{used:.1f} GB / {total:.1f} GB", f"剩余 {free:.1f} GB")
                st.caption(f"已用 {used:.1f} GB · 剩余 {free:.1f} GB · 共 {total:.1f} GB")
                st.divider()

# ===== TAB 4: STORAGE =====
with tabs[4]:
    st.header("📊 存储空间分析")
    dirs_info = [
        ("Downloads", "下载目录", "C:/Users/Administrator/Downloads"),
        ("Desktop", "桌面", "C:/Users/Administrator/Desktop"),
        ("Documents", "文档", "C:/Users/Administrator/Documents"),
        ("WeChat Files", "微信文件", "D:/WeChat Files"),
        ("Obsidian", "知识库", "E:/知识库obsidian"),
        ("Projects", "项目目录", "E:/创业项目"),
    ]
    results = []
    for name, label, dpath in dirs_info:
        dpath_norm = os.path.normpath(dpath)
        if os.path.exists(dpath_norm):
            total_size = 0; file_count = 0
            for dirpath, _, filenames in os.walk(dpath_norm):
                for fn in filenames:
                    fp = os.path.join(dirpath, fn)
                    try:
                        if os.path.exists(fp): total_size += os.path.getsize(fp); file_count += 1
                    except: pass
            results.append({"目录": label, "路径": dpath, "文件数": file_count, "大小(MB)": round(total_size/1048576, 1)})
        else:
            results.append({"目录": label, "路径": dpath, "文件数": 0, "大小(MB)": 0})
    df_st = pd.DataFrame(results).sort_values("大小(MB)", ascending=False)
    st.dataframe(df_st, use_container_width=True, hide_index=True)

# ===== TAB 5: DIGITAL ASSETS =====
with tabs[5]:
    st.header("🌐 数字资产中心")
    df_assets = pd.read_sql_query("SELECT * FROM digital_assets WHERE is_enabled=1 ORDER BY sort_order, name", conn)
    categories = sorted(df_assets["category"].unique().tolist())
    
    col_side, col_main = st.columns([1.5, 4.5])
    
    with col_side:
        st.subheader("分类")
        if st.button("📋 全部", key="da_all", use_container_width=True):
            st.session_state.da_cat = "全部"
        for cat in categories:
            cnt = len(df_assets[df_assets["category"] == cat])
            if st.button(f"{cat} ({cnt})", key=f"da_cat_{cat}", use_container_width=True):
                st.session_state.da_cat = cat
        st.divider()
        with st.expander("➕ 新增分类"):
            new_cat = st.text_input("新分类名", key="da_new_cat")
            if st.button("创建分类", key="da_create_cat") and new_cat:
                cur.execute("INSERT INTO digital_assets (category,name,url,created_at,updated_at) VALUES (?,'','',datetime('now','localtime'),datetime('now','localtime'))", (new_cat,))
                conn.commit()
                st.success(f"分类 {new_cat} 已创建")
                st.rerun()
    
    with col_main:
        sel_cat = st.session_state.get("da_cat", "全部")
        df_view = df_assets[df_assets["category"] == sel_cat] if sel_cat != "全部" else df_assets
        st.caption(f"共 {len(df_view)} 条")
        
        if st.button("➕ 新增资产", key="da_add_btn"):
            st.session_state.da_show_form = True
            st.session_state.da_edit_id = None
        
        if st.session_state.get("da_show_form"):
            edit_id = st.session_state.get("da_edit_id")
            row = df_assets[df_assets["id"] == edit_id].iloc[0] if edit_id and len(df_assets[df_assets["id"] == edit_id]) > 0 else None
            st.subheader(("编辑: "+row["name"]) if row is not None else "新增资产")
            with st.form("da_form"):
                name = st.text_input("名称 *", value=row["name"] if row is not None else "", key="da_f_name")
                url = st.text_input("网址 *", value=row["url"] if row is not None else "", key="da_f_url")
                cat_idx = categories.index(row["category"]) if row is not None and row["category"] in categories else 0
                cat = st.selectbox("分类 *", categories, index=cat_idx, key="da_f_cat")
                uname = st.text_input("账号", value=row["username"] if row is not None else "", key="da_f_uname")
                remark = st.text_input("备注", value=row["remark"] if row is not None else "", key="da_f_remark")
                c1, c2 = st.columns(2)
                saved = c1.form_submit_button("💾 保存")
                cancelled = c2.form_submit_button("取消")
                if saved and name and url:
                    now = pd.Timestamp.now().isoformat()
                    if edit_id and row is not None:
                        cur.execute("UPDATE digital_assets SET name=?,url=?,category=?,username=?,remark=?,updated_at=? WHERE id=?", (name,url,cat,uname,remark,now,edit_id))
                    else:
                        cur.execute("INSERT INTO digital_assets (category,name,url,username,remark,created_at,updated_at) VALUES (?,?,?,?,?,?,?)", (cat,name,url,uname,remark,now,now))
                    conn.commit()
                    st.session_state.da_show_form = False; st.session_state.da_edit_id = None
                    st.rerun()
                if cancelled:
                    st.session_state.da_show_form = False; st.session_state.da_edit_id = None
                    st.rerun()
        
        if not df_view.empty:
            for _, row in df_view.iterrows():
                c1,c2,c3,c4,c5 = st.columns([2.5, 3, 1.2, 0.8, 0.8])
                c1.write(f"**{row['name']}**")
                c2.write(str(row['url'])[:50] + ("..." if len(str(row['url'])) > 50 else ""))
                c3.write(str(row['username']) if row['username'] else "—")
                if c4.button("🚀", key=f"da_open_{row['id']}"):
                    _webbrowser.open(row['url'])
                if c5.button("✏️", key=f"da_edit_{row['id']}"):
                    st.session_state.da_show_form = True; st.session_state.da_edit_id = row['id']; st.rerun()
                with st.expander(f"详情"):
                    st.write(f"URL: {row['url']}")
                    st.write(f"分类: {row['category']}")
                    st.write(f"账号: {row['username'] or '—'}")
                    st.write(f"备注: {row['remark'] or '—'}")
                    if st.button("🗑️ 删除", key=f"da_del_{row['id']}"):
                        cur.execute("DELETE FROM digital_assets WHERE id=?", (row['id'],)); conn.commit()
                        st.success("已删除"); st.rerun()
        else:
            st.info("暂无资产")

# ===== TABS 6-9: FUTURE MODULES =====
for i, (tab, name) in enumerate([(tabs[6], "备份中心"), (tabs[7], "项目管理中心"), (tabs[8], "知识库中心"), (tabs[9], "Prompt管理中心"), (tabs[10], "设置中心")]):
    with tab:
        st.header(f"🚧 {name}")
        st.info(f"{name} - Future Module（待开发）")

conn.close()
