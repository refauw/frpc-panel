# coding=utf-8
import os
import threading
import time
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from enum import Enum
from apscheduler.schedulers.background import BackgroundScheduler

from py.frpc_config import FrpcConfig
from py.frpc_manager import FRPCManager
from py.system_monitor import get_server_status


class Channels(str, Enum):
    STATUS = "status"
    INFO = "info"
    TCP = "tcp"
    LOGS = "logs"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, origins="*")
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    ping_interval=25,  # 发送 ping 的间隔（秒）
    ping_timeout=60  # 等待 pong 的最大时间（秒）
)

cfg = FrpcConfig()
frpc = FRPCManager()

clients = set()

# ======== 全局变量 ========
# 初始化订阅字典（每个频道一个集合存订阅者 SID）
subscriptions = {}


# subscriptions = {channel.value: set() for channel in Channels}


@socketio.on('connect')
def handle_connect():
    print(f'客户端已连接: {request.sid}')
    clients.add(request.sid)
    emit('connected', {'message': '已连接服务器'})


@socketio.on('disconnect')
def handle_disconnect():
    print(f'客户端已断开: {request.sid}')
    clients.discard(request.sid)


@socketio.on("subscribe")
def handle_subscribe(data):
    sid = getattr(request, "sid", None)
    channels = data.get("channels", [])  # 支持一次订阅多个
    if sid not in subscriptions:
        subscriptions[sid] = set()

    for channel in channels:
        subscriptions[sid].add(channel)

    if Channels.STATUS.value in channels:
        send_dispatch_message(Channels.STATUS.value, {"status": "已停止"}, sid)

    if Channels.INFO.value in channels:
        send_dispatch_message(Channels.INFO.value, cfg.to_server_info_dict(), sid)

    if Channels.TCP.value in channels:
        send_dispatch_message(Channels.TCP.value, cfg.to_tcp_dict(), sid)

    print(f"{sid} 当前订阅频道: {subscriptions[sid]}")


# 发送 订阅消息
def send_dispatch_message(channel, message, sid=None):
    """向指定频道发送订阅消息"""
    if sid is None:
        emit('dispatch', {'channel': channel, 'data': message}, broadcast=True)
        return
    for _channels in subscriptions.get(sid, []):
        if channel in _channels:
            emit('dispatch', {'channel': channel, 'data': message}, to=sid)


@socketio.on('unsubscribe')
def handle_unsubscribe(data):
    print(f'客户端取消订阅: {data}')


@socketio.on('heartbeat')
def handle_heartbeat(_):
    now = time.time()
    emit('pong', {'type': 'heartbeat', 'timestamp': now, 'server': get_server_status()})
    print("💓 心跳检测 ", now)


@socketio.on("control_frpc")
def handle_service_control(data):
    global service_status
    action = data.get("action")
    print(f"客户端控制 frpc 服务: {action}")
    if action == "start":
        start_flag = frpc.start()
        service_status = "运行中"
        send_dispatch_message(Channels.STATUS.value, {"status": service_status})
    elif action == "stop":
        start_flag = frpc.stop()
        service_status = "已停止"
        send_dispatch_message(Channels.STATUS.value, {"status": service_status})
    elif action == "restart":
        service_status = "重启中"
        send_dispatch_message(Channels.STATUS.value, {"status": service_status})
        frpc.restart()
        service_status = "运行中"
        send_dispatch_message(Channels.STATUS.value, {"status": service_status})
    elif action == "save_conf":
        server_info = data.get("data")
        cfg.set_server_info(server_info)
        send_dispatch_message(Channels.INFO.value, cfg.to_server_info_dict())
    elif action == "add_tcp":
        print(f"客户端添加 TCP 代理: {data}")
    elif action == "upd_tcp":
        print(f"客户端更新 TCP 代理: {data}")
    elif action == "rm_tcp":
        print(f"客户端控制 frpc 服务: {action}")

    else:
        return


# ===== 后台推送线程 =====
def push_server_status():
    """后台循环推送服务器状态"""
    if clients:  # 只有有客户端时才推送
        socketio.emit('status', get_server_status(), namespace='/', to=None)
        print("[定时推送] status 已发送")


if __name__ == '__main__':
    # 启动定时任务
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(push_server_status, 'interval', seconds=10)
    # scheduler.start()

    # threading.Thread(target=push_server_status, daemon=True).start()

    # 定时任务
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(push_server_status, "interval", seconds=1)
    # scheduler.start()

    socketio.run(app, host='0.0.0.0', port=5050, debug=False, allow_unsafe_werkzeug=True)
