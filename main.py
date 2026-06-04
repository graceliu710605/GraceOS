from scanners.software_scanner import scan as software_scan
from scanners.disk_scanner import scan as disk_scan
from scanners.file_scanner import scan as file_scan


def main():
    software_scan()
    disk_scan()
    file_scan()

    print("GraceOS运行完成")


if __name__ == "__main__":
    main()