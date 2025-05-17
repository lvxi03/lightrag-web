import axios from 'axios';

const http = axios.create({
    baseURL: 'http://localhost:8000/api/auth/', // 后端 API 地址
    withCredentials: true, // 确保与后端 CORS_ALLOW_CREDENTIALS 匹配
});

// 检查用户是否未授权
export const unauthorized = () => {
    return !localStorage.getItem('token'); // 假设使用 localStorage 存储 token
};

// 登录方法
export const login = async (data) => {
    try {
        const response = await http.post('login/', data);
        return response.data;
    } catch (error) {
        console.error('登录请求失败详情:', error.response?.data || error.message);
        throw error;
    }
};

// 注册方法
export const register = async (data) => {
    try {
        const response = await http.post('register/', data);
        return response.data;
    } catch (error) {
        console.error('注册请求失败:', error.response?.data || error.message);
        throw error;
    }
};


export const logout = async () => {
    try {
        const response = await http.post('logout/');
        if (response.status === 200) {
            localStorage.removeItem('token');  // 清除 token
            window.location.href = '/login';  // 跳转到登录页面
        }
        return response.data;
    } catch (error) {
        console.error('登出请求失败详情:', error.response?.data || error.message);
        throw error;
    }
};

// 清除 token
export const clearToken = () => {
    localStorage.removeItem('token');
};

// 发送验证码
export const sendCode = async (email) => {
    try {
        const response = await http.get('send-code/', { params: { email } });
        return response.data;
    } catch (error) {
        console.error('发送验证码失败:', error.response?.data || error.message);
        throw error;
    }
};

// 验证验证码
export const verifyCode = async (data) => {
    try {
        const response = await http.post('verify-code/', data);
        return response.data;
    } catch (error) {
        console.error('验证验证码失败:', error.response?.data || error.message);
        throw error;
    }
};

// 重置密码
export const resetPassword = async (data) => {
    try {
        const response = await http.post('reset-password/', data);
        return response.data;
    } catch (error) {
        console.error('重置密码失败:', error.response?.data || error.message);
        throw error;
    }
};

// 登录状态拦截器
http.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token'); // 清除无效 token
            window.location.href = '/'; // 跳转到登录页
        }
        return Promise.reject(error);
    }
);

// 导出常用方法
export const get = (url, config) => http.get(url, config);
export const post = (url, data, config) => http.post(url, data, config);
export const put = (url, data, config) => http.put(url, data, config);
export const del = (url, config) => http.delete(url, config);

export default http;