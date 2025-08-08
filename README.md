# frpc-panel

一个基于 **Vue + Arco Design + Flask-SocketIO** 的 FRPC 管理面板，支持 TCP 配置卡片化展示、实时服务器状态监控、配置管理等功能。

## ✨ 功能特性

- **卡片化 TCP 配置管理**
  - 现代化紫色主题卡片
  - 支持动态添加、修改、删除配置项
  - 每行 4 个卡片，自适应布局

- **实时服务器状态**
  - CPU、内存、运行时间、连接数实时刷新
  - WebSocket 实时推送，无需刷新页面

- **服务端信息监控**
  - 支持 `ping` 时返回运行信息
  - 后端使用 Flask-SocketIO 推送数据

- **前后端分离**
  - 前端使用 Vue 3 + Arco Design UI
  - 后端使用 Flask + Flask-SocketIO

---

## 📦 技术栈

### 前端
- [Vue 3](https://vuejs.org/) + [Vite](https://vitejs.dev/)
- [Arco Design Vue](https://arco.design/)
- [socket.io-client](https://socket.io/)

### 后端
- [Flask](https://flask.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [Python 3.9+](https://www.python.org/)

---

## 📂 目录结构

```plaintext
frpc-panel/
├── backend/               # 后端代码 (Flask)
│   ├── app.py              # Flask 入口
│   ├── requirements.txt    # 后端依赖
│   └── ...
├── frontend/               # 前端代码 (Vue 3 + Arco Design)
│   ├── src/
│   ├── package.json
│   └── ...
└── README.md
