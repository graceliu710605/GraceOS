import os
import json
from datetime import datetime

OUTPUT_FILE = r"E:\知识库obsidian\02_Projects\graceos\09_Database\file_assets\file_inventory.json"

SCAN_DRIVES = [
    "C:\\",
    "D:\\",
    "E:\\"
]


def scan():

    print("开始建立文件索引...")

    files = []

    for drive in SCAN_DRIVES:

        if not os.path.exists(drive):
            continue

        print(f"扫描 {drive}")

        for root, dirs, filenames in os.walk(drive):

            for filename in filenames:

                try:

                    filepath = os.path.join(root, filename)

                    stat = os.stat(filepath)

                    files.append(
                        {
                            "file_name": filename,
                            "file_path": filepath,
                            "file_size": stat.st_size,
                            "last_modified": datetime.fromtimestamp(
                                stat.st_mtime
                            ).isoformat(),
                            "file_type": os.path.splitext(filename)[1],
                        }
                    )

                except Exception:
                    pass

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            files,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"索引完成，共 {len(files)} 个文件")
    print(f"输出文件: {OUTPUT_FILE}")