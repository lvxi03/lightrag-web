import axios from 'axios';

// 创建 Axios 实例
const http = axios.create({
    baseURL: 'http://localhost:8000/api/auth/',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 检查用户是否未授权
export const unauthorized = () => {
    return !localStorage.getItem('token');  // 假设使用 localStorage 存储 token
};

// 登录方法
export const login = async (data) => {
    try {
        const response = await http.post('login/', data);
        if (response.data && response.data.token) {
            localStorage.setItem('token', response.data.token);  // 存储 token
        }
        return response.data;
    } catch (error) {
        console.error('登录请求失败详情:', error.response?.data || error.message);
        throw error;
    }
};

// 注册方法
export const register = async (data) => {
    console.log("发送到后端的注册数据:", data); // 打印发送的数据
    try {
        const response = await http.post('register/', data);
        return response.data;
    } catch (error) {
        if (error.response) {
            console.error('注册请求失败，状态码:', error.response.status);
            console.error('注册请求失败详情:', error.response.data);
            if (error.response.data && typeof error.response.data === 'object') {
                // 如果后端返回的是一个对象，打印每个错误字段
                if (error.response.data.errors) {
                    console.error('后端返回的错误字段:', error.response.data.errors);
                }
                throw new Error(JSON.stringify(error.response.data));
            } else {
                throw new Error(error.response.data || '未知错误');
            }
        } else {
            console.error('注册请求失败详情:', error.message);
            throw new Error(error.message);
        }
    }
};

// 登出方法
export const logout = async () => {
    try {
        const response = await http.post('logout/');
        if (response.status === 200) {
            localStorage.removeItem('token');  // 清除 token
        }
        return response.data;
    } catch (error) {
        console.error('登出请求失败详情:', error.response?.data || error.message);
        throw error;
    }
};

// 登录状态拦截器
http.interceptors.response.use(
    response => response,
    error => {
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
);

// 导出常用方法
export const get = (url, config) => http.get(url, config);
export const post = (url, data, config = {}) => http.post(url, data, config);
export const put = (url, data, config) => http.put(url, data, config);
export const del = (url, config) => http.delete(url, config);

export default http;