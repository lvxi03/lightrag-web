<template>
  <div id="app">
    <header>
      <nav>
        <router-link class="nav-items" to="/main" active-class="active">欢迎使用！</router-link>
        <!-- 新增智慧问答按钮 -->
        <router-link class="nav-items" to="/knowledge" active-class="active">智慧问答</router-link>
        <router-link class="nav-items" to="/graph" active-class="active">知识图谱</router-link>
        <el-button class="nav-items" @click="userLogout" active-class="active">退出登录</el-button>
      </nav>
    </header>

    <div class="content">
      <img src="@/img/xi.png" alt="background" class="back-3">

      <div class="title">
        <h3>Journal To The Western</h3>
        <h1>西游记</h1>
      </div>

      <img src="@/img/xi2.png" alt="background" class="back-2">
      <img src="@/img/xi2.png" alt="background" class="back-1">

      <div class="info-wrap">
        <p>
          《西游记》讲述了唐僧（玄奘）受观音菩萨之命，前往西天（印度）取回真经的故事。唐僧在取经的途中，先后收服了三个徒弟：孙悟空、猪八戒和沙僧。这四个师徒在取经的道路上，历经九九八十一难，最终取得真经，修成正果。
        </p>
      </div>

      <div class="cta">
        <button @click="goToMain">
          Explore More
          <i class="fa-solid fa-arrow-right"></i>
        </button>
      </div>

      <div class="slider">
        <i class="fa-solid fa-chevron-left"></i>
        <i class="fa-solid fa-chevron-right"></i>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { logout } from '@/api'; // 确保正确导入了 logout 方法
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus'; // 确保正确导入了 ElMessage

export default {
  name: 'App',
  methods: {
    userLogout: async () => {
      try {
        // 调用后端登出接口
        await logout();
        // 登出成功后，清除本地存储的 token
        localStorage.removeItem('token');
        // 提示用户退出成功
        ElMessage.success('退出登录成功，欢迎您再次使用');
        // 跳转到登录页面
        router.push("/");
      } catch (error) {
        // 登出失败，提示用户
        ElMessage.warning('退出登录失败，请稍后再试');
        console.error('退出登录失败:', error);
      }
  },
     goToMain() {
      // 跳转到 /main 页面
      this.$router.push("/main");
    }
  },
  mounted() {
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
  }
};
</script>
<style>
/* 引入 Font Awesome 和自定义样式 */
@import url('@/img/all.min.css');
@import url('@/views/styles.css');

* {
  padding: 0;
  margin: 0;
  border: none;
  outline: none;
  font-family: "Inter", sans-serif;
}

body {
  background-image: url('@/img/xi.png');
  background-size: cover;
  background-position: top;
  background-repeat: no-repeat;
  overflow: hidden;
}

body::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  background: linear-gradient(transparent 50%, rgb(0, 0, 0));
}

.content img {
  position: absolute;
  bottom: -12%;
}

header {
  position: absolute;
  top: 0;
  z-index: 1;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

nav {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 5%;
  background-color: rgba(255, 255, 255, 0.2);
  height: 30px;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  backdrop-filter: blur(5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

nav a {
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 2px;
  /* // 去掉下划线 */
  text-decoration: none;
  /* // 设置彩虹渐变 */
  background-image: linear-gradient(to right, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8f00ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  width: 110px;
  text-align: center;
  padding: 15px 0;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.active {
  background-color: #16423c;
  /* // 激活状态保持彩虹色 */
  color: transparent;
  background-image: linear-gradient(to right, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #8f00ff);
  -webkit-background-clip: text;
  background-clip: text;
}

nav a:hover {
  background-color: #16423c;
  color: white;
}

nav:hover > a:not(:hover) {
  background-color: transparent;
  color: rgb(53, 53, 53);
}

.title {
  position: absolute;
  top: 40%;
  right: 50%;
  transform: translate(50%, -50%);
}

.title h3 {
  font-size: 2rem;
  font-weight: 400;
  letter-spacing: 15px;
  color: black;
  text-align: center;
}

.title h1 {
  font-size: 10rem;
  font-weight: 800;
  letter-spacing: 50px;
  text-transform: uppercase;
  color: white;
  text-align: center;
  margin: -20px 0;
}

p {
  font-size: 14px;
  font-weight: 300;
  letter-spacing: 1px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.7);
  width: 70%;
  text-align: center;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
}

.info-wrap {
  width: 100%;
  display: flex;
  justify-content: center;
  position: absolute;
  bottom: 18%;
  z-index: 1;
}

.cta {
  position: absolute;
  bottom: 8%;
  display: flex;
  justify-content: center;
  width: 100%;
  z-index: 1;
}

.cta button {
  font-size: 18px;
  font-weight: 400;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.8);
  background-color: transparent;
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 50px;
  height: 50px;
  width: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  cursor: pointer;
}

.cta button:hover {
  background-color: rgba(255, 255, 255, 0.8);
  color: rgb(53, 53, 53);
}

.slider {
  position: absolute;
  top: 50%;
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.slider i {
  padding: 0 5%;
  font-size: 36px;
  color: rgba(255, 255, 255, 0.4);
}
</style>