import { io, Socket } from "socket.io-client";
import type { SockMessageType } from "./type"; // 你的消息类型

type Callback = (data: any) => void;

interface WebSocketOptions {
  maxReconnectAttempts?: number;
  reconnectInterval?: number;
  heartbeatInterval?: number;
  token?: string;
}

class WebSocketManager {
  private static instance: WebSocketManager | null = null;
  private socket: Socket | null = null;
  private readonly url: string;
  private subscriptions = new Map<SockMessageType, Set<Callback>>();
  private options: Required<WebSocketOptions>;
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null;

  private constructor(url: string, options: WebSocketOptions = {}) {
    this.url = url;
    this.options = {
      maxReconnectAttempts: options.maxReconnectAttempts ?? 5,
      reconnectInterval: options.reconnectInterval ?? 3000,
      heartbeatInterval: options.heartbeatInterval ?? 30000,
      token: options.token ?? "",
    };
    this.connect();
  }

  public static getInstance(
    url: string,
    options?: WebSocketOptions
  ): WebSocketManager {
    if (!WebSocketManager.instance) {
      WebSocketManager.instance = new WebSocketManager(url, options);
    }
    return WebSocketManager.instance;
  }

  /** 建立连接 */
  private connect() {
    this.socket = io(this.url, {
      reconnectionAttempts: this.options.maxReconnectAttempts,
      reconnectionDelay: this.options.reconnectInterval,
      auth: { token: this.options.token },
    });

    this.socket.on("connect", () => {
      console.log("✅ WebSocket 连接成功");
      this.startHeartbeat();
    });

    this.socket.on("disconnect", (reason) => {
      console.warn("❌ WebSocket 断开:", reason);
      this.stopHeartbeat();
    });

    this.socket.on("pong", (data) => {
      console.log("💓 心跳响应:", data);
    });

    // 收到后端推送的自定义事件
    this.socket.on("dispatch", ({ channel, data }) => {
      console.log("🔔 订阅频道消息:", channel, JSON.stringify(data))
      this.dispatchMessage({ type: channel, ...data });
    });
  }

  /** 订阅消息 */
  public subscribe(topic: SockMessageType, callback: Callback) {
    if (!this.subscriptions.has(topic)) {
      this.subscriptions.set(topic, new Set());
    }
    this.subscriptions.get(topic)!.add(callback);
  }

  /** 取消订阅 */
  public unsubscribe(topic: SockMessageType, callback: Callback) {
    this.subscriptions.get(topic)?.delete(callback);
  }

  /** 分发消息 */
  private dispatchMessage(message: any) {
    const { type, ...rest } = message;
    const callbacks = this.subscriptions.get(type);
    callbacks?.forEach((cb) => cb(rest));
  }

  /** 发送消息 */
  public send(type: SockMessageType, data: any) {
    this.socket?.emit(type, data);
  }

  /** 启动心跳 */
  private startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      this.send("heartbeat", {});
    }, this.options.heartbeatInterval);
  }

  /** 停止心跳 */
  private stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  /** 关闭连接 */
  public close() {
    this.stopHeartbeat();
    this.socket?.close();
    WebSocketManager.instance = null;
  }
}

export default WebSocketManager;
