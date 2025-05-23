<template>
  <div style="text-align: center; margin: 0 20px">
    <div style="margin-top: 100px">
      <div style="font-size: 25px; font-weight: bold">注册新用户</div>
      <div style="font-size: 14px; color: grey">欢迎注册我们的学习平台，请在下方填写相关信息</div>
    </div>
    <div style="margin-top: 50px">
      <el-form :model="form" :rules="rules" ref="formRef" @validate="onValidate">
        <el-form-item prop="username">
          <el-input v-model="form.username" :maxlength="8" type="text" placeholder="用户名">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" :maxlength="16" type="password" placeholder="密码">
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password_repeat">
          <el-input v-model="form.password_repeat" :maxlength="16" type="password" placeholder="重复密码">
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="form.email" type="email" placeholder="电子邮件地址">
            <template #prefix>
              <el-icon><Message /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="code">
          <el-row :gutter="10" style="width: 100%">
            <el-col :span="17">
              <el-input v-model="form.code" :maxlength="6" type="text" placeholder="请输入验证码">
                <template #prefix>
                  <el-icon><EditPen /></el-icon>
                </template>
              </el-input>
            </el-col>
            <el-col :span="5">
              <el-button type="success" @click="validateEmail" :disabled="!isEmailValid">
                获取验证码
              </el-button>
            </el-col>
          </el-row>
        </el-form-item>
      </el-form>
    </div>
    <div style="margin-top: 80px">
      <el-button style="width: 270px" type="warning" @click="register" plain>立即注册</el-button>
    </div>
    <div style="margin-top: 20px">
      <span style="font-size: 14px; line-height: 15px; color: grey">已有账号? </span>
      <el-link type="primary" style="translate: 0 -2px" @click="router.push('/login')">立即登录</el-link>
    </div>
  </div>
</template>

<script setup>
import { EditPen, Lock, Message, User } from "@element-plus/icons-vue";
import router from "@/router/index.js";
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import { get, post } from "@/net.js";

const form = reactive({
  username: '',
  password: '',
  password_repeat: '',
  email: '',
  code: '',
  role: 'user'
});

const validateUsername = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入用户名'));
  } else if (!/^[a-zA-Z0-9\u4e00-\u9fa5]+$/.test(value)) {
    callback(new Error('用户名不能包含特殊字符，只能是中文/英文'));
  } else {
    callback();
  }
};

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'));
  } else {
    callback();
  }
};

const rules = {
  username: [
    { validator: validateUsername, trigger: ['blur', 'change'] },
    { min: 2, max: 8, message: '用户名的长度必须在2-8个字符之间', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 16, message: '密码的长度必须在8-16个字符之间', trigger: ['blur', 'change'] }
  ],
  password_repeat: [
    { validator: validatePassword, trigger: ['blur', 'change'] }
  ],
  email: [
    { required: true, message: '请输入邮件地址', trigger: 'blur' },
    { type: 'email', message: '请输入合法的电子邮件地址', trigger: ['blur', 'change', 'input'] }
  ],
  code: [
    { required: true, message: '请输入获取的验证码', trigger: 'blur' }
  ]
};

const formRef = ref();
const isEmailValid = ref(false);

const onValidate = (prop, isValid) => {
  console.log(`字段 ${prop} 验证结果: ${isValid}`);
  if (prop === 'email') {
    isEmailValid.value = isValid;
  }
};

const validateEmail = () => {
  formRef.value.validateField('email', (isValid) => {
    if (!isValid) {
      ElMessage.warning('请输入合法的电子邮件地址');
      return;
    }
    get(`/send-code/?email=${form.email}&type=register`, (response) => {
      if (response.status === 'success') {
        ElMessage.success(`验证码已发送到邮箱: ${form.email}，请注意查收`);
      } else {
        ElMessage.warning(response.message || '验证码发送失败');
      }
    }, undefined, (message) => {
      ElMessage.warning(message);
    });
  });
};

const register = () => {
  formRef.value.validate((isValid) => {
    if (isValid) {
      const registerData = {
        username: form.username,
        password: form.password,
        email: form.email,
        code: form.code,
        role: form.role
      };
      console.log("发送到后端的注册数据:", registerData);

      post('/register/', registerData)
        .then(response => {
          console.log("后端返回的响应数据:", response);
          if (response.data.status === 'success') {
            ElMessage.success('注册成功，欢迎加入我们');
            formRef.value.resetFields();
            router.push("/login");
          } else {
            // 如果后端返回的状态不是 'success'，显示具体的错误信息
            ElMessage.error(response.data.message || '注册失败，请稍后再试');
          }
        })
        .catch(error => {
          console.error("注册请求失败:", error);
          if (error.response && error.response.data) {
            console.error("后端返回的错误信息:", error.response.data);
            ElMessage.error(error.response.data.message || '注册失败，请稍后再试');
          } else {
            ElMessage.error('注册失败，请稍后再试');
          }
        });
    } else {
      ElMessage.warning('请完整填写注册表单内容！');
    }
  });
};
</script>