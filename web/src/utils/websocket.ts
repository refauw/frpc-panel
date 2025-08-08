import { io, Socket } from "socket.io-client";
import type { SockMessageType } from "./type"; // 确保你定义了合适的类型

type Callback = (data: any) => void;

interface WebSocketOptions {
  maxReconnectAttempts?: number;
  reconnectInterval?: number;
  heartbeatInterval?: number;
}

class WebSocketManager {
  private static instance: WebSocketManager | null = null;
  private socket: Socket | null = null;
  private readonly url: string;
  private subscriptions: Map<SockMessageType, Set<Callback>> = new Map();
  private options: Required<WebSocketOptions>;
  private heartbeatTimer: any = null;

  private constructor(url: string, options: WebSocketOptions = {}) {
    this.url = url;
    this.options = {
      maxReconnectAttempts: options.maxReconnectAttempts || 5,
      reconnectInterval: options.reconnectInterval || 3000,
      heartbeatInterval: options.heartbeatInterval || 30000,
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

  private connect() {
    this.socket = io(this.url, {
      reconnectionAttempts: this.options.maxReconnectAttempts,
      reconnectionDelay: this.options.reconnectInterval,
    });

    this.socket.on("connect", () => {
      console.log("✅ WebSocket 连接成功");
      this.startHeartbeat();
    });

    this.socket.on("disconnect", () => {
      console.warn("❌ WebSocket 已断开");
      this.stopHeartbeat();
    });

    this.socket.on("message", (msg) => {
      try {
        const message = JSON.parse(msg);
        this.dispatchMessage(message);
      } catch (e) {
        console.error("❌ 无法解析消息", msg);
      }
    });
  }

  public subscribe(topic: SockMessageType, callback: Callback) {
    if (!this.subscriptions.has(topic)) {
      this.subscriptions.set(topic, new Set());
    }
    this.subscriptions.get(topic)!.add(callback);
  }

  public unsubscribe(topic: SockMessageType, callback: Callback) {
    this.subscriptions.get(topic)?.delete(callback);
  }

  private dispatchMessage(message: any) {
    const { type, ...rest } = message;
    const callbacks = this.subscriptions.get(type);
    callbacks?.forEach((cb) => cb(rest));
  }

  public send(type: SockMessageType, data: any) {
    this.socket?.emit("message", { type, ...data });
  }

  private startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      this.send("heartbeat", {});
    }, this.options.heartbeatInterval);
  }

  private stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  public close() {
    this.stopHeartbeat();
    this.socket?.close();
    WebSocketManager.instance = null;
  }
}

export default WebSocketManager;
