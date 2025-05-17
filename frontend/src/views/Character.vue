<template>
  <div class="characters-list">
    <h2>主要人物</h2>
    <ul>
      <li>唐僧</li>
      <li>孙悟空</li>
      <li>猪八戒</li>
      <li>沙僧</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'CharacterList'
};
</script>

<style scoped>
.characters-list {
  width: 100%;
  overflow: auto;
}

.characters-list h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.characters-list ul {
  list-style-type: none;
  padding: 0;
}

.characters-list li {
  margin-bottom: 5px;
}
</style>