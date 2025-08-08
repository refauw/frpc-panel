<!-- src/App.vue -->
<template>
  <div class="layout-container">
    <Sidebar
      :server-info="{
        server: '192.168.1.8',
        port: '7000',
        token: 'abc123',
        status: '运行中',
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
      @start="startService"
      @stop="stopService"
      @restart="restartService"
      @add-tcp="addEntry"
      @save-config="saveConfig"
    />
    <div class="content">
      <h3 style="margin-bottom: 1rem">TCP 配置项</h3>
      <div class="tcp-grid">
        <TcpCard
          v-for="(cfg, idx) in tcpConfigs"
          :key="idx"
          :config="cfg"
          @update="(val) => updateEntry(idx, val)"
          @delete="() => removeEntry(idx)"
        />
      </div>
    </div>

    <a-modal
      v-model:visible="showServiceModal"
      title="编辑服务信息"
      @ok="saveServiceInfo"
    >
      <a-form layout="vertical">
        <a-form-item label="服务器地址">
          <a-input v-model="server" />
        </a-form-item>
        <a-form-item label="端口">
          <a-input v-model="port" />
        </a-form-item>
        <a-form-item label="Token">
          <a-input v-model="token" />
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

const server = ref("8.134.170.8");
const port = ref("7000");
const token = ref("abcdef123456");
const status = ref("运行中");
const showServiceModal = ref(false);

const tcpConfigs = ref([
  { name: "df_tcp_abc", local: "127.0.0.1:8080", remote: "8.134.170.8:15060" },
]);

const socket = WebSocketManager.getInstance("http://0.0.0.0:5000");

const handleServerStatus = (data) => {
  console.log("服务器状态:", data);
  // 你可以更新响应式数据
};

onMounted(() => {
  socket.subscribe("server_status", handleServerStatus);
  socket.send("subscribe", { topic: "server_status" });
});

onUnmounted(() => {
  socket.unsubscribe("server_status", handleServerStatus);
});

const addEntry = () => {
  tcpConfigs.value.push({
    name: "tcp_" + Math.random().toString(36).substring(2, 7),
    local: "127.0.0.1:8080",
    remote: "8.8.8.8:10000",
  });
};

const removeEntry = (index) => tcpConfigs.value.splice(index, 1);

const editEntry = (index) => {
  const item = tcpConfigs.value[index];
  const newName = prompt("修改名称", item.name);
  if (newName !== null) tcpConfigs.value[index].name = newName;
};

const saveConfig = () => {
  console.log("保存配置:", tcpConfigs.value);
  Message.success("配置已保存");
};

const startService = () => {
  status.value = "运行中";
  Message.success("服务已启动");
};
const stopService = () => {
  status.value = "已停止";
  Message.success("服务已停止");
};
const restartService = () => {
  status.value = "重启中";
  setTimeout(() => {
    status.value = "运行中";
    Message.success("服务已重启");
  }, 1000);
};

const saveServiceInfo = () => {
  showServiceModal.value = false;
  Message.success("服务信息已保存");
};
const updateEntry = (index, newData) => {
  tcpConfigs.value[index] = { ...tcpConfigs.value[index], ...newData };
};
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
