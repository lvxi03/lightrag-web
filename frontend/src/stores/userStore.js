import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { createStore } from "vuex";

export const useUserStore = defineStore('user', () => {
    const username = ref('');
    const password = ref('');
    const loginStatus = ref(false);
    const token = ref('');

    const ax = axios.create({
        baseURL: 'http://localhost:8000', // 请求后端数据的基本地址，自定义
        timeout: 2000 // 请求超时设置，单位ms
    });
    ax.defaults.withCredentials = true;

    // 登录方法
    const Login = async (userName, pass) => {
        try {
            const res = await login({ username: userName, password: pass });
            if (res.status === 'success') {
                username.value = userName;
                loginStatus.value = true;
                token.value = res.token; // 假设后端返回的令牌在 token 字段中
            } else {
                loginStatus.value = false;
                console.error('Login failed:', res.message);
                alert('Login failed: ' + res.message);
            }
        } catch (error) {
            console.error('Login Error:', error.response ? error.response.data : error.message);
            alert('Login Error: ' + (error.response ? error.response.data : error.message));
        }
    };

    export default createStore({
      state: {
        resetEmail: null,
      },
      mutations: {
        setResetEmail(state, email) {
          state.resetEmail = email;
        },
      },
    });
    // 清空用户信息
    const clearUserStore = () => {
        username.value = '';
        password.value = '';
        loginStatus.value = false;
        token.value = '';
        clearToken(); // 调用 api.js 中的 clearToken 方法清除 localStorage 中的 token
    };

    return { username, password, loginStatus, token, Login, clearUserStore };
});