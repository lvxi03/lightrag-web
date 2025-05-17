<template>
    <canvas ref="canvas" class="canvas-particle"></canvas>
  </template>
  
  <script>
  export default {
    name: 'CanvasParticle',
    mounted() {
      this.initCanvas();
    },
    methods: {
      initCanvas() {
        const canvas = this.$refs.canvas;
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
  
        const config = {
          vx: 4,
          vy: 4,
          height: 2,
          width: 2,
          count: 100,
          color: "121, 162, 185",
          stroke: "100, 200, 180",
          dist: 6000,
          e_dist: 20000,
          max_conn: 10
        };
  
        // 在这里实现 CanvasParticle 的逻辑
        // 你可以直接复制 canvas-particle.js 的代码并稍作修改
      }
    }
  };
  </script>
  
  <style scoped>
  .canvas-particle {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }
  </style>