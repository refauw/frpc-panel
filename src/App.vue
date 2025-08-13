<!-- src/App.vue -->
<template>
  <div class="layout-container">
    <Sidebar
      :server-info="{
        server: data.info.serverAddr,
        port: data.info.serverPort,
        token: data.info.token,
        status: data.status,
        startTime: '2025-08-07 09:00',
        connectionCount: 23,
        uptime: '6小时12分钟',
      }"
      :resource-info="{
        cpuUsage: 62,
        memoryUsed: '3.2 GB',
        memoryTotal: '8 GB',
        memoryPercent: 40,
        diskUsed: '55 GB',
        diskTotal: '120 GB',
        diskPercent: 46,
      }"
      @edit="showServiceModal = true"
      @start="startFrpcServer"
      @stop="stopFrpcServer"
      @restart="restartFrpcServer"
      @add-tcp="openTcpAdd"
    />
    <div class="content" v-if="true">
      <h3 style="margin-bottom: 1rem">TCP 配置项</h3>
      <div class="tcp-grid">
        <TcpCard
          v-for="(cfg, idx) in data.proxies"
          :key="idx"
          :config="cfg"
          :server-addr="data.info.serverAddr"
          @update="() => openTcpEdit(idx)"
          @delete="() => removeTcpEntry(idx)"
        />
      </div>
    </div>

    <tcp-config-form-modal
      v-model:visible="showTcpModal"
      :mode="tcpModalMode"
      :formData="editTcpData"
      @save="handleTcp"
    />

    <a-modal
      v-model:visible="showServiceModal"
      title="编辑服务信息"
      @ok="handleSaveServerInfo"
    >
      <a-form :model="data.editInfo" layout="vertical">
        <a-form-item label="服务器地址" name="serverAddr">
          <a-input v-model="data.editInfo.serverAddr" />
        </a-form-item>
        <a-form-item label="端口" name="serverPort">
          <a-input v-model="data.editInfo.serverPort" />
        </a-form-item>
        <a-form-item label="Token" name="token">
          <a-input v-model="data.editInfo.token" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import TcpCard from "./components/TcpCard.vue";
import Sidebar from "./components/Sidebar.vue";
import { Message } from "@arco-design/web-vue";
import WebSocketManager from "./utils/websocket";
import TcpConfigFormModal from "./components/TcpConfigFormModal.vue";
import { cloneDeep } from "lodash/lang.js";

const data = ref({
  status: "-",
  info: { serverAddr: "-", serverPort: "-", token: "-" },
  editInfo: { serverAddr: "", serverPort: "", token: "" },
  proxies: [
    {
      name: "df_tcp_abc",
      localIP: "127.0.0.1",
      localPort: "8080",
      remotePort: "15060",
      type: "tcp",
    },
  ],
});

const showTcpModal = ref(false);
const tcpModalMode = ref("add");
const editTcpData = ref({});

function openTcpAdd() {
  tcpModalMode.value = "add";
  editTcpData.value = {};
  showTcpModal.value = true;
}

function openTcpEdit(index) {
  tcpModalMode.value = "edit";
  editTcpData.value = { ...data.value.proxies[index], index };
  showTcpModal.value = true;
}

function removeTcpEntry(index) {
  data.value.proxies.splice(index, 1);
}

function handleTcp(newCfg) {
  if (newCfg.mode === "add") {
    data.value.proxies.push({
      name: newCfg.name,
      local: newCfg.local,
      remote: newCfg.remote,
    });
  } else if (newCfg.mode === "edit") {
    const idx = newCfg.index;
    data.value.proxies[idx] = {
      name: newCfg.name,
      local: newCfg.local,
      remote: newCfg.remote,
    };
  }
  showTcpModal.value = false;
  Message.success(newCfg.mode === "add" ? "添加成功" : "编辑成功");
}

// const token = ref(localStorage.getItem("token") || "tk123123");
const token = ref("tk123123");

const showLoginModal = ref(!token.value);
const showServiceModal = ref(false);

let socket = null;

const connectSocket = () => {
  socket = WebSocketManager.getInstance("http://localhost:5050", {
    token: token.value,
  });

  socket.send("subscribe", { channels: ["status", "info", "tcp", "logs"] });

  // 订阅后端推送
  socket.subscribe("status", (_data) => {
    data.value.status = _data.status;
    console.log("📊 服务器状态:", _data);
    Message.success("服务状态变更：" + _data.status);
  });

  socket.subscribe("info", (_data) => {
    data.value.info = _data;
    data.value.editInfo = cloneDeep(_data);
    console.log("📊 INFP 配置项:", _data);
    Message.success("服务信息内容变更：" + _data);
  });

  socket.subscribe("tcp", (_data) => {
    data.value.proxies = _data;
    console.log("📊 TCP 配置项:", _data);
    Message.success("服务信息内容变更：" + _data);
  });
};

const handleSaveServerInfo = () => {
  socket.send("control_frpc", {
    action: "save_conf",
    data: data.value.editInfo,
  });
};

const startFrpcServer = () => {
  socket.send("control_frpc", { action: "start" });
};
const stopFrpcServer = () => {
  socket.send("control_frpc", { action: "stop" });
};
const restartFrpcServer = () => {
  socket.send("control_frpc", { action: "restart" });
};

const handleLogin = () => {
  // 假设调用后端登录接口获取 token
  fetch("/api/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.token) {
        token.value = data.token;
        localStorage.setItem("token", data.token);
        showLoginModal.value = false;
        connectSocket();
      } else {
        Message.error("登录失败");
      }
    });
};

onMounted(() => {
  if (token.value) {
    connectSocket();
  }
});

onUnmounted(() => {});
</script>

<style scoped>
.layout-container {
  display: flex;
  gap: 2rem;
  padding: 2rem;
}

.content {
  flex: 1;
}

.tcp-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.25rem;
}
</style>
