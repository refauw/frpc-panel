# coding=utf-8
import psutil
import time
import platform
import os

def format_bytes(size):
    """将字节数转换成人类可读的单位（B/KB/MB/GB/TB/PB）"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def detect_environment():
    """检测运行环境：容器 / Mac / Linux"""
    if os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv"):
        return "container"
    if platform.system() == "Darwin":
        return "mac"
    return "linux"

def get_cpu_info():
    """获取 CPU 信息（核心数、使用率）"""
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "cpu_percent": psutil.cpu_percent(interval=0.5)
    }

def get_memory_info():
    """获取内存信息（总量、已用、可用、占用率）"""
    mem = psutil.virtual_memory()
    return {
        "total": format_bytes(mem.total),
        "used": format_bytes(mem.used),
        "available": format_bytes(mem.available),
        "percent": mem.percent
    }

def get_disk_info():
    """获取磁盘信息（总量、已用、可用、占用率）"""
    mount_path = "/"
    if detect_environment() == "container" and os.path.exists("/app"):
        mount_path = "/app"
    disk = psutil.disk_usage(mount_path)
    return {
        "mount": mount_path,
        "total": format_bytes(disk.total),
        "used": format_bytes(disk.used),
        "free": format_bytes(disk.free),
        "percent": disk.percent
    }

def get_network_info():
    """获取网络流量（发送 / 接收字节数），只取常用接口"""
    net_io = psutil.net_io_counters(pernic=True)
    valid_ifaces = ["eth0", "en0", "lo", "lo0"]
    stats = {}
    for iface, counters in net_io.items():
        if any(iface.startswith(v) for v in valid_ifaces):
            stats[iface] = {
                "sent": format_bytes(counters.bytes_sent),
                "recv": format_bytes(counters.bytes_recv)
            }
    return stats

def get_system_info():
    """获取系统信息（平台、启动时间、运行环境）"""
    return {
        "platform": f"{platform.system()} {platform.release()}",
        "boot_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time())),
        "environment": detect_environment()
    }

def get_current_process_info():
    """获取当前进程信息（PID、占用内存、CPU 百分比）"""
    proc = psutil.Process(os.getpid())
    return {
        "pid": proc.pid,
        "memory": format_bytes(proc.memory_info().rss),
        "cpu_percent": proc.cpu_percent(interval=0.5)
    }

def get_server_status():
    """
    统一封装的服务器状态获取方法
    可直接用于 Flask-SocketIO / FastAPI WebSocket 返回
    """
    return {
        "system": get_system_info(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info(),
        "process": get_current_process_info(),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }

# 示例调用
if __name__ == '__main__':
    import json
    print(json.dumps(get_server_status(), indent=2, ensure_ascii=False))
