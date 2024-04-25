<template>
  <q-layout view="lHh lpR lFr">
    <q-header
      :class="$q.dark.isActive ? 'header_dark' : 'header_normal'"
      class="text-grey-2 q-py-md"
    >
      <q-toolbar>
        <q-btn
          dense
          flat
          round
          icon="menu"
          @click="toggleLeftDrawer"
        />
        <q-toolbar-title>
          <q-avatar>
            <img src="~assets/kering-logo.png">
          </q-avatar>
        </q-toolbar-title>
        <div>
          <q-btn
            class="q-mr-xs bg-grey-3 q-py-xs q-px-sm custom-border"
            flat @click="$q.dark.toggle()"
            color="black"
            :icon="$q.dark.isActive ? 'nights_stay' : 'wb_sunny'" />
        </div>
        <div class="q-mr-xs">
          <q-btn
            v-if="isAuthenticated"
            no-caps
            flat
            class="bg-grey-3
            custom-border"
            @click="logout"
          >
              <q-icon
                size="xs"
                style="color: rgb(250, 108, 14)"
                name="logout"
              />
            <span class="text-black q-ml-sm">Log Out</span>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      side="left"
      overlay
      bordered
    >
      <div
        :class="$q.dark.isActive ? 'drawer_dark' : 'bg-grey-1'"
        class="full-height q-px-sm drawer-content"
      >
        <q-toolbar class="q-px-md q-py-md">
          <div class="logo-container">
            <a href="/">
              <img
                src="~assets/kering-logo.png"
                class="responsive-logo"
              />
            </a>
          </div>
        </q-toolbar>
        <q-list class="q-px-md q-py-md drawer-list">
          <q-item active-class="tab-active" to="/" exact class="navigation-item" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="dashboard" color="primary"/>
            </q-item-section>

            <q-item-section> Dashboard </q-item-section>
          </q-item>

          <q-item active-class="tab-active" to="/analytics" class="navigation-item" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="insights" />
            </q-item-section>

            <q-item-section> Analytics </q-item-section>
          </q-item>

          <q-item active-class="tab-active" to="/statistics" class="navigation-item" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="analytics" />
            </q-item-section>

            <q-item-section> Statistics </q-item-section>
          </q-item>

          <q-item active-class="tab-active" to="/customer_management" class="navigation-item" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="manage_accounts" />
            </q-item-section>

            <q-item-section>
              Customer Management
            </q-item-section>
          </q-item>

          <q-item active-class="tab-active" to="/transactions" class="navigation-item" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="paid" />
            </q-item-section>

            <q-item-section> Transactions </q-item-section>
          </q-item>

          <q-item active-class="tab-active" to="/sales_invoices" class="navigation-item" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="receipt" />
            </q-item-section>

            <q-item-section> Sales Invoices </q-item-section>
          </q-item>

          <q-item active-class="tab-active" to="/my_profile" class="navigation-item" clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="person_pin" />
            </q-item-section>

            <q-item-section> My Profile </q-item-section>
          </q-item>
        </q-list>
        <!-- User Profile fixed at the bottom -->
        <q-separator />
        <div class="user-profile-drawer">
          <user-profile />
        </div>
      </div>

    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>

</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from "src/stores/auth";
import UserProfile from 'src/components/UserProfile.vue';

export default {
  components: {
    UserProfile
  },
  setup() {
    const leftDrawerOpen = ref(true);
    const { isAuthenticated, logout } = useAuthStore();
    return {
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
      isAuthenticated,
      logout,
    }
  }
}
</script>



<style scoped>
.drawer_dark {
  background: linear-gradient(145deg, #2e3d57 15%, rgb(7, 18, 34) 70%);
  color: white;
}

.header_normal {
  background: white;
}

.header_dark {
  background: linear-gradient(145deg, #2e3d57 15%, rgb(7, 18, 34) 70%);
}

.navigation-item {
  border-radius: 5px;
}

.tab-active {
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.custom-border {
  border-radius: 5px;
}

.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 10px;
}

.responsive-logo {
  width: 80%;
  max-width: 100px;
  height: auto;
  margin: 0 auto;
}

.drawer-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.drawer-list {
  overflow-y: auto;
  flex-grow: 1;
}

.user-profile-drawer {
  padding: 0px;
  background: white;
}

.drawer_dark .user-profile-drawer {
  background: #2e3d57;
}
</style>
