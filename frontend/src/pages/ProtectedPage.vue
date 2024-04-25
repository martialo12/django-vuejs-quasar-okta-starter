<template>
  <q-page class="flex flex-center">
    <div>
      <q-card>
        <q-card-section>
          <div class="text-h6">User Info</div>
        </q-card-section>
        <q-card-section>
          <div><strong>Message:</strong> Welcome back!</div>
          <div><strong>Fullname:</strong> {{ user.user.name }}</div>
          <div><strong>Email:</strong> {{ user.user.email }}</div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { useAuthStore } from "src/stores/auth";

export default {
  setup() {
    const { user } = useAuthStore();
    return { user };
  },
};
</script>
