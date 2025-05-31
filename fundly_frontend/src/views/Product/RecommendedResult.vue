<template>
    <h1>추천 결과 확인하기</h1>

  <div class="recommended-result-container">
    <RouterCard
      v-for="product in recommendationProductList"
      :key="product.id"
      class="card-item"
      :card-content="`${product.financial_company.company_name} ${product.options[0].max_interest_rate}%`"
      :page-name="'productdetail'"
      :params="{ id: `${product.id}`, comeFrom: `${product.come_from}` }"
      :card-title="product.product_name"
      :is-icon="true"
      :is-round="false"
      :icon-class="'pi pi-chevron-right'"
    />
  </div>
</template>

<script setup>
import RouterCard from '@/components/card/RouterCard.vue'
import { ref, onMounted } from 'vue'
import axiosInstance from '@/api/axiosInstance'

const recommendationProductList = ref('')
onMounted(async () => {
  const response = await axiosInstance.get('http://127.0.0.1:8000/api/recommendation/')
  recommendationProductList.value = response.data.products
  console.log(response.data)
})
</script>

<style scoped>
.recommended-result-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 가로 4칸 */
  grid-template-rows: repeat(4, auto); /* 세로 최대 4줄 */
  gap: 1rem;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  box-sizing: border-box;
}

.card-item {
  aspect-ratio: 1/1;
  width: 100%;
}
</style>
