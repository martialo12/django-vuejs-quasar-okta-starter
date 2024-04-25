<template>
  <q-page class="flex flex-center">
    <div class="text-center">
      <q-icon
        name="cloud"
        size="8em"
      />
      <p class="text-h1">
        Welcome to Starter kit
      </p>
      <p
        v-if="apiStatus"
        class="text-h5"
      >
        API Status: {{ apiStatus }}
      </p>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "boot/axios";

const apiStatus = ref();

const fetchApiStatus =  async () => {
  try {
    await api.get("/api/healthz");
    apiStatus.value = "✅";
  } catch(error) {
    apiStatus.value = "🚫";
  }
};

onMounted(() => {
  fetchApiStatus();
});
</script>
