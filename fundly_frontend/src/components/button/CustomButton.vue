<template>
  <div :class="justify">
    <Button class="btn-primary" :class="classname" :label="labelName" />
  </div>
</template>

<script setup>
import Button from "primevue/button";
defineProps({
  classname: Object,
  labelName: String,
  justify: String
});
</script>

<style scoped>
.btn-primary {
  background-color: var(--p-indigo-500) !important;
  color: var(--p-primary-100) !important;
  border: none !important;
}

.btn-primary:hover {
  background-color: var(--p-indigo-50) !important;
  color: var(--p-indigo-700) !important;
}

.btn-primary.active {
  background-color: var(--p-indigo-50);
  color: var(--p-indigo-700);
}

.btn-primary:focus {
  background-color: var(--p-indigo-50);
  color: var(--p-indigo-700);
}

.center {
  display: flex;

  justify-content: center;
}
.end {
  display: flex;

  justify-content: flex-end;
}
</style>
