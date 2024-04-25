<template>
  <div class="fullscreen bg-white text-black text-center q-pa-md flex flex-center">
    <div>
      <div class="q-mb-xl">
        <q-icon
          :name="iconName"
          :color="iconColor"
          size="8rem"
        />
      </div>
      <div class="q-mb-xl text-center">
        <p
          v-if="message"
          class="text-h6"
        >
          {{ message }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "src/stores/auth";

export default {
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const message = ref("");
    const success = ref();

    const messages = {
      waiting: "Please wait while we confirm your identity...",
      success: "You have been successfully logged in ✅",
      failed: "Failed to confirm your identity 🚫",
    };

    const authenticate = async () => {
      const code = router.currentRoute.value.query.code;
      const state = router.currentRoute.value.query.state;
      if (!code || !state) {
        message.value = messages.failed;
        success.value = false;
        router.push("/login");
        return;
      }

      message.value = messages.waiting;
      const loginSuccessful = await authStore.login(code, state);

      if (loginSuccessful) {
        message.value = messages.success;
        success.value = true;
        router.push("/protected");
      } else {
        message.value = messages.failed;
        success.value = false;
        router.push("/login");
      }
    };

    const iconName = computed(() => (success.value === false ? "error" : "login"));
    const iconColor = computed(() => (success.value === false ? "red" : "green"));

    onMounted(authenticate);

    return { message, iconName, iconColor };
  },
};
</script>
