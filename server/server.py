# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set file encoding=utf-8
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

CORS(app, origins="*")  # 👈 允许你的前端地址跨域
socketio = SocketIO(app, cors_allowed_origins="*")

clients = set()

@socketio.on('connect')
def handle_connect():
    print('客户端已连接', request.sid)
    clients.add(request.sid)
    emit('connected', {'message': '已连接服务器'})

@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开', request.sid)
    clients.discard(request.sid)

@socketio.on('subscribe')
def handle_subscribe(data):
    print(f'客户端订阅: {data}')

@socketio.on('unsubscribe')
def handle_unsubscribe(data):
    print(f'客户端取消订阅: {data}')

@socketio.on('heartbeat')
def handle_heartbeat():
    print('客户端心跳')
    emit('pong', {'type': 'heartbeat', 'timestamp': time.time()})

# 模拟服务器信息推送
def send_server_status():
    while True:
        socketio.emit('server_status', {
            'cpu': 35,
            'memory': '2.5 GB / 8 GB',
            'uptime': '1小时23分钟',
            'connections': 8
        })
        time.sleep(1)
        print('server_status emitted')

if __name__ == '__main__':
    threading.Thread(target=send_server_status, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
