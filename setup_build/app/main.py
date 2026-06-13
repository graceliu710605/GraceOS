from scanners.software_scanner import scan as software_scan
from scanners.disk_scanner import scan as disk_scan
from scanners.file_scanner import scan as file_scan

from analyzers.software_search import search
from analyzers.large_file_analyzer import analyze


def main():

    print("\n========== GraceOS ==========\n")

    # 软件扫描
    software_scan()

    print("\n===== 软件查询测试 =====")

    print("\nDocker:")
    print(search("Docker"))

    print("\nPython:")
    print(search("Python"))

    print("\nGit:")
    print(search("Git"))

    print("\n=======================")

    # 磁盘扫描
    disk_scan()

    # 文件扫描（暂时保留）
    file_scan()

    print("\n===== C盘最大文件 Top10 =====")

    for item in analyze(r"C:\\", top_n=10):
        print(f'{item["size_mb"]} MB | {item["name"]}')

    print("\n===== D盘最大文件 Top10 =====")

    try:
        for item in analyze(r"D:\\", top_n=10):
            print(f'{item["size_mb"]} MB | {item["name"]}')
    except:
        print("D盘不存在")

    print("\n===== E盘最大文件 Top10 =====")

    for item in analyze(r"E:\\", top_n=10):
        print(f'{item["size_mb"]} MB | {item["name"]}')

    print("\n=======================")

    print("\nGraceOS运行完成")


if __name__ == "__main__":
    main()