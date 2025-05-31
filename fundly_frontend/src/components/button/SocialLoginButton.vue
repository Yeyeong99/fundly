<template>
  <div class="social-btn-container" :class="socialname" @click="$emit('click')" role="button">
    <div class="social">
      <img :src="srcPath" :alt="socialname" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  socialname: String,
  srcPath: String,
})
</script>

<style scoped>
.social-btn-container {
  background-color: var(--p-primary-50);
  padding: 0.7rem 0.7rem 0.5rem 0.7rem;
  border-radius: 100%;
  cursor: pointer;
}

.kakao {
  background-color: #fee500;
}
img {
  height: 2rem;
  width: 2rem;
}
</style>
