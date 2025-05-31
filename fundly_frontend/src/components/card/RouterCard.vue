<!-- RouterCard.vue -->
<template>
  <RouterLink class="decorate" :to="{ name: pageName, params: params }">
    <Card :class="[backgroundcolor,{ 'flex': isFlex }]" class="hover card center lightcolor">
      <template #title>
        <div class="custom-card-title">{{ cardTitle }}</div>
      </template>
      <template #content>
        {{ cardContent }}
        <ul
          v-for="product in productList"
          :key="product.finance_product ?? product.additional_product"
        >
          <li>{{ product.title }}</li>
        </ul>
        <p >{{ startDate }}</p>
        <ProgressBar v-if="isProgressbar" :value="value"></ProgressBar>
        <div v-if="isIcon" class="icon-container">
          <div class="icon">
            <i :class="[iconClass, { 'is-round': isRound }]"></i>
          </div>
        </div>
        <p v-if="isDurationMonths" class="text-end">{{ durationMonths }} 개월</p>
      </template>
    </Card>
  </RouterLink>
</template>

<script setup>
import Card from 'primevue/card'
import ProgressBar from 'primevue/progressbar'
import { RouterLink } from 'vue-router'

defineProps({
  pageName: String,
  params: Object,
  cardTitle: String,
  cardContent: String,
  startDate: String,
  isIcon: Boolean,
  isFlex: Boolean,
  iconClass: String,
  isRound: Boolean,
  productList: Array,
  isProgressbar: Boolean,
  isDurationMonths: Boolean,
  value: Number,
  durationMonths: Number,
  backgroundcolor: String,
})
</script>

<style scoped>
.decorate {
  text-decoration: none;
}

.hover {
  transition: background-color 0.3s ease;
}

.hover:hover {
  color: var(--p-primary-900);
  background-color: var(--p-indigo-50);
}

.card {
  height: 100%;
}

.lightcolor {
  background-color: var(--p-primary-100);
}

.custom-card-title {
  font-size: 1rem;
}

.text-end {
  text-align: end;
}


.is-round {
  padding: 0.4rem;
  border: 0.1px solid;
  border-radius: 1rem;
}

.flex.card.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 100%;
}

.backgroundcolor {
  color: var(--p-primary-50);
  background-color: var(--p-indigo-300);
}

.success {
  background-color: var(--p-lime-300);
}
</style>
