from flask import Flask, render_template, request, redirect
import subprocess
import os

import platform


app = Flask(__name__)

arch = platform.machine()
FRPC_BIN = f"./frpc/darwin_arm64"
FRPC_CONF = "./frpc.toml"
FRPC_PROCESS = None


def is_running():
    global FRPC_PROCESS
    return FRPC_PROCESS and FRPC_PROCESS.poll() is None

@app.route("/", methods=["GET", "POST"])
def index():

    print("当前系统架构:", arch)

    global FRPC_PROCESS
    status = "🟢 运行中" if is_running() else "🔴 已停止"

    if request.method == "POST":
        with open(FRPC_CONF, "w") as f:
            f.write(request.form.get("config", ""))
        return redirect("/")

    config = open(FRPC_CONF).read() if os.path.exists(FRPC_CONF) else ""
    return render_template("index.html", status=status, config=config)

@app.route("/start")
def start():
    global FRPC_PROCESS
    if not is_running():
        FRPC_PROCESS = subprocess.Popen([FRPC_BIN, "-c", FRPC_CONF])
    return redirect("/")

@app.route("/stop")
def stop():
    global FRPC_PROCESS
    if is_running():
        FRPC_PROCESS.terminate()
        FRPC_PROCESS.wait()
        FRPC_PROCESS = None
    return redirect("/")

@app.route("/restart")
def restart():
    stop()
    return start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)
