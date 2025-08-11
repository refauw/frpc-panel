<template>
  <div class="frp-card">
    <!-- 操作按钮 -->
    <div class="frp-actions">
      <icon-edit @click="showModal = true" class="arco-icon-hover" />
      <icon-delete @click="$emit('delete')" class="arco-icon-hover" />
    </div>

    <!-- 标题 -->
    <div class="frp-title">
      <span class="frp-type-badge">tcp</span>
      {{ config.name }}
    </div>

    <!-- 地址信息，每行一项 -->
    <div class="frp-info-line">
      <span class="frp-address-label">内网：</span>
      <span class="frp-address-value">{{ config.local }}</span>
    </div>
    <div class="frp-info-line">
      <span class="frp-address-label">映射地址：</span>
      <span class="frp-address-value">{{ config.remote }}</span>
    </div>

    <!-- 编辑 Modal -->
    <a-modal v-model:visible="showModal" title="编辑 TCP 配置" @ok="saveEdit">
      <a-form layout="vertical">
        <a-form-item label="名称">
          <a-input v-model="editData.name" />
        </a-form-item>
        <a-form-item label="内网地址">
          <a-input v-model="editData.local" />
        </a-form-item>
        <a-form-item label="映射地址">
          <a-input v-model="editData.remote" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import { IconEdit, IconDelete } from "@arco-design/web-vue/es/icon";

const props = defineProps({
  config: Object,
});
const emit = defineEmits(["update", "delete"]);

const showModal = ref(false);
const editData = reactive({
  name: "",
  local: "",
  remote: "",
});

watch(
  () => props.config,
  (val) => {
    editData.name = val.name;
    editData.local = val.local;
    editData.remote = val.remote;
  },
  { immediate: true }
);

const saveEdit = () => {
  emit("update", { ...editData });
  showModal.value = false;
};
</script>

<style scoped>
.frp-card {
  position: relative;
  border-left: 5px solid #7e22ce;
  border-radius: 0.75rem;
  background: white;
  padding: 1rem 1.25rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.frp-title {
  font-weight: 600;
  color: #7e22ce;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.frp-type-badge {
  font-size: 0.75rem;
  background-color: #f3e8ff;
  color: #7e22ce;
  padding: 0.2em 0.6em;
  border-radius: 0.3rem;
  margin-right: 0.5rem;
}

.frp-info-line {
  display: flex;
  align-items: center;
  margin-top: 0.25rem;
  font-size: 0.9rem;
}

.frp-address-label {
  color: #6c757d;
  min-width: 80px;
}

.frp-address-value {
  font-weight: 500;
  color: #7e22ce;
  word-break: break-word;
}

.frp-actions {
  position: absolute;
  top: 0.5rem;
  right: 0.75rem;
  display: flex;
  gap: 0.5rem;
}

.arco-icon-hover {
  cursor: pointer;
  color: #7e22ce;
}
</style>
