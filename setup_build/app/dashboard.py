"""
个人数字资产管家 (GraceOS V2.1)
Asset Management Platform: Analyze -> Suggest -> Execute
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import sqlite3
import pandas as pd
import subprocess
import shutil
from datetime import date
from analyzers.health_scorer import calculate as calc_health

DB_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\graceos.db"
ARCHIVE_DIR = r"E:\归档"
RECYCLE_DIR = r"E:\回收站"

# System protection paths
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

def _format_last_modified(val):
    if not val: return "-"
    s = str(val).strip()
    if len(s) >= 10: return s[:10]
    return s

def _format_install_date(val):
    s = str(val).strip()
    if len(s) == 8 and s.isdigit(): return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s if s else "-"

def _safe_delete(fp):
    """Move to recycle bin"""
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
    """Batch delete files to recycle bin"""
    ok, fail = 0, 0
    for fp in files:
        success, _ = _safe_delete(fp)
        if success: ok += 1
        else: fail += 1
    return ok, fail

def _archive_file(fp):
    """Move to archive dir preserving structure"""
    try:
        rel = os.path.relpath(fp, "C:\\")
        target = os.path.join(ARCHIVE_DIR, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.move(fp, target)
        return True, target
    except Exception as e:
        return False, str(e)

def _launch_software(install_path, sw_name):
    """Try to launch software from install path"""
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

def _render_file_table(df, section_key, max_rows=50, show_date=True, batch_delete=False):
    """Render a file table with optional date column and batch delete support"""
    if df.empty: st.info("没有找到匹配的文件"); return
    full_df = df.head(max_rows).copy()
    display = full_df.copy()
    if "last_modified" in df.columns and show_date:
        display = display[["file_name", "size_mb", "last_modified", "file_path"]]
        display.columns = ["文件名", "大小(MB)", "生成日期", "路径"]
        display["生成日期"] = display["生成日期"].apply(_format_last_modified)
    else:
        display = display[["file_name", "size_mb", "file_path"]]
        display.columns = ["文件名", "大小(MB)", "路径"]
    sel_key = f"filesel_{section_key}"
    sel_mode = "multi-row" if batch_delete else "single-row"
    event = st.dataframe(display, use_container_width=True, hide_index=True,
        height=min(35*len(display)+38, 600), on_select="rerun",
        selection_mode=sel_mode, key=f"tbl_{section_key}")
    if event.selection.rows:
        if not batch_delete:
            idx = event.selection.rows[0]
            if idx != st.session_state.get(sel_key, -1):
                st.session_state[sel_key] = idx
                fp = full_df.iloc[idx]["file_path"]
                _open_file(fp)
        else:
            rows = event.selection.rows
            n = len(rows)
            if n > 1:
                selected_files = [full_df.iloc[i]["file_path"] for i in rows]
                selected_mb = sum(full_df.iloc[i]["size_mb"] for i in rows)
                cols = st.columns([3, 1, 1])
                if cols[0].button(f"🗑️ 批量删除 {n} 个文件 (约 {selected_mb:.0f} MB)", key=f"batch_del_{section_key}"):
                    ok, fail = _safe_delete_batch(selected_files)
                    if fail == 0: st.success(f"已删除 {ok} 个,释放约 {selected_mb:.0f} MB")
                    else: st.warning(f"删除 {ok} 个成功, {fail} 个失败")
                    st.rerun()
                if cols[1].button(f"📂 全部打开目录", key=f"batch_open_{section_key}"):
                    for fp in selected_files[:5]:
                        d = os.path.dirname(os.path.normpath(fp))
                        if d and os.path.exists(d): os.startfile(d)
                    st.toast("已打开前5个目录")
            else:
                idx = rows[0]
                fp = full_df.iloc[idx]["file_path"]
                sz = full_df.iloc[idx]["size_mb"]
                cols = st.columns([2, 1, 1])
                if cols[0].button(f"🗑️ 删除 ({sz:.0f} MB)", key=f"del_{section_key}_{idx}"):
                    ok, msg = _safe_delete(fp)
                    if ok: st.success("已移至回收站")
                    else: st.error(msg)
                if cols[1].button("📂 打开", key=f"open_{section_key}_{idx}"):
                    _open_file(fp)

st.set_page_config(page_title="个人数字资产管家", layout="wide")
st.title("个人数字资产管家")

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

tab_names = ["🏠 首页", "📂 文件", "📋 软件", "📑 磁盘", "📊 存储", "💾 备份", "📁 项目", "🧠 知识库", "📝 Prompt", "⚙️ 设置"]
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

tab_cols = st.columns(len(tab_names))
for i, name in enumerate(tab_names):
    t = "primary" if i == st.session_state.active_tab else "secondary"
    if tab_cols[i].button(name, key=f"tabbtn_{i}", use_container_width=True, type=t):
        st.session_state.active_tab = i
        st.rerun()

active = st.session_state.active_tab

# ========== TAB 0: HOME ==========
if active == 0:
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
            c2.metric("文件活跃度", f"{score['unused_score']}/100", f"{score['unused_mb']:.0f}MB未使用")
            c3.metric("磁盘健康度", f"{score['disk_score']}/100", f"C盘 {score['c_pct']:.1f}%")
            c4.metric("软件健康度", f"{score['sw_score']}/100", f"{score['sw_multi']}多版本")

        st.divider()

        st.subheader("资产中心")
        j1, j2, j3, j4 = st.columns(4)
        if j1.button("📂 文件资产中心\n搜索/重复/大文件/未使用", key="jump_file", use_container_width=True):
            st.session_state.active_tab = 1; st.rerun()
        if j2.button("📋 软件资产中心\n已安装软件清单/健康", key="jump_sw", use_container_width=True):
            st.session_state.active_tab = 2; st.rerun()
        if j3.button("📑 磁盘资产中心\n容量/使用率/预警", key="jump_disk", use_container_width=True):
            st.session_state.active_tab = 3; st.rerun()
        if j4.button("📊 存储空间分析\n目录级空间统计", key="jump_store", use_container_width=True):
            st.session_state.active_tab = 4; st.rerun()

        st.divider()

        st.header("🤖 AI 建议中心")
        suggestions = []
        if score["dup_score"] < 20:
            suggestions.append({"icon": "⚠️", "title": "重复文件清理", "desc": f"发现 {score['dup_files']:,} 个重复文件", "action": f"占用 {score['dup_mb']:.0f}MB", "tab_idx": 1, "btn": "查看重复文件"})
        if score["unused_score"] < 15:
            suggestions.append({"icon": "📦", "title": "未使用文件归档", "desc": f"{score['unused_count']:,} 个文件超过90天未使用", "action": f"占用 {score['unused_mb']:.0f}MB", "tab_idx": 1, "btn": "查看未使用文件"})
        if score["disk_score"] < 15:
            suggestions.append({"icon": "🔴", "title": "C盘空间不足", "desc": f"C盘使用率 {score['c_pct']:.1f}%", "action": "剩余空间不足", "tab_idx": 3, "btn": "查看磁盘详情"})
        if score["sw_score"] < 20:
            suggestions.append({"icon": "🔄", "title": "多版本软件", "desc": f"{score['sw_multi']} 个软件存在多版本", "action": "建议清理旧版本", "tab_idx": 2, "btn": "查看软件健康"})

        if not suggestions:
            st.success("✅ 各项指标良好，暂无建议")

        for i, s in enumerate(suggestions):
            cols = st.columns([6, 2, 2])
            cols[0].write(f"{s['icon']} **{s['title']}**: {s['desc']} ({s['action']})")
            if cols[1].button(s["btn"], key=f"sug_{i}"):
                st.session_state.active_tab = s["tab_idx"]
                st.rerun()

    st.divider()
    if st.button("🔄 刷新评分", key="refresh_score"):
        st.rerun()

# ========== TAB 1: FILE ==========
if active == 1:
    cur.execute("SELECT COUNT(*) FROM files"); fc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM (SELECT file_name, file_size FROM files GROUP BY file_name, file_size HAVING COUNT(*)>1)"); dg = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(cnt),0) FROM (SELECT COUNT(*) AS cnt FROM files GROUP BY file_name, file_size HAVING COUNT(*)>1)"); dfc = cur.fetchone()[0]
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("文件总数", f"{fc:,}")
    with c2: st.metric("重复组数", f"{dg:,}")
    with c3: st.metric("重复文件", f"{dfc:,}")
    c4.metric("数据库","SQLite")

    st.divider()
    st.header("🔍 文件搜索")
    kw = st.text_input("输入文件名称关键字", placeholder="如: .pdf, 报告...", key="file_search")
    if kw:
        df = pd.read_sql_query(f"SELECT file_name,file_path,last_modified,ROUND(file_size/1048576.0,2) AS size_mb FROM files WHERE file_name LIKE ? {SHORTCUT_FILTER} ORDER BY file_size DESC LIMIT 100", conn, params=[f"%{kw}%"])
        st.caption(f"找到 {len(df)} 条结果")
        _render_file_table(df, "search", show_date=True, batch_delete=True)

    st.divider()

    # === DUPLICATE FILE ACTION CENTER ===
    st.header("🔧 重复文件处理中心")
    df_dup = pd.read_sql_query("""SELECT file_name, ROUND(file_size/1048576.0,2) AS size_mb, COUNT(*) AS dc, MIN(file_path) AS sample_path, MAX(file_path) AS dup_path FROM files GROUP BY file_name, file_size HAVING COUNT(*) > 1 ORDER BY dc DESC LIMIT 100""", conn)

    if not df_dup.empty:
        total_dup_mb = (df_dup["size_mb"] * (df_dup["dc"] - 1)).sum()
        st.caption(f"前100重复组，保留一份可释放约 {total_dup_mb:.0f} MB")
        disp = df_dup.copy()
        disp = disp[["file_name", "size_mb", "dc", "sample_path", "dup_path"]]
        disp.columns = ["文件名", "大小(MB)", "重复数", "建议保留", "建议删除"]

        event_dup = st.dataframe(disp, use_container_width=True, hide_index=True, height=400,
            on_select="rerun", selection_mode="multi-row", key="tbl_dupact")

        if event_dup.selection.rows:
            rows = event_dup.selection.rows
            n = len(rows)
            if n > 1:
                to_delete = []
                total_mb = 0
                for idx in rows:
                    row = df_dup.iloc[idx]
                    to_delete.append(row["dup_path"])
                    total_mb += row["size_mb"]
                cols = st.columns([3, 1])
                if cols[0].button(f"🗑️ 批量删除 {n} 组副本 (约 {total_mb:.0f} MB)", key=f"batch_del_dup"):
                    ok, fail = _safe_delete_batch(to_delete)
                    if fail == 0: st.success(f"已删除 {ok} 个副本,释放约 {total_mb:.0f} MB")
                    else: st.warning(f"删除 {ok} 个成功, {fail} 个失败")
                    st.rerun()
            else:
                idx = rows[0]
                row = df_dup.iloc[idx]
                keep = row["sample_path"]
                dup = row["dup_path"]
                sz = row["size_mb"]
                st.info(f"**建议保留**: {keep}\n\n**建议删除**: {dup}\n\n释放空间: {sz:.0f} MB")
                cdel, carc = st.columns(2)
                if cdel.button(f"🗑️ 删除副本 ({sz:.0f}MB)", key=f"del_dup_{idx}"):
                    ok, msg = _safe_delete(dup)
                    if ok: st.success(f"已移至回收站: {msg}")
                    else: st.error(msg)
                if carc.button(f"📦 归档副本", key=f"arc_dup_{idx}"):
                    ok, msg = _archive_file(dup)
                    if ok: st.success(f"已归档: {msg}")
                    else: st.error(msg)
    else:
        st.info("无重复文件")

    st.divider()
    st.header("📦 Top 100 大文件")
    df_big = pd.read_sql_query(f"SELECT file_name,file_path,last_modified,ROUND(file_size/1048576.0,2) AS size_mb FROM files WHERE 1=1 {SHORTCUT_FILTER} ORDER BY file_size DESC LIMIT 100", conn)
    _render_file_table(df_big, "big", show_date=True, batch_delete=True)

    st.divider()

    # === UNUSED FILE ACTION CENTER ===
    st.header("🕐 长期未使用文件处理中心")
    df_old = pd.read_sql_query(f"SELECT file_name,file_path,last_modified,ROUND(file_size/1048576.0,2) AS size_mb FROM files WHERE 1=1 AND NOT (file_path LIKE '%Windows%' OR file_path LIKE '%System32%' OR file_name IN ('pagefile.sys','hiberfil.sys','swapfile.sys')) {SHORTCUT_FILTER} ORDER BY last_modified ASC LIMIT 100", conn)
    if not df_old.empty:
        total_old_mb = df_old["size_mb"].sum()
        st.caption(f"前100个最久未使用文件，共 {total_old_mb:.0f} MB（已排除系统文件）")
        disp_old = df_old[["file_name","size_mb","last_modified","file_path"]].head(100).copy()
        disp_old.columns = ["文件名","大小(MB)","生成日期","路径"]
        disp_old["生成日期"] = disp_old["生成日期"].apply(_format_last_modified)

        event_old = st.dataframe(disp_old, use_container_width=True, hide_index=True, height=400,
            on_select="rerun", selection_mode="multi-row", key="tbl_oldact")

        if event_old.selection.rows:
            rows = event_old.selection.rows
            n = len(rows)
            if n > 1:
                selected_files = [df_old.iloc[i]["file_path"] for i in rows]
                selected_mb = sum(df_old.iloc[i]["size_mb"] for i in rows)
                cols = st.columns([3, 1])
                if cols[0].button(f"🗑️ 批量删除 {n} 个文件 (约 {selected_mb:.0f} MB)", key=f"batch_del_old"):
                    ok, fail = _safe_delete_batch(selected_files)
                    if fail == 0: st.success(f"已删除 {ok} 个,释放约 {selected_mb:.0f} MB")
                    else: st.warning(f"删除 {ok} 个成功, {fail} 个失败")
                    st.rerun()
            else:
                idx = rows[0]
                row = df_old.iloc[idx]
                fp = row["file_path"]
                sz = row["size_mb"]
                dt = _format_last_modified(row["last_modified"])
                st.info(f"**文件**: {row['file_name']}\n**日期**: {dt}\n**路径**: {fp}\n**大小**: {sz:.0f} MB")
                c1, c2, c3 = st.columns(3)
                if c1.button(f"🗑️ 删除", key=f"del_old_{idx}"):
                    ok, msg = _safe_delete(fp)
                    if ok: st.success(f"已移至回收站")
                    else: st.error(msg)
                if c2.button(f"📦 归档", key=f"arc_old_{idx}"):
                    ok, msg = _archive_file(fp)
                    if ok: st.success(f"已归档")
                    else: st.error(msg)
                if c3.button(f"📂 打开", key=f"open_old_{idx}"):
                    _open_file(fp)
    else:
        st.info("无长期未使用文件")

# ========== TAB 2: SOFTWARE ==========
if active == 2:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='software'")
    if cur.fetchone() is None:
        st.warning("软件数据表未创建。运行: python software_to_sqlite.py")
    else:
        cur.execute("SELECT COUNT(*) FROM software"); sw_count = cur.fetchone()[0]
        st.metric("软件总数", f"{sw_count}")
        st.divider()

        st.header("🔍 软件搜索")
        c1, c2 = st.columns([3, 1])
        with c1: sw_kw = st.text_input("搜索软件名称", placeholder="例: Python, Docker...", key="sw_search")
        with c2: sort_by = st.selectbox("排序", ["名称 A-Z", "名称 Z-A", "安装日期 新→旧", "安装日期 旧→新"], key="sw_sort")
        wc = "WHERE name LIKE ?" if sw_kw else ""
        params_sw = [f"%{sw_kw}%"] if sw_kw else []
        sm = {"名称 A-Z": "name ASC", "名称 Z-A": "name DESC", "安装日期 新→旧": "install_date DESC", "安装日期 旧→新": "install_date ASC"}
        oc = sm.get(sort_by, "name ASC")
        sql_sw = f"SELECT name AS 软件名称, install_date AS 安装日期, install_path AS 安装路径 FROM software {wc} ORDER BY {oc} LIMIT 200"
        df_sw = pd.read_sql_query(sql_sw, conn, params=params_sw)
        if not df_sw.empty:
            df_sw["安装日期"] = df_sw["安装日期"].apply(lambda x: _format_install_date(x) if pd.notna(x) else "-")
        st.caption(f"找到 {len(df_sw)} 条")
        if not df_sw.empty:
            sel_key = "swsel_main"
            event = st.dataframe(df_sw, use_container_width=True, hide_index=True,
                height=min(35*len(df_sw)+38, 600), on_select="rerun",
                selection_mode="single-row", key="swtbl_main")
            if event.selection.rows:
                idx = event.selection.rows[0]
                if idx != st.session_state.get(sel_key, -1):
                    st.session_state[sel_key] = idx
                    ip = df_sw.iloc[idx].get("安装路径") or ""
                    sw_name = str(df_sw.iloc[idx]["软件名称"])
                    launched, result = _launch_software(ip, sw_name)
                    if launched:
                        st.toast(f"启动: {sw_name}")
                    else:
                        st.toast("无安装路径，无法启动")

        st.divider()

        # === MULTI-VERSION SOFTWARE ACTION CENTER ===
        st.header("🔬 多版本软件处理中心")
        dup_sw = pd.read_sql_query("SELECT name AS 软件名称, COUNT(*) AS 版本数, GROUP_CONCAT(version,', ') AS 所有版本, MAX(version) AS 最新版本, MIN(version) AS 最旧版本 FROM software GROUP BY name HAVING COUNT(*) > 1 ORDER BY 版本数 DESC", conn)
        if not dup_sw.empty:
            st.caption("同一软件安装了多个版本，建议保留最新版本")
            disp_sw = dup_sw[["软件名称", "版本数", "最新版本", "最旧版本"]].copy()
            event_sw = st.dataframe(disp_sw, use_container_width=True, hide_index=True, height=350,
                on_select="rerun", selection_mode="multi-row", key="tbl_swact")
            if event_sw.selection.rows:
                rows = event_sw.selection.rows
                if len(rows) == 1:
                    idx = rows[0]
                    row = dup_sw.iloc[idx]
                    st.info(f"**{row['软件名称']}**\n所有版本: {row['所有版本']}\n\n💡 建议保留: {row['最新版本']}\n⚠️ 建议卸载: {row['最旧版本']}")
                    cols = st.columns(2)
                    if cols[0].button(f"🗑️ 卸载旧版本 ({row['最旧版本']})", key=f"uninst_{idx}"):
                        try:
                            subprocess.run(["winget", "uninstall", "--name", row['软件名称'], "--version", str(row['最旧版本'])], capture_output=True, timeout=30)
                            st.toast(f"已发起卸载: {row['软件名称']} {row['最旧版本']}")
                        except Exception as e:
                            st.warning(f"winget 卸载失败，请手动卸载: {e}")
                    if cols[1].button(f"⚡ winget搜索 {row['软件名称']}", key=f"winget_{idx}"):
                        try:
                            r = subprocess.run(["winget", "search", row["软件名称"]], capture_output=True, timeout=15)
                            st.code(r.stdout.decode("utf-8", errors="replace")[:2000] or "无结果")
                        except Exception as e:
                            st.warning(f"winget 不可用: {e}")
                else:
                    sw_names = [str(dup_sw.iloc[i]["软件名称"]) for i in rows]
                    if st.button(f"🗑️ 批量卸载 {len(rows)} 个软件的最旧版本", key=f"batch_uninst_sw"):
                        for i in rows:
                            row = dup_sw.iloc[i]
                            try:
                                subprocess.run(["winget", "uninstall", "--name", str(row['软件名称']), "--version", str(row['最旧版本'])], capture_output=True, timeout=30)
                            except: pass
                        st.toast(f"已发起批量卸载 {len(rows)} 个软件")
        else:
            st.success("✅ 无多版本软件")

        st.divider()
        st.header("最早安装的软件 (Top 30)")
        stale = pd.read_sql_query("SELECT name AS 软件名称, version AS 版本号, install_date AS 安装日期 FROM software WHERE install_date IS NOT NULL AND install_date != '' ORDER BY install_date ASC LIMIT 30", conn)
        if not stale.empty:
            stale["安装日期"] = stale["安装日期"].apply(lambda x: _format_install_date(x) if pd.notna(x) else "-")
            st.dataframe(stale, use_container_width=True, hide_index=True)

# ========== TAB 3: DISKS ==========
if active == 3:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='disks'")
    if cur.fetchone() is None:
        st.warning("磁盘数据表未创建。运行: python disk_to_sqlite.py")
    else:
        df_disks=pd.read_sql_query("SELECT name,total_gb,used_gb,free_gb,usage_pct,root,description FROM disks ORDER BY name",conn)
        if df_disks.empty: st.info("磁盘数据为空")
        else:
            st.header("📑 磁盘概览")
            c_row=df_disks[df_disks["name"].str.upper()=="C"]
            if not c_row.empty and c_row.iloc[0]["usage_pct"]>80:
                st.warning(f"⚠️ C盘空间不足！已用 {c_row.iloc[0]['usage_pct']:.1f}%，剩余 {c_row.iloc[0]['free_gb']:.1f} GB")
            for _,row in df_disks.iterrows():
                name,total,used,free,pct=row["name"],row["total_gb"],row["used_gb"],row["free_gb"],row["usage_pct"]
                root=row.get("root") or ""; desc=row.get("description") or ""
                color="#28a745" if pct<70 else ("#ffc107" if pct<90 else "#dc3545")
                ca,cb=st.columns([3,1])
                with ca:
                    lb=f"📁 {name} 盘 ({desc})" if desc else f"📁 {name} 盘"
                    if root and os.path.exists(root) and st.button(lb,key=f"disk_{name}",use_container_width=True):
                        os.startfile(root)
                    st.markdown(f"""<div style='background:#e9ecef;border-radius:4px;height:20px;width:100%'><div style='background:{color};border-radius:4px;height:20px;width:{min(pct,100):.1f}%;text-align:center;color:#fff;font-size:12px;line-height:20px'>{pct:.1f}%</div></div>""",unsafe_allow_html=True)
                with cb: st.metric(f"{name}:",f"{used:.1f} GB / {total:.1f} GB",f"剩余 {free:.1f} GB")
                st.caption(f"已用 {used:.1f} GB · 剩余 {free:.1f} GB · 共 {total:.1f} GB")
                st.divider()

# ========== TAB 4: STORAGE ==========
if active == 4:
    st.header("📊 存储空间分析")
    dirs_info=[
        ("Downloads","下载目录","C:/Users/Administrator/Downloads"),
        ("Desktop","桌面","C:/Users/Administrator/Desktop"),
        ("Documents","文档","C:/Users/Administrator/Documents"),
        ("WeChat Files","微信文件","D:/WeChat Files"),
        ("Obsidian","知识库","E:/知识库obsidian"),
        ("Projects","项目目录","E:/知识库obsidian/02_Projects/graceos"),
    ]
    results=[]
    for name,label,dpath in dirs_info:
        dpath_norm=os.path.normpath(dpath)
        if os.path.exists(dpath_norm):
            total_size=0; file_count=0
            for dirpath,_,filenames in os.walk(dpath_norm):
                for fn in filenames:
                    fp=os.path.join(dirpath,fn)
                    try:
                        if os.path.exists(fp): total_size+=os.path.getsize(fp); file_count+=1
                    except: pass
            results.append({"目录":label,"路径":dpath,"文件数":file_count,"大小(MB)":round(total_size/1048576,1)})
        else: results.append({"目录":label,"路径":dpath,"文件数":0,"大小(MB)":0})
    df_st=pd.DataFrame(results).sort_values("大小(MB)",ascending=False)
    st.dataframe(df_st,use_container_width=True,hide_index=True)

# ========== TABS 5-9: FUTURE MODULES ==========
if active >= 5:
    future_names = {5: "备份中心", 6: "项目管理中心", 7: "知识库中心", 8: "Prompt管理中心", 9: "设置中心"}
    name = future_names.get(active, "Future Module")
    st.header(f"🚧 {name}")
    st.info(f"{name} - Future Module（待开发）")
    st.caption("此模块将在后续版本中实现")

conn.close()
