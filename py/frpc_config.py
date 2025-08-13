import toml
import os


class FrpcConfig:
    def __init__(self, file_path="./frpc/frpc.toml"):
        self.file_path = file_path
        config_dir = os.path.dirname(file_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        if os.path.exists(file_path):
            self._load()
        else:
            self.server_info = {
                'server_addr': "",
                'server_port': '',
                'token': ""
            }
            self.proxies = []
            self.save()  # 创建默认文件

    def _load(self):
        data = toml.load(self.file_path)
        self.server_info = {
            'server_addr': data.get("serverAddr"),
            'server_port': data.get("serverPort"),
            'token': data.get("auth", {}).get("token", ''),
        }
        self.proxies = data.get("proxies", [])

    def save(self):
        data = {
            "serverAddr": self.server_info.get("server_addr", ''),
            "serverPort": self.server_info.get("server_port", '7000'),
            "auth": {"method": "token", "token": self.server_info.get("token", '')},
            "proxies": self.proxies
        }
        with open(self.file_path, "w") as f:
            toml.dump(data, f)

    # 修改 server_info 相关操作
    def set_server_info(self, server_info):
        self.server_info = {
            'server_addr': server_info.get("serverAddr", ''),
            'server_port': server_info.get("serverPort", '7000'),
            'token': server_info.get("token", ''),
        }
        self.save()

    # proxies 相关操作
    def add_proxy(self, proxy):
        self.proxies.append(proxy)

    def remove_proxy(self, name):
        self.proxies = [p for p in self.proxies if p.get("name") != name]

    def update_proxy(self, name, new_proxy):
        for i, p in enumerate(self.proxies):
            if p.get("name") == name:
                self.proxies[i] = new_proxy
                return True
        return False  # 没找到对应代理

    def get_proxy(self, name):
        for p in self.proxies:
            if p.get("name") == name:
                return p
        return None

    # 方便前端用，导出 dict
    def to_server_info_dict(self):
        return {
            "serverAddr": self.server_info.get("server_addr", ''),
            "serverPort": self.server_info.get("server_port", '7000'),
            "token": self.server_info.get("token", ''),
        }

    def to_tcp_dict(self):
        return self.proxies


# 使用示例
if __name__ == "__main__":
    cfg = FrpcConfig()
    print("原配置:", cfg.to_server_info_dict(), cfg.to_tcp_dict())

    cfg.set_server_info("1.2.3.4", 1234, "abcdefg123456")

    cfg.add_proxy({
        "name": "proxy1",
        "type": "tcp",
        "localIP": "localhost",
        "localPort": 8080,
        "remotePort": 15060
    })

    cfg.add_proxy({
        "name": "proxy2",
        "type": "tcp",
        "localIP": "localhost",
        "localPort": 8080,
        "remotePort": 15060
    })

    cfg.update_proxy("proxy1", {
        "name": "proxy1",
        "type": "tcp",
        "localIP": "127.0.0.1",
        "localPort": 8081,
        "remotePort": 15061
    })

    # cfg.remove_proxy("proxy1")

    print("修改后配置:", cfg.to_tcp_dict())

    cfg.save()
