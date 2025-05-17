<template>
  <div class="footer">
    <div class="west west1"></div>
    <div class="west west2"></div>
    <div class="west west3"></div>
    <div class="west west4"></div>
    <!-- 引入并使用子组件 -->
    <Login />
  </div>
</template>

<script setup>
import Login from '../views/welcom/LoginPage.vue'; // 引入子组件
// 无需额外的 JavaScript 逻辑
</script>

<style scoped>
body {
  background-image: url('@/img/bac.png');
}

.footer {
  width: 760px;
  height: 240px;
  margin: 300px auto;
  /* background-color: red; */
  position: relative; /* 确保子组件可以正确定位 */
}

.west {
  float: left;
  width: 25%;
  height: 100%;
  /* background-color: #33ccff; */
  background-repeat: no-repeat;
  background-position-y: center;
}

.west1 {
  background-image: url('@/img/west_1.png');
  animation: swk 1.4s steps(8) infinite;
}

.west2 {
  background-image: url('@/img/west_2.png');
  animation: zbj 1.4s steps(8) infinite;
}

.west3 {
  background-image: url('@/img/west_3.png');
  animation: ts 1.4s steps(8) infinite;
}

.west4 {
  background-image: url('@/img/west_4.png');
  animation: shs 1.4s steps(8) infinite;
}

@keyframes swk {
  0% {
    background-position-x: 0px;
  }
  100% {
    background-position-x: -1600px;
  }
}

@keyframes zbj {
  0% {
    background-position-x: 0px;
  }
  100% {
    background-position-x: -1600px;
  }
}

@keyframes shs {
  0% {
    background-position-x: 0px;
  }
  100% {
    background-position-x: -1680px;
  }
}

@keyframes ts {
  0% {
    background-position-x: 0px;
  }
  100% {
    background-position-x: -1360px;
  }
}
</style>