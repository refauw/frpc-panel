import subprocess
import os
import platform


class FRPCManager:
    def __init__(self, bin_dir="./frpc", conf_file="./frpc.toml"):
        self.arch = platform.machine()
        self.frpc_bin = self._detect_binary(bin_dir)
        self.frpc_conf = conf_file
        self.frpc_process = None

    def _detect_binary(self, bin_dir):
        """根据当前架构自动选择 frpc 可执行文件"""
        arch_map = {
            "x86_64": "frpc_linux_amd64",
            "frpc_linux_arm64": "frpc_darwin_arm64",
            "aarch64": "frpc_linux_arm64",
        }
        binary_name = arch_map.get(self.arch, "frpc")
        path = os.path.join(bin_dir, binary_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"未找到对应架构的 frpc 二进制文件: {path}")
        return path

    def is_running(self):
        """检查 frpc 是否运行"""
        return self.frpc_process and self.frpc_process.poll() is None

    def start(self):
        """启动 frpc"""
        if not self.is_running():
            self.frpc_process = subprocess.Popen([self.frpc_bin, "-c", self.frpc_conf])
            return True
        return False

    def stop(self):
        """停止 frpc"""
        if self.is_running():
            self.frpc_process.terminate()
            self.frpc_process.wait()
            self.frpc_process = None
            return True
        return False

    def restart(self):
        """重启 frpc"""
        self.stop()
        return self.start()

    def read_config(self):
        """读取配置文件内容"""
        return open(self.frpc_conf).read() if os.path.exists(self.frpc_conf) else ""

    def save_config(self, content):
        """保存配置到文件"""
        with open(self.frpc_conf, "w") as f:
            f.write(content)
