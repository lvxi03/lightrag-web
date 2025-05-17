<template>
  <div class="footer">
    <div class="west west1"></div>
    <div class="west west2"></div>
    <div class="west west3"></div>
    <div class="west west4"></div>
  </div>
</template>

<script>
export default {
  name: "Bac1"
};
</script>

<style scoped>
.footer {
  width: 760px;
  height: 240px;
  margin: 200px auto;
}

.west {
  float: left;
  width: 25%;
  height: 100%;
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