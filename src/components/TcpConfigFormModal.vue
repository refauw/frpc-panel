<template>
  <a-modal
    :visible="visible"
    :title="mode === 'edit' ? '编辑 TCP 配置' : '添加 TCP 配置'"
    @ok="handleOk"
    @cancel="handleCancel"
    unmount-on-close
  >
    <a-form layout="vertical" :model="localForm">
      <a-form-item
        label="名称"
        field="name"
        :rules="[{ required: true, message: '请输入名称' }]"
      >
        <a-input v-model="localForm.name" placeholder="请输入配置名称" />
      </a-form-item>

      <a-form-item
        label="内网地址"
        field="local"
        :rules="[{ required: true, message: '请输入内网地址' }]"
      >
        <a-input v-model="localForm.local" placeholder="如 127.0.0.1:8080" />
      </a-form-item>

      <a-form-item
        label="映射地址"
        field="remote"
        :rules="[{ required: true, message: '请输入映射地址' }]"
      >
        <a-input v-model="localForm.remote" placeholder="如 example.com:6000" />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  visible: { type: Boolean, required: true },
  mode: { type: String, default: "add" }, // 'add' 或 'edit'
  formData: { type: Object, default: () => ({}) },
});

const emits = defineEmits(["update:visible", "save"]);

const localForm = reactive({
  name: "",
  local: "",
  remote: "",
});

// 当外部传入数据变化时，更新本地表单
watch(
  () => props.formData,
  (newVal) => {
    if (props.mode === "edit") {
      Object.assign(localForm, newVal);
    } else {
      Object.assign(localForm, { name: "", local: "", remote: "" });
    }
  },
  { immediate: true, deep: true }
);

function handleOk() {
  emits("save", { ...localForm, mode: props.mode });
}

function handleCancel() {
  emits("update:visible", false);
}
</script>
