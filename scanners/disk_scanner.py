import subprocess
from pathlib import Path


def scan():

    print("开始扫描磁盘...")

    result = subprocess.run(
        [
            "powershell",
            "-Command",
            "Get-PSDrive -PSProvider FileSystem | ConvertTo-Json"
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    output_dir = Path(
        r"E:\创业项目\GraceOS\09_Database\disk_assets"
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "disk_inventory.json"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result.stdout)

    print(f"磁盘信息已保存: {output_file}")