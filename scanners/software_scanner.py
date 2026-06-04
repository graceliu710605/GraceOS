import subprocess

def scan():
    print("开始扫描软件...")

    result = subprocess.run(
        ["winget", "list"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    print(result.stdout[:1000])