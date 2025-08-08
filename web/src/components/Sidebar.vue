<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="sidebar-actions">
        <!-- 状态判断 -->
        <template v-if="serverInfo.status === '已停止'">
          <a-tooltip content="启动">
            <icon-play-circle @click="start" class="icon-btn start" />
          </a-tooltip>
        </template>
        <template v-else-if="serverInfo.status === '运行中'">
          <a-tooltip content="重启">
            <icon-rotate-right @click="restart" class="icon-btn restart" />
          </a-tooltip>
          <a-tooltip content="停止">
            <icon-stop @click="stop" class="icon-btn stop" />
          </a-tooltip>
        </template>
        <template v-else>
          <a-tooltip content="处理中">
            <icon-loading class="icon-btn loading" />
          </a-tooltip>
        </template>

        <!-- 编辑按钮 -->
        <a-tooltip content="编辑服务器信息">
          <icon-edit @click="onEdit" class="icon-btn edit" />
        </a-tooltip>

        <!-- 添加 TCP -->
        <a-tooltip content="添加 TCP">
          <icon-plus @click="addTcp" class="icon-btn add" />
        </a-tooltip>
      </div>
    </div>

    <!-- 基础信息 -->
    <div class="info-block">
      <div class="info-subtitle">服务信息</div>
      <div>
        服务器：<strong>{{ serverInfo.server }}</strong>
      </div>
      <div>
        端口：<strong>{{ serverInfo.port }}</strong>
      </div>
      <div>
        Token：<strong>{{ serverInfo.token }}</strong>
      </div>
      <div>
        状态：
        <a-tag :color="statusColor">{{ serverInfo.status }}</a-tag>
      </div>
    </div>

    <!-- 运行信息 -->
    <div class="info-block">
      <div class="info-subtitle">运行信息</div>
      <div>
        启动时间：<strong>{{ serverInfo.startTime }}</strong>
      </div>
      <div>
        连接数：<strong>{{ serverInfo.connectionCount }}</strong>
      </div>
      <div>
        运行时长：<strong>{{ serverInfo.uptime }}</strong>
      </div>
    </div>

    <!-- 资源监控 -->
    <div class="info-block">
      <div class="info-subtitle">资源监控</div>

      <div class="progress-label">CPU 使用率</div>
      <a-progress
        :percent="resourceInfo.cpuUsage"
        :show-text="true"
        size="small"
      />

      <div class="progress-label mt-2">内存占用</div>
      <a-progress
        :percent="resourceInfo.memoryPercent"
        :show-text="true"
        size="small"
        :text="`${resourceInfo.memoryUsed} / ${resourceInfo.memoryTotal}`"
      />

      <div class="progress-label mt-2">磁盘占用</div>
      <a-progress
        :percent="resourceInfo.diskPercent"
        :show-text="true"
        size="small"
        :text="`${resourceInfo.diskUsed} / ${resourceInfo.diskTotal}`"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import {
  IconEdit,
  IconStop,
  IconPlayCircle,
  IconRotateRight,
  IconLoading,
  IconPlus,
} from "@arco-design/web-vue/es/icon";

const props = defineProps({
  serverInfo: {
    type: Object,
    required: true,
  },
  resourceInfo: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["edit", "start", "stop", "restart", "addTcp"]);

const statusColor = computed(() => {
  switch (props.serverInfo.status) {
    case "运行中":
      return "green";
    case "已停止":
      return "gray";
    case "重启中":
      return "orange";
    default:
      return "blue";
  }
});

const onEdit = () => emit("edit");
const start = () => emit("start");
const stop = () => emit("stop");
const restart = () => emit("restart");
const addTcp = () => emit("addTcp");
</script>

<style scoped>
.sidebar {
  width: 280px;
  position: sticky;
  top: 2rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  height: fit-content;
}
.sidebar-header {
  display: flex;
  justify-content: center;
  align-items: center;
}
.sidebar-title {
  font-size: 1.1rem;
  font-weight: 600;
}
.sidebar-actions {
  display: flex;
  gap: 1rem;
}
.icon-btn {
  font-size: 18px;
  cursor: pointer;
  transition: 0.2s;
}
.icon-btn:hover {
  opacity: 0.8;
}
.icon-btn.start {
  color: #10b981;
}
.icon-btn.restart {
  color: #f59e0b;
}
.icon-btn.stop {
  color: #ef4444;
}
.icon-btn.edit {
  color: #7e22ce;
}
.icon-btn.add {
  color: #3b82f6;
}
.icon-btn.loading {
  color: #64748b;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.info-block {
  margin-top: 1.25rem;
  color: #666;
  line-height: 1.8;
}
.info-subtitle {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}
.progress-label {
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
  color: #555;
}
.mt-2 {
  margin-top: 0.5rem;
}
</style>
