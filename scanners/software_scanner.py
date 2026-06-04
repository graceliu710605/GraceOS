import subprocess
import json
from pathlib import Path
from datetime import datetime


def scan():

    print("开始扫描软件...")

    result = subprocess.run(
        ["winget", "list"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    lines = result.stdout.splitlines()

    software_list = []

    for line in lines:

        if "----" in line:
            continue

        if len(line.strip()) < 10:
            continue

        software_list.append(
            {
                "raw": line.strip(),
                "scan_time": datetime.now().isoformat()
            }
        )

    output_dir = Path(
        r"E:\创业项目\GraceOS\09_Database\software_assets"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "software_inventory.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            software_list,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"发现软件 {len(software_list)} 个")

    print(f"输出文件: {output_file}")