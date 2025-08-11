# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8

import psutil
import time
import platform
import os

# pip install psutil

# podman run --rm --pid=host --net=host --ipc=host --privileged my_image

def format_bytes(size):
    # 转换为 MB 或 GB 显示
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def get_cpu_info():
    print("📌 CPU 信息")
    print(f"  物理核心数: {psutil.cpu_count(logical=False)}")
    print(f"  逻辑核心数: {psutil.cpu_count(logical=True)}")
    print(f"  当前 CPU 使用率: {psutil.cpu_percent(interval=1)}%")
    print()


def get_memory_info():
    print("📌 内存信息")
    mem = psutil.virtual_memory()
    print(f"  总内存: {format_bytes(mem.total)}")
    print(f"  已用内存: {format_bytes(mem.used)}")
    print(f"  可用内存: {format_bytes(mem.available)}")
    print(f"  内存使用率: {mem.percent}%")
    print()


def get_disk_info():
    print("📌 磁盘信息")
    disk = psutil.disk_usage('/')
    print(f"  总容量: {format_bytes(disk.total)}")
    print(f"  已用: {format_bytes(disk.used)}")
    print(f"  可用: {format_bytes(disk.free)}")
    print(f"  使用率: {disk.percent}%")
    print()


def get_network_info():
    print("📌 网络信息")
    net = psutil.net_io_counters()
    print(f"  已发送: {format_bytes(net.bytes_sent)}")
    print(f"  已接收: {format_bytes(net.bytes_recv)}")
    print()


def get_system_info():
    print("📌 系统信息")
    print(f"  系统平台: {platform.system()} {platform.release()}")
    print(f"  启动时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))}")
    print()


def get_current_process_info():
    print("📌 当前进程信息")
    proc = psutil.Process(os.getpid())
    print(f"  进程 PID: {proc.pid}")
    print(f"  内存使用: {format_bytes(proc.memory_info().rss)}")
    print(f"  CPU 占用: {proc.cpu_percent(interval=1)}%")
    print()


def main():
    print("=" * 40)
    print("🎯 系统资源监控工具")
    print("=" * 40)

    get_system_info()
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_network_info()
    get_current_process_info()

    print("=" * 40)


if __name__ == '__main__':
    main()
