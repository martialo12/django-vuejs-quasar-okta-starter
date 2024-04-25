

<template>
  <q-layout>
    <q-page-container>
      <q-page class="login-page">
        <q-card class="login-card q-pa-md">
          <div class="logo-container">
            <q-img src="~assets/kering-logo.png" class="responsive-logo">
            </q-img>
          </div>
          <q-card-section>
            <div class="q-mt-md text-center">
              <q-btn
              label="Login with Okta"
              @click="login"
              :loading="loading"
              :disable="loading"
              color="dark"
              rounded/>
            </div>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import { api } from 'src/boot/axios';

const $q = useQuasar();
const loading = ref(false);

const login = async () => {
  loading.value = true;
  try {
    const response = await api.get('/api/users/okta/login');
    window.location.replace(response.data.url);
  } catch (error) {
    const message = error.response?.data?.detail || 'Login failed. Please try again.';
    $q.notify({ type: 'negative', position: 'top', message });
  } finally {
    loading.value = false; // End loading
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-card {
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  width: 350px;
  max-width: 90vw;
}

.responsive-logo {
  width: 100%;
  max-width: 100px;
  height: auto;
  margin: 0 auto;
}

.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 10px;
}
</style>
