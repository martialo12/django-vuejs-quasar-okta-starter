<template>
  <div class="flex items-center justify-between q-pa-md">
    <div class="flex items-center">
      <q-avatar class="q-mr-md">
        <img src="https://cdn.quasar.dev/img/boy-avatar.png">
      </q-avatar>
      <div>
        <div class="text-h7">
          {{ user.user.name }}
        </div>
        <div class="text-caption text-grey-8">
          {{ user.user.email }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "src/stores/auth";
export default {
  name: 'UserProfileDrawer',
  setup() {
    const { user } = useAuthStore();
    return { user };
  }
}
</script>
