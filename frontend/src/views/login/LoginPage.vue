<template>
  <div style="text-align: center; margin: 0 20px">
    <div style="margin-top: -450px">
      <div style="font-size: 35px; font-weight: bold">登录</div>
      <div style="font-size: 14px; color: grey">在进入系统之前请先输入用户名和密码进行登录</div>
    </div>
    <div style="margin-top: 8px">
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input v-model="form.username" maxlength="20" type="text" placeholder="用户名/邮箱">
            <template #prefix>
              <el-icon>
                <User/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" maxlength="20" style="margin-top: 10px" placeholder="密码">
            <template #prefix>
              <el-icon>
                <Lock/>
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-row style="margin-top: 5px">
          <el-col :span="12" style="text-align: left">
            <el-form-item prop="remember">
              <el-checkbox v-model="form.remember" label="记住我"/>
            </el-form-item>
          </el-col>
          <el-col :span="12" style="text-align: right">
            <el-link @click="router.push('/forget')">忘记密码？</el-link>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <div style="margin-top: -30px; position: relative; z-index: 1000">
      <el-button @click="handleLogin()" style="width: 270px; z-index: 1000" type="success" plain>立即登录</el-button>
    </div>
    <el-divider>
      <span style="color: grey; font-size: 13px">没有账号</span>
    </el-divider>
    <div>
      <el-button style="width: 270px" @click="router.push('/register')" type="warning" plain>注册账号</el-button>
    </div>
    <div v-if="errorMessage" style="color: red; margin-top: 20px">{{ errorMessage }}</div>
  </div>
</template>

<script setup>
import { User, Lock } from '@element-plus/icons-vue';
import { useRoute, useRouter } from 'vue-router';
import { reactive, ref, onMounted } from "vue";
import { login } from '@/net.js';
import { ElMessage } from 'element-plus';

const formRef = ref();
const form = reactive({
  username: '',
  password: '',
  remember: false
});

const rules = {
  username: [
    { required: true, message: '请输入用户名' }
  ],
  password: [
    { required: true, message: '请输入密码' }
  ]
};

const errorMessage = ref(''); // 用于显示错误信息
const router = useRouter();

const handleLogin = async () => {
  try {
    const response = await login(form);
    if (response && response.token) {
      localStorage.setItem('token', response.token);
      router.push('/index');
    } else {
      errorMessage.value = '登录失败: 响应中没有 token';
    }
  } catch (error) {
    console.error('登录失败:', error);
    if (error.response) {
      if (error.response.status === 400) {
        errorMessage.value = error.response.data.message || '用户名或密码错误';
      } else {
        errorMessage.value = '登录失败: ' + error.response.data.message;
      }
    } else {
      errorMessage.value = '登录失败: ' + error.message;
    }
  }
};

// 每次进入 /login 页面时刷新页面
onMounted(() => {
  // 检查是否已经刷新过页面
  if (!localStorage.getItem('hasReloaded')) {
    // 设置标志变量
    localStorage.setItem('hasReloaded', 'true');
    // 刷新页面
    window.location.reload();
  } else {
    // 如果已经刷新过，清除标志变量
    localStorage.removeItem('hasReloaded');
  }
});
</script>

<style scoped>
/* 如果需要进一步自定义样式，可以在这里添加 */
</style>