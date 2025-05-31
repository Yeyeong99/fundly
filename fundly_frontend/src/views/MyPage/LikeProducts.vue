<template>
  <div class="title">
    <h2>찜한 상품을 확인할 수 있어요.</h2>
  </div>
  <div class="likeproducts-container">
    <RouterCard
      v-for="wish in wishlist"
      :key="wish.id"
      class="card-item"
      :page-name="'productdetail'"
      :params="{ id: `${wish.id}`, comeFrom: `${wish.come_from}` }"
      :card-title="wish.product_name"
      :is-icon="true"
      :is-round="false"
      :icon-class="'pi pi-heart-fill'"
    >
    </RouterCard>
    <RouterCard
      class="card-item"
      :page-name="'checkproducts'"
      :card-title="'상품 추가 하기'"
      :is-icon="true"
      :is-progressbar="false"
      :icon-class="'pi pi-plus'"
      :is-round="true"
      :is-flex="true"
      :is-duration-months="false"
      :backgroundcolor="'backgroundcolor'"
    ></RouterCard>
  </div>
</template>

<script setup>
import RouterCard from '@/components/card/RouterCard.vue'
import axiosInstance from '@/api/axiosInstance'
import { RouterLink } from 'vue-router'
import { onMounted, ref } from 'vue'

const wishlist = ref([])

onMounted(async () => {
  try {
    const response = await axiosInstance.get('http://127.0.0.1:8000/api/wishlist/')

    for (let i = 0; i < response.data.length; i++) {
      const products = response.data[i]

      if (products.financial_product) {
        wishlist.value.push(products.financial_product)
      }

      if (products.additional_product) {
        wishlist.value.push(products.additional_product)
      }
    }
  } catch (err) {
    console.log(err)
  }
})
</script>

<style scoped>
.likeproducts-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 가로 4칸 */
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
