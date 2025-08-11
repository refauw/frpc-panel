# coding=utf-8
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time
import os

# ===== 配置区 =====
SECRET_KEY = 'secret!'
PORT = 5000
PUSH_INTERVAL = 1  # 推送间隔秒
ALLOW_ORIGINS = "*"  # 允许跨域来源
# =================

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app, origins=ALLOW_ORIGINS)
socketio = SocketIO(app, cors_allowed_origins=ALLOW_ORIGINS)

clients = set()


@socketio.on('connect')
def handle_connect():
    print(f'客户端已连接: {request.sid}')
    clients.add(request.sid)
    emit('connected', {'message': '已连接服务器'})


@socketio.on('disconnect')
def handle_disconnect():
    print(f'客户端已断开: {request.sid}')
    clients.discard(request.sid)


@socketio.on('subscribe')
def handle_subscribe(data):
    print(f'客户端订阅: {data}')


@socketio.on('unsubscribe')
def handle_unsubscribe(data):
    print(f'客户端取消订阅: {data}')


@socketio.on('heartbeat')
def handle_heartbeat():
    print('收到客户端心跳')
    emit('pong', {'type': 'heartbeat', 'timestamp': time.time()})


# ===== 模拟数据函数 =====
def get_server_status():
    """返回模拟的服务器状态，可替换为真实采集逻辑"""
    return {
        'cpu': 35,
        'memory': '2.5 GB / 8 GB',
        'uptime': '1小时23分钟',
        'connections': 8
    }


# ===== 后台推送线程 =====
def send_server_status():
    while True:
        socketio.emit('server_status', get_server_status())
        print('[推送] server_status 已发送')
        time.sleep(PUSH_INTERVAL)


if __name__ == '__main__':
    # 避免 Flask debug 双进程重复启动任务
    # if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        # socketio.start_background_task(send_server_status)

    # 判断环境自动选择启动方式
    if os.environ.get("ENV") == "production":
        import eventlet

        eventlet.monkey_patch()
        socketio.run(app, host='0.0.0.0', port=PORT)
    else:
        socketio.run(app, host='0.0.0.0', port=PORT, allow_unsafe_werkzeug=True)
