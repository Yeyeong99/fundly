<template>
  <Button class="btn" :class="className" :label="labelName" text fluid />
</template>

<script setup>
import Button from 'primevue/button'
defineProps({
  className: Object,
  labelName: String,
})
</script>

<style scoped>
.p-button {
  display: inline-flex;
  padding: 0.7rem 2rem 0.7rem 2rem;
  justify-content: flex-end !important;
  border-radius: 0 !important;
}

.btn:hover {
  background-color: var(--p-indigo-50) !important;
  color: var(--p-indigo-700) !important;
}

.btn.active {
  background-color: var(--p-indigo-50);
  color: var(--p-indigo-700);
}

.btn:focus {
  background-color: var(--p-indigo-50);
  color: var(--p-indigo-700);
}
</style>
