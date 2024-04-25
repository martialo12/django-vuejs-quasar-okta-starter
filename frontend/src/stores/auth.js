import { ref } from "vue";
import { defineStore } from "pinia";
import { api } from "boot/axios";
import { useRouter } from 'vue-router';

// Helper functions for localStorage
function getLocalStorageItem(key, defaultValue = null) {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
}

function setLocalStorageItem(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

export const useAuthStore = defineStore("auth", () => {
    const isAuthenticated = ref(getLocalStorageItem("isAuthenticated", false));
    const user = ref(getLocalStorageItem("user", null));
    const router = useRouter(); // Using Vue Router for redirection

    const login = async (code, state) => {
        try {
            const response = await api.post("/api/users/okta/callback/",
                {code, state}
            );
            isAuthenticated.value = true;
            user.value = response.data;
            console.log("response data auth store: ", response.data);
            setLocalStorageItem("isAuthenticated", true);
            setLocalStorageItem("user", response.data);
            return true;
        } catch (error) {
            console.error(error);
            isAuthenticated.value = false;
            user.value = null;
            setLocalStorageItem("isAuthenticated", false);
            setLocalStorageItem("user", null);
            return false;
        }
    };

    const logout = async () => {
        try {
            const response = await api.get("/api/users/okta/logout");
            console.log('response: ', response);
            let message = response.data.message;

            if (message === "Logout successful") {
                isAuthenticated.value = false;
                user.value = null;
                setLocalStorageItem("isAuthenticated", false);
                setLocalStorageItem("user", null);
                 // Use Vue Router for redirection
                 router.push('/login');
            }

        } catch (error) {
            console.error(error);
        }
    };

    return { isAuthenticated, user, login, logout };
});
