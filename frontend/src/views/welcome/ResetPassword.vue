<template>
  <div class="container">
    <h2>重置密码</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="email">邮箱:</label>
        <input
          type="email"
          id="email"
          v-model="email"
          required
          placeholder="Enter your email"
          disabled
        />
      </div>
      <div class="form-group">
        <label for="password">新密码:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          placeholder="新密码"
        />
      </div>
      <div class="form-group">
        <label for="password_repeat">确认密码:</label>
        <input
          type="password"
          id="password_repeat"
          v-model="password_repeat"
          required
          placeholder="确认密码"
        />
      </div>
      <button type="submit">提交</button>
    </form>
    <div v-if="message" class="message" :class="messageClass">{{ message }}</div>
  </div>
</template>

<script>
import axios from "axios";
import { useRoute } from "vue-router";

export default {
  data() {
    return {
      email: "",
      password: "",
      password_repeat: "",
      message: "",
      messageClass: "",
    };
  },
  methods: {
    async submitForm() {
      // 清空之前的提示信息
      this.message = "";
      this.messageClass = "";

      // 基本表单验证
      if (!this.email) {
        this.message = "邮箱不能为空。";
        this.messageClass = "error";
        return;
      }

      if (this.password !== this.password_repeat) {
        this.message = "两次输入的密码不一致。";
        this.messageClass = "error";
        return;
      }

      try {
        const response = await axios.post("http://localhost:8000/api/auth/reset-password/", {
          email: this.email,
          password: this.password,
        });

        if (response.status === 200) {
          this.message = response.data.message || "密码重置成功！";
          this.messageClass = "success";
        } else {
          this.message = "密码重置失败。";
          this.messageClass = "error";
        }
      } catch (error) {
        if (error.response) {
          this.message = error.response.data.message || "无效的邮箱或密码。";
        } else {
          this.message = "网络错误或服务器未运行。";
        }
        this.messageClass = "error";
      }
    },
  },
  mounted() {
    const route = useRoute();
    if (route.query.email) {
      this.email = route.query.email; // 自动填充邮箱地址
    } else {
      this.message = "未找到邮箱地址，请返回上一步填写邮箱。";
      this.messageClass = "error";
    }
  },
};
</script>

<style>
/* 全局样式 */
body {
  background-image: url('@/img/bac5.png'); /* 确保路径正确 */
  background-size: cover;
  background-position: center;
  overflow: hidden; /* 防止滚动条出现 */
}
</style>

<style scoped>
.container {
  max-width: 400px;
  margin: 250px auto; /* 将表单向下移动100px */
  padding: 20px 40px; /* 增加右边的间距 */
  background: rgba(255, 255, 255, 0.8); /* 设置背景透明度为 0.8 */
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}

.message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  color: white;
  text-align: center;
}

.success {
  background-color: #28a745;
}

.error {
  background-color: #dc3545;
}
</style>