"""
软件扫描器 V2 - 结构化输出
数据来源: 1. winget list  2. Windows 注册表
"""
import subprocess, json, os, sys, locale
from pathlib import Path
from datetime import datetime

def _parse_winget_line(line, col_positions, key_map=None):
    if key_map is None: key_map = {}
    result = {}
    for col_name, start, end in col_positions:
        value = line[start:end].strip() if end is not None else line[start:].strip()
        key = key_map.get(col_name, col_name.lower())
        result[key] = value
    version = result.get("version","") or result.get("版本","")
    if version.endswith("*"): version = version[:-1]
    result["version"] = version
    return result

def _detect_column_positions(header_line, dashes_line, col_names=None):
    if col_names is None:
        col_names = ["名称","ID","版本","可用","源"] if "名称" in header_line else ["Name","Id","Version","Available","Source"]
    col_starts = {}
    for name in col_names:
        idx = header_line.find(name)
        if idx >= 0: col_starts[name] = idx
    sorted_cols = sorted(col_starts.items(), key=lambda x: x[1])
    positions = []
    for i, (name, start) in enumerate(sorted_cols):
        end = sorted_cols[i+1][1] if i+1 < len(sorted_cols) else None
        positions.append((name, start, end))
    return positions

def _parse_winget_output(stdout):
    lines = stdout.splitlines()
    header_line = dashes_line = None
    is_chinese = False
    for line in lines:
        if not header_line and "Name" in line and "Id" in line and "Version" in line: header_line = line
        if not header_line and "名称" in line and ("ID" in line or "版本" in line): header_line = line; is_chinese = True
        if header_line and "----" in line: dashes_line = line; break
    if not header_line: return None
    if is_chinese:
        col_names = ["名称","ID","版本","可用","源"]
        key_map = {"名称":"name","ID":"id","Id":"id","版本":"version","可用":"available","源":"source"}
        require_id = False
    else:
        col_names = ["Name","Id","Version","Available","Source"]
        key_map = {}; require_id = True
    col_positions = _detect_column_positions(header_line, dashes_line or "", col_names)
    software_list = []; started = False
    for line in lines:
        if line == dashes_line: started = True; continue
        if not started or len(line.strip()) < 5: continue
        parsed = _parse_winget_line(line, col_positions, key_map)
        if bool(parsed.get("name")) and (not require_id or bool(parsed.get("id"))):
            software_list.append(parsed)
    print(f"[DIAG] winget parsed: {len(software_list)} rows")
    return software_list

def _query_registry():
    ps_script = r"""
$keys = @(
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*'
)
$results = @()
foreach ($key in $keys) {
    if (Test-Path (Split-Path $key -Parent)) {
        Get-ItemProperty $key -ErrorAction SilentlyContinue | ForEach-Object {
            $results += [PSCustomObject]@{
                DisplayName = $_.DisplayName
                Publisher = $_.Publisher
                InstallDate = $_.InstallDate
                EstimatedSize = $_.EstimatedSize
                InstallLocation = $_.InstallLocation
            }
        }
    }
}
$results | Where-Object { $_.DisplayName } | ConvertTo-Json -Compress
"""
    try:
        result = subprocess.run(["powershell","-NoProfile","-Command",ps_script], capture_output=True, text=True, errors="replace", timeout=60)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return [data] if isinstance(data, dict) else data
    except Exception as e: print(f"Registry query failed: {e}")
    return []

def _merge_registry_data(software_list, registry_data):
    for sw in software_list:
        sw_name = sw.get("name","").lower()
        if not sw_name: continue
        for reg in registry_data:
            display = (reg.get("DisplayName") or "").lower()
            if not display: continue
            if sw_name == display or sw_name in display or display in sw_name:
                if reg.get("Publisher"): sw["publisher"] = str(reg["Publisher"]).strip()
                if reg.get("InstallDate"): sw["install_date"] = str(reg["InstallDate"]).strip()
                if reg.get("InstallLocation"): sw["install_path"] = str(reg["InstallLocation"]).strip()
                if reg.get("EstimatedSize") and reg["EstimatedSize"] > 0:
                    sw["size_bytes"] = int(reg["EstimatedSize"]) * 1024
                break

def scan():
    print("Starting software scan...")
    raw_bytes = subprocess.run(["winget","list","--accept-source-agreements"], capture_output=True, timeout=60).stdout
    print(f"[DEBUG] encoding: sys={sys.getdefaultencoding()}, locale={locale.getpreferredencoding()}")
    raw_output = raw_bytes.decode("utf-8", errors="replace").strip()
    if "名称" not in raw_output and "Name" not in raw_output:
        raw_output = raw_bytes.decode("gbk", errors="replace").strip()
        print("[DEBUG] fallback to gbk")
    software_list = _parse_winget_output(raw_output)
    if software_list is None:
        software_list = []
        lines = raw_output.splitlines()
        header_seen = False
        for line in lines:
            if "Name" in line and "Id" in line: header_seen = True; continue
            if not header_seen: continue
            if "----" in line or len(line.strip()) < 5: continue
            software_list.append({"name": line.strip(), "raw": line.strip()})
    print("Querying registry...")
    registry_data = _query_registry()
    print(f"Registry entries: {len(registry_data)}")
    _merge_registry_data(software_list, registry_data)
    scan_time = datetime.now().isoformat()
    for sw in software_list: sw["scan_time"] = scan_time
    print(f"Found {len(software_list)} software packages")
    output_dir = Path(r"E:\创业项目\GraceOS\09_Database\software_assets")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "software_inventory.json"
    with open(output_file,"w",encoding="utf-8") as f:
        json.dump(software_list, f, ensure_ascii=False, indent=2)
    print(f"Output: {output_file}")
    return software_list

if __name__=="__main__": scan()
