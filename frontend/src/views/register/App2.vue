  <template>
    <div className="app-container">
      <div className="register-container">
        <RegisterPage/>
      </div>
      <Bac2/>
    </div>
  </template>

  <script>
  import Bac2 from '@/views/register/Bac2.vue';
  import RegisterPage from '@/views/register/RegisterPage.vue';

  export default {
    name: "App",
    components: {
      Bac2,
      RegisterPage
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
    background-image: url('@/img/img.png');
    background-size: cover;
    background-position: center;
  }

  .app-container {
    width: 100%;
    height: 100%;
    position: relative; /* 确保子元素可以绝对定位 */
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .register-container {
    width: 100%;
    max-width: 600px; /* 限制最大宽度 */
    padding: 20px;
    background: rgba(255, 255, 255, 0.8); /* 半透明背景 */
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 10; /* 确保表单在动态图上方 */
    margin-bottom: 30px; /* 与动态图的间距 */
  }
  </style>