from scanners.software_scanner import scan as software_scan
from scanners.disk_scanner import scan as disk_scan
from scanners.file_scanner import scan as file_scan

from analyzers.software_search import search


def main():

    software_scan()

    print("\n===== 软件查询测试 =====")

    print("\nDocker:")
    print(search("Docker"))

    print("\nPython:")
    print(search("Python"))

    print("\nGit:")
    print(search("Git"))

    print("\n=======================")

    disk_scan()
    file_scan()

    print("\nGraceOS运行完成")


if __name__ == "__main__":
    main()