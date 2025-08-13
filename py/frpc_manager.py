import subprocess
import os
import platform
import signal


def _detect_binary(bin_dir, file_name):
    """检测文件是否存在"""
    path = os.path.join(bin_dir, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"未找到文件: {path}")
    return path


class FRPCManager:
    def __init__(self, bin_dir="./frpc", conf_name="frpc.toml"):
        # 根据系统自动识别可执行文件名
        system = platform.system().lower()
        arch = platform.machine().lower()

        # macOS 的 platform.machine() 可能返回 arm64 / x86_64
        if system == "darwin":
            binary_name = f"darwin_{arch}"
        elif system == "linux":
            binary_name = f"linux_{arch}"
        elif system == "windows":
            binary_name = f"windows_{arch}.exe"
        else:
            raise ValueError(f"不支持的系统: {system}")

        self.frpc_bin = _detect_binary(bin_dir, binary_name)
        self.frpc_conf = _detect_binary(bin_dir, conf_name)
        self.frpc_process = None

    def is_running(self):
        """检查 frpc 是否运行"""
        return self.frpc_process and self.frpc_process.poll() is None

    def start(self):
        """启动 frpc"""
        if self.is_running():
            print("⚠ frpc 已经在运行")
            return False
        self.frpc_process = subprocess.Popen(
            [self.frpc_bin, "-c", self.frpc_conf],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"✅ frpc 已启动 (PID: {self.frpc_process.pid})")
        return True

    def stop(self):
        """停止 frpc"""
        if not self.is_running():
            print("⚠ frpc 未运行")
            return False
        self.frpc_process.terminate()
        try:
            self.frpc_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("⏳ 停止超时，强制杀进程")
            self.frpc_process.kill()
        self.frpc_process = None
        print("🛑 frpc 已停止")
        return True

    def restart(self):
        """重启 frpc"""
        print("🔄 正在重启 frpc...")
        self.stop()
        return self.start()

    def reload(self):
        """热加载配置"""
        if not self.is_running():
            print("⚠ frpc 未运行，无法 reload")
            return False
        result = subprocess.run(
            [self.frpc_bin, "reload", "-c", self.frpc_conf],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("♻ 配置已热加载")
            return True
        else:
            print("❌ 热加载失败:", result.stderr.strip())
            return False

    def status(self):
        """获取 frpc 代理状态"""
        result = subprocess.run(
            [self.frpc_bin, "status", "-c", self.frpc_conf],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()

    def version(self):
        """获取 frpc 版本"""
        result = subprocess.run(
            [self.frpc_bin, "-v"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()


if __name__ == "__main__":
    manager = FRPCManager(bin_dir="../frpc")

    # # 示例
    # print("版本:", manager.version())
    # manager.start()
    print('11',manager.status())
    # manager.reload()
    # manager.restart()
    # manager.stop()
