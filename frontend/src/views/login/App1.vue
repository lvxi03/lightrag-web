<template>
  <div className="app-container">
    <Bac1/>
    <LoginPage/>
  </div>
</template>

<script>
import Bac1 from '@/views/login/Bac1.vue';
import LoginPage from '@/views/login/LoginPage.vue';

export default {
  name: "App",
  components: {
    Bac1,
    LoginPage
  }
};
</script>

<style>
/* 全局样式 */
body {
  margin: 0; /* 移除默认的 margin */
  padding: 0; /* 移除默认的 padding */
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中 */
  align-items: center; /* 水平居中 */
  background-image: url('@/img/bac.png');
  background-size: cover;
  background-position: center;
  overflow: hidden; /* 防止滚动条出现 */
}

.app-container {
  width: 100%;
  height: 100%;
  position: relative; /* 确保子元素可以绝对定位 */
}
</style>