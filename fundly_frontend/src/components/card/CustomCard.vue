<!-- RouterCard.vue -->
<template>
  <Card :class="backgroundcolor" class="hover card center">
    <template #title>
      {{ cardTitle }}
    </template>
    <template #content>
      <div
        v-for="product in productList"
        :key="product.finance_product ?? product.additional_product"
      >
        <RouterLink
          :to="{ name: pageName, params: params }"
          class="decorate"
          ><CustomTextButton :label-name="product.title"></CustomTextButton
        ></RouterLink>
      </div>
      <p class="text-end">{{ startDate }}</p>
      <ProgressBar v-if="isProgressbar" :value="value"></ProgressBar>
      <div v-if="isIcon" class="icon-container">
        <div class="icon">
          <i :class="iconClass"></i>
        </div>
      </div>
      <p v-if="isDurationMonths" class="text-end">{{ durationMonths }} 개월</p>
    </template>
  </Card>
</template>

<script setup>
import Card from "primevue/card";
import ProgressBar from "primevue/progressbar";
import CustomTextButton from "../button/CustomTextButton.vue";
import { RouterLink } from "vue-router";
defineProps({
  pageName: String,
  params: Object,
  cardTitle: String,
  startDate: String,
  isIcon: Boolean,
  iconClass: String,
  productList: Array,
  isProgressbar: Boolean,
  isDurationMonths: Boolean,
  value: Number,
  durationMonths: Number,
  backgroundcolor: String
});
</script>

<style scoped>
.decorate {
  text-decoration: none;
}

.card {
  height: 100%;
}

.text-end {
  text-align: end;
}
.pi {
  padding: 0.4rem;
  border: 0.1px solid;
  border-radius: 1rem;
}

.backgroundcolor {
  color: var(--p-primary-50);
  background-color: var(--p-indigo-300);
}
</style>
