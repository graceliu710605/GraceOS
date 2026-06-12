"""
GraceOS V2 - Personal Digital Operating System
Tabs: Home | Files | Software | Disks | Storage | Backup | Projects | Knowledge | Prompts | Settings
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import sqlite3
import pandas as pd
import os
import subprocess
from datetime import date
from analyzers.health_scorer import calculate as calc_health, get_latest as get_health

DB_FILE = r"E:\创业项目\GraceOS\09_Database\graceos.db"
SHORTCUT_FILTER = " AND file_name NOT LIKE '%=%' AND file_name NOT LIKE 'ms-%' AND file_name NOT LIKE 'shell:%' AND file_name NOT LIKE 'file:///%'"

def _open_file(path):
    norm = os.path.normpath(path)
    if os.path.exists(norm): os.startfile(norm)
    else: st.toast("文件不存在")

def _format_install_date(val):
    s = str(val).strip()
    if len(s) == 8 and s.isdigit(): return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s

def _render_file_table(df, section_key, max_rows=50):
    if df.empty: st.info("没有找到匹配的文件"); return
    display = df.head(max_rows).copy()
    display = display[["file_name", "size_mb", "file_path"]]
    display.columns = ["文件名", "大小(MB)", "路径"]
    sel_key = f"filesel_{section_key}"
    event = st.dataframe(display, use_container_width=True, hide_index=True,
        height=min(35*len(display)+38, 600), on_select="rerun", selection_mode="single-row", key=f"tbl_{section_key}")
    if event.selection.rows:
        idx = event.selection.rows[0]
        if idx != st.session_state.get(sel_key, -1):
            st.session_state[sel_key] = idx
            _open_file(df.iloc[idx]["file_path"])

st.set_page_config(page_title="GraceOS V2", layout="wide")
st.title("GraceOS V2 - 个人数字操作系统")

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# ===== 10 Tabs =====
tabs = st.tabs(["🏠 首页", "📂 文件", "📋 软件", "📑 磁盘", "📊 存储", "💾 备份", "📁 项目", "🧠 知识库", "📝 Prompt", "⚙️ 设置"])

# ========== TAB 0: 首页仪表盘 ==========
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
            c1.metric("重复文件", f"{score['dup_score']}/25", f"{score['dup_files']:,}个")
            c2.metric("未使用文件", f"{score['unused_score']}/25", f"{score['unused_mb']:.0f}MB")
            c3.metric("磁盘空间", f"{score['disk_score']}/25", f"C盘 {score['c_pct']:.1f}%")
            c4.metric("软件健康", f"{score['sw_score']}/25", f"{score['sw_multi']}个多版本")

        st.divider()
        st.subheader("关键指标")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("文件总数", f"{score['total_files']:,}")
        m2.metric("重复文件组", f"{score['dup_count']:,}")
        m3.metric("重复占用", f"{score['dup_mb']:.0f} MB")
        m4.metric("软件总数", f"{score['sw_count']}")

        st.divider()
        st.subheader("问题列表")
        issues = []
        if score["dup_score"] < 20: issues.append(f"⚠️ 重复文件过多（{score['dup_files']:,}个），扣{25-score['dup_score']}分")
        if score["unused_score"] < 15: issues.append(f"⚠️ 长期未使用文件占用 {score['unused_mb']:.0f}MB，扣{25-score['unused_score']}分")
        if score["disk_score"] < 15: issues.append(f"⚠️ C盘使用率 {score['c_pct']:.1f}%，扣{25-score['disk_score']}分")
        if score["sw_score"] < 20: issues.append(f"⚠️ {score['sw_multi']}个软件存在多版本，扣{25-score['sw_score']}分")
        if not issues: issues.append("✅ 各项指标良好，暂无问题")
        for i in issues: st.write(i)

        st.divider()
        st.subheader("历史趋势")
        hist = pd.read_sql_query("SELECT score_date, total_score FROM health_scores ORDER BY score_date DESC LIMIT 14", conn)
        if len(hist) > 1:
            hist = hist.iloc[::-1]
            st.line_chart(hist.set_index("score_date"))
    else:
        st.info("评分数据计算中...")

    if st.button("🔄 刷新评分", key="refresh_score"):
        calc_health(conn)
        st.rerun()

# ========== TAB 1: 文件资产 ==========
with tabs[1]:
    cur.execute("SELECT COUNT(*) FROM files")
    fc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM (SELECT file_name, file_size FROM files GROUP BY file_name, file_size HAVING COUNT(*)>1)")
    dg = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(cnt),0) FROM (SELECT COUNT(*) AS cnt FROM files GROUP BY file_name, file_size HAVING COUNT(*)>1)")
    dfc = cur.fetchone()[0]
    c1,c2,c3,c4=st.columns(4)
    with c1:
        with st.expander(f"文件总数: {fc:,}"):
            st.dataframe(pd.read_sql_query("SELECT file_name,file_path,ROUND(file_size/1048576.0,2) AS size_mb,last_modified FROM files ORDER BY file_size DESC LIMIT 200",conn), use_container_width=True, hide_index=True, height=400)
    with c2:
        with st.expander(f"重复组数: {dg:,}"):
            st.dataframe(pd.read_sql_query("SELECT file_name,ROUND(file_size/1048576.0,2) AS size_mb,COUNT(*) AS dc,MIN(file_path) AS sample_path FROM files GROUP BY file_name,file_size HAVING COUNT(*)>1 ORDER BY dc DESC LIMIT 100",conn), use_container_width=True, hide_index=True, height=400)
    with c3:
        with st.expander(f"重复文件: {dfc:,}"):
            st.dataframe(pd.read_sql_query("SELECT file_name,file_path,ROUND(file_size/1048576.0,2) AS size_mb,last_modified FROM files ORDER BY last_modified ASC LIMIT 200",conn), use_container_width=True, hide_index=True, height=400)
    c4.metric("数据库","SQLite")
    st.divider()
    st.header("🔍 文件搜索")
    kw = st.text_input("输入文件名称关键字", placeholder="如: .pdf, 报告...", key="file_search")
    if kw:
        df = pd.read_sql_query(f"SELECT file_name,file_path,ROUND(file_size/1048576.0,2) AS size_mb FROM files WHERE file_name LIKE ? {SHORTCUT_FILTER} ORDER BY file_size DESC LIMIT 100", conn, params=[f"%{kw}%"])
        st.caption(f"找到 {len(df)} 条结果")
        _render_file_table(df,"search")
    st.divider()
    st.header("📦 Top 100 大文件")
    df_big = pd.read_sql_query(f"SELECT file_name,file_path,ROUND(file_size/1048576.0,2) AS size_mb FROM files WHERE 1=1 {SHORTCUT_FILTER} ORDER BY file_size DESC LIMIT 100", conn)
    _render_file_table(df_big,"big")
    st.divider()
    st.header("🔧 重复文件统计")
    st.dataframe(pd.read_sql_query("SELECT file_name,ROUND(file_size/1048576.0,2) AS size_mb,COUNT(*) AS dc,MIN(file_path) AS sample_path FROM files GROUP BY file_name,file_size HAVING COUNT(*)>1 ORDER BY dc DESC LIMIT 50",conn), use_container_width=True, hide_index=True, height=400)
    st.divider()
    st.header("🕐 长期未使用文件")
    df_old = pd.read_sql_query(f"SELECT file_name,file_path,last_modified,ROUND(file_size/1048576.0,2) AS size_mb FROM files WHERE 1=1 {SHORTCUT_FILTER} ORDER BY last_modified ASC LIMIT 50", conn)
    _render_file_table(df_old,"old")

# ========== TAB 2: 软件资产中心 ==========
with tabs[2]:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='software'")
    if cur.fetchone() is None:
        st.warning("软件数据表未创建。运行: python software_to_sqlite.py")
    else:
        cur.execute("SELECT COUNT(*) FROM software")
        st.metric("软件总数", f"{cur.fetchone()[0]}")
        st.divider()
        st.header("🔍 软件搜索")
        c1,c2=st.columns([3,1])
        with c1: sw_kw=st.text_input("搜索软件名称",placeholder="例: Python, Docker...",key="sw_search")
        with c2: sort_by=st.selectbox("排序",["名称 A-Z","名称 Z-A","安装日期 新→旧","安装日期 旧→新"],key="sw_sort")
        wc="WHERE name LIKE ?" if sw_kw else ""
        params=[f"%{sw_kw}%"] if sw_kw else []
        sm={"名称 A-Z":"name ASC","名称 Z-A":"name DESC","安装日期 新→旧":"install_date DESC","安装日期 旧→新":"install_date ASC"}
        oc=sm.get(sort_by,"name ASC")
        sql=f"SELECT name,install_date,install_path FROM software {wc} ORDER BY {oc} LIMIT 200"
        df_sw=pd.read_sql_query(sql,conn,params=params)
        if not df_sw.empty: df_sw["install_date"]=df_sw["install_date"].apply(lambda x:_format_install_date(x) if pd.notna(x) else "-")
        st.caption(f"找到 {len(df_sw)} 条软件记录")

        # Table display
        if not df_sw.empty:
            disp=df_sw.copy()
            disp.columns=["软件名称","安装日期","安装路径"]
            sel_key="swsel_main"
            event=st.dataframe(disp,use_container_width=True,hide_index=True,height=min(35*len(disp)+38,600),on_select="rerun",selection_mode="single-row",key="swtbl_main")
            if event.selection.rows:
                idx=event.selection.rows[0]
                if idx!=st.session_state.get(sel_key,-1):
                    st.session_state[sel_key]=idx
                    ip=df_sw.iloc[idx].get("install_path") or ""
                    if ip and os.path.exists(ip): os.startfile(ip)
                    else: st.toast("无安装路径")

        # SW Health Analysis
        st.divider()
        st.header("🔬 软件健康分析")
        dup_sw=pd.read_sql_query("SELECT name,COUNT(*) AS ver_count,GROUP_CONCAT(version,', ') AS versions FROM software GROUP BY name HAVING COUNT(*)>1 ORDER BY ver_count DESC",conn)
        if not dup_sw.empty:
            st.subheader(f"多版本软件 ({len(dup_sw)} 个)")
            st.caption("同一软件安装了多个版本，建议只保留最新版本")
            st.dataframe(dup_sw, use_container_width=True, hide_index=True)
        else:
            st.success("✅ 无多版本软件")

        stale=pd.read_sql_query("SELECT name,version,install_date FROM software WHERE install_date IS NOT NULL AND install_date != '' ORDER BY install_date ASC LIMIT 30",conn)
        if not stale.empty:
            st.subheader("最早安装的软件 (Top 30)")
            st.dataframe(stale, use_container_width=True, hide_index=True)
        else:
            st.info("无安装日期数据")

# ========== TAB 3: 磁盘资产中心 ==========
with tabs[3]:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='disks'")
    if cur.fetchone() is None:
        st.warning("磁盘数据表未创建。运行: python disk_to_sqlite.py")
    else:
        df_disks=pd.read_sql_query("SELECT name,total_gb,used_gb,free_gb,usage_pct,root,description FROM disks ORDER BY name",conn)
        if df_disks.empty:
            st.info("磁盘数据为空")
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

# ========== TAB 4: 存储空间分析 ==========
with tabs[4]:
    st.header("📊 存储空间分析")
    dirs_info=[
        ("Downloads", "下载目录", "C:/Users/Administrator/Downloads"),
        ("Desktop", "桌面", "C:/Users/Administrator/Desktop"),
        ("Documents", "文档", "C:/Users/Administrator/Documents"),
        ("WeChat Files", "微信文件", "D:/WeChat Files"),
        ("Obsidian", "知识库", "E:/知识库obsidian"),
        ("Projects", "项目目录", "E:/创业项目"),
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
        else:
            results.append({"目录":label,"路径":dpath,"文件数":0,"大小(MB)":0})
    df_st=pd.DataFrame(results)
    df_st=df_st.sort_values("大小(MB)",ascending=False)
    st.dataframe(df_st,use_container_width=True,hide_index=True)

    st.divider()
    st.subheader("Top 20 目录（按文件聚合大小）")
    try:
        top_dirs=pd.read_sql_query("""
            SELECT SUBSTR(file_path,1,LENGTH(file_path)-LENGTH(file_name)-1) AS directory,
                   COUNT(*) AS file_count,
                   ROUND(SUM(file_size)/1048576.0,1) AS total_mb
            FROM files GROUP BY directory ORDER BY total_mb DESC LIMIT 20
        """,conn)
        top_dirs.columns=["目录","文件数","大小(MB)"]
        st.dataframe(top_dirs,use_container_width=True,hide_index=True)
    except: st.info("目录聚合查询需要数据库支持（当前文件系统扫描较慢）")

# ========== TAB 5: 备份中心 ==========
with tabs[5]:
    st.header("💾 备份中心")
    st.subheader("Git 仓库备份")
    git_repos=[("GraceOS",r"E:\创业项目\GraceOS"),("Obsidian知识库",r"E:\知识库obsidian")]
    for rname,rpath in git_repos:
        git_d=os.path.join(rpath,".git")
        status="✅ Git仓库" if os.path.exists(git_d) else "❌ 非Git仓库"
        col_g1,col_g2,col_g3=st.columns([2,1,1])
        col_g1.write(f"**{rname}**: {rpath}")
        col_g2.write(status)
        if os.path.exists(git_d):
            if col_g3.button(f"Auto Commit {rname}",key=f"gcommit_{rname}"):
                try:
                    r1=subprocess.run(["git","-C",rpath,"add","."],capture_output=True,text=True)
                    r2=subprocess.run(["git","-C",rpath,"commit","-m",f"Auto backup {date.today()}"],capture_output=True,text=True)
                    if "nothing to commit" in r2.stdout+r2.stderr:
                        st.success(f"{rname}: 无变更")
                    elif r2.returncode==0:
                        st.success(f"{rname}: commit 成功")
                        cur.execute("INSERT INTO backup_history(backup_type,target,status,details,created_at) VALUES('git',?,?,?,datetime('now','localtime'))",(rpath,"success",r2.stdout[:200]))
                        conn.commit()
                    else:
                        st.error(f"{rname}: {r2.stderr}")
                except Exception as e: st.error(str(e))
    st.divider()
    st.subheader("SQLite 数据库备份")
    if st.button("📦 备份数据库",key="bkup_sqlite"):
        try:
            import shutil
            bk_path="E:\\创业项目\\GraceOS\\09_Database\\graceos_backup_" + date.today().strftime('%Y%m%d') + ".db"
            shutil.copy2(DB_FILE,bk_path)
            cur.execute("INSERT INTO backup_history(backup_type,target,status,details,created_at) VALUES('sqlite',?,'success',?,datetime('now','localtime'))",(bk_path,f"Size: {os.path.getsize(DB_FILE)} bytes"))
            conn.commit()
            st.success(f"数据库已备份到: {bk_path}")
        except Exception as e: st.error(str(e))

    st.divider()
    st.subheader("备份历史")
    bh=pd.read_sql_query("SELECT * FROM backup_history ORDER BY id DESC LIMIT 20",conn)
    if bh.empty: st.info("暂无备份记录")
    else: st.dataframe(bh,use_container_width=True,hide_index=True)

# ========== TAB 6: 项目管理中心 ==========
with tabs[6]:
    st.header("📁 项目管理中心")
    st.info("功能开发中 - 扫描本地项目目录、检测Git状态、统计项目大小")
    if st.button("🔍 快速扫描项目",key="scan_proj"):
        project_dirs=[
            r"E:\创业项目\GraceOS",
            r"E:\知识库obsidian",
        ]
        results=[]
        for pd_path in project_dirs:
            if os.path.exists(pd_path):
                git_d=os.path.join(pd_path,".git")
                is_git=os.path.exists(git_d)
                branch=""; gs=""
                if is_git:
                    try:
                        br=subprocess.run(["git","-C",pd_path,"branch","--show-current"],capture_output=True,text=True)
                        branch=br.stdout.strip()
                        stt=subprocess.run(["git","-C",pd_path,"status","--short"],capture_output=True,text=True)
                        gs="dirty" if stt.stdout.strip() else "clean"
                    except: pass
                # Count files + size
                fc_i=0; sz=0
                for dp,_,fns in os.walk(pd_path):
                    for fn in fns:
                        try:
                            fp_i=os.path.join(dp,fn)
                            if os.path.exists(fp_i) and not ".git" in dp:
                                fc_i+=1; sz+=os.path.getsize(fp_i)
                        except: pass
                results.append({"名称":os.path.basename(pd_path),"路径":pd_path,"Git":"✅" if is_git else "❌","分支":branch,"状态":gs,"文件数":fc_i,"大小MB":round(sz/1048576,1)})
        if results:
            cur.executemany("INSERT OR REPLACE INTO project_assets(name,path,is_git,git_branch,git_status,size_mb,status,scan_time) VALUES(?,?,?,?,?,?,?,datetime('now','localtime'))",[(r["名称"],r["路径"],1 if r["Git"]=="✅" else 0,r["分支"],r["状态"],r["大小MB"],"active") for r in results])
            conn.commit()
            st.dataframe(pd.DataFrame(results),use_container_width=True,hide_index=True)

# ========== TAB 7: 知识库中心 ==========
with tabs[7]:
    st.header("🧠 知识库中心")
    obsidian_path=r"E:\知识库obsidian"
    if os.path.exists(obsidian_path):
        md_count=0; att_count=0; total_sz=0
        for dp,_,fns in os.walk(obsidian_path):
            for fn in fns:
                fp=os.path.join(dp,fn)
                if ".git" in dp or ".obsidian" in dp: continue
                try:
                    if os.path.exists(fp):
                        sz=os.path.getsize(fp); total_sz+=sz
                        if fn.endswith(".md"): md_count+=1
                        else: att_count+=1
                except: pass
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Markdown笔记",f"{md_count}篇")
        c2.metric("附件",f"{att_count}个")
        c3.metric("总大小",f"{total_sz/1048576:.1f} MB")
        c4.metric("路径",obsidian_path)
        cur.execute("INSERT OR REPLACE INTO knowledge_stats(vault_name,vault_path,note_count,attachment_count,size_mb,scan_time) VALUES(?,?,?,?,?,datetime('now','localtime'))",("知识库",obsidian_path,md_count,att_count,round(total_sz/1048576,1)))
        conn.commit()
    else:
        st.warning(f"Obsidian路径不存在: {obsidian_path}")

# ========== TAB 8: Prompt 中心 ==========
with tabs[8]:
    st.header("📝 Prompt 管理中心")
    st.info("Prompt资产管理 - 分类、搜索、版本管理")
    with st.form("add_prompt"):
        st.write("添加新 Prompt")
        p_title=st.text_input("标题")
        p_content=st.text_area("内容")
        p_cat=st.selectbox("分类",["coding","writing","analysis","automation","other"])
        p_tags=st.text_input("标签(逗号分隔)")
        if st.form_submit_button("保存"):
            if p_title and p_content:
                cur.execute("INSERT INTO prompt_assets(title,content,category,tags,created_at,updated_at) VALUES(?,?,?,?,datetime('now','localtime'),datetime('now','localtime'))",(p_title,p_content,p_cat,p_tags))
                conn.commit()
                st.success("保存成功")
                st.rerun()
    prompts=pd.read_sql_query("SELECT id,title,category,tags,usage_count,rating,last_used FROM prompt_assets ORDER BY id DESC LIMIT 50",conn)
    if not prompts.empty:
        st.dataframe(prompts,use_container_width=True,hide_index=True)
    else:
        st.info("暂无Prompt，请添加")

# ========== TAB 9: 设置中心 ==========
with tabs[9]:
    st.header("⚙️ 设置中心")
    st.subheader("扫描设置")
    st.checkbox("启用自动扫描（暂未实现）",value=False)
    st.subheader("备份设置")
    st.checkbox("Git 自动 Push（暂未实现）",value=False)
    st.subheader("通知设置")
    st.checkbox("C盘超过85%提醒（暂未实现）",value=False)
    st.checkbox("健康分低于60提醒（暂未实现）",value=False)

conn.close()
