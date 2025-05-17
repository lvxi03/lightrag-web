<template>
  <div class="character-carousel">
    <div
      class="carousel-container"
      @mouseenter="pauseCarousel"
      @mouseleave="startCarousel"
    >
      <div
        v-for="(character, index) in characters"
        :key="character.name"
        class="character-card"
      >
        <img :src="character.img" alt="" class="character-image" />
        <h3>{{ character.name }}</h3>
        <p>{{ character.description }}</p>
      </div>
      <!-- 复制一份卡片列表以实现无缝循环 -->
      <div
        v-for="(character, index) in characters"
        :key="`clone-${character.name}`"
        class="character-card"
      >
        <img :src="character.img" alt="" class="character-image" />
        <h3>{{ character.name }}</h3>
        <p>{{ character.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const characters = ref([
      {
        name: "孙悟空",
        description: "第一主角，书中的许多情节都围绕他展开。他机智勇敢、本领高强，具有反抗精神，追求自由，一路上保护唐僧西天取经，降妖除魔。",
        img: "/assets/孙悟空.png"
      },
      {
        name: "唐僧",
        description: "取经团队的核心人物，虽有时显得迂腐、不明事理，但意志坚定，一心向佛，是取经事业的领导者和精神支柱，历经九九八十一难，最终取得真经。",
        img: "/assets/唐僧.png"
      },
      {
        name: "沙僧",
        description: "重要配角，性格沉稳、任劳任怨，忠心耿耿地保护唐僧，承担着团队的后勤保障工作，一路上挑担牵马，默默付出。",
        img: "/assets/沙僧.png"
      },
      {
        name: "白龙马",
        description: "重要角色，原是西海龙王三太子，因犯错被贬下凡，化作白马驮载唐僧西天取经。他虽言语不多，但忠诚可靠，默默承担着重要的交通任务，是取经团队不可或缺的一员。",
        img: "/assets/白龙马.png"
      },
      {
        name: "猪八戒",
        description: "重要配角，性格憨厚又有些懒惰、贪吃贪色。他有时会偷懒耍滑，但在关键时刻也能发挥一定的作用，为取经团队增添了不少趣味。",
        img: "/assets/猪八戒.png"
      }
    ]);

    const startCarousel = () => {
      document.querySelector('.carousel-container').style.animationPlayState = 'running';
    };

    const pauseCarousel = () => {
      document.querySelector('.carousel-container').style.animationPlayState = 'paused';
    };

    return {
      characters,
      startCarousel,
      pauseCarousel
    };
  }
};
</script>

<style scoped>
.character-carousel {
  overflow-x: hidden; /* 隐藏水平滚动条 */
  position: relative;
  width: 100%; /* 确保宽度占满父容器 */
  height: 100vh; /* 确保高度占满视口 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-container {
  display: flex;
  animation: slide 40s linear infinite; /* 调整动画时间 */
  width: 200%; /* 设置为两倍宽度以容纳所有卡片 */
  transition: transform 0.5s ease; /* 平滑滚动 */
}

.character-card {
  width: 500px; /* 调整宽度 */
  height: 700px; /* 调整高度 */
  margin-right: 20px;
  padding: 20px; /* 调整内边距 */
  border: 1px solid #ccc;
  border-radius: 15px; /* 调整圆角 */
  background-color: #f9f9f9;
  text-align: center;
  cursor: default;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-shrink: 0; /* 防止卡片被压缩 */
}

.character-image {
  max-width: 100%; /* 确保图片宽度不超过卡片宽度 */
  max-height: 550px; /* 限制图片高度 */
  object-fit: contain; /* 保持图片原始宽高比例 */
  margin-bottom: 15px;
}

.character-card h3 {
  font-size: 20px; /* 调整标题字体大小 */
  margin: 15px 0;
}

.character-card p {
  font-size: 16px; /* 调整描述字体大小 */
  margin: 10px 0;
}

.character-card:hover {
  background-color: #e0f7fa;
}

@keyframes slide {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-100%); /* 调整 translateX 的值 */
  }
}
</style>