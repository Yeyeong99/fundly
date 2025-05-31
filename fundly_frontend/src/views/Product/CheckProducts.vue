<!-- CheckProducts.vue -->
<template>
  <div v-if="loading" class="loading">
    <i class="pi pi-spin pi-spinner" style="font-size: 2.5rem"></i>
    <h3>불러오는 중입니다...</h3>
  </div>
  <div v-else class="checkproducts-container">
    <h2 class="product-title">시중에 공개된 예금, 적금 상품을 확인해보세요.</h2>
    <div class="select-container">
      <Select
        v-model="productType"
        :options="['전체', '예금', '적금']"
        placeholder="상품 유형 필터"
        class="mb-3"
        style="min-width: 10rem"
        size="small"
      />
    </div>

    <DataTable
      :value="finalProducts"
      paginator
      :rows="5"
      table-style="min-width: 60rem"
    >
      <Column
        v-for="col of columnInfos"
        :key="col.field"
        :field="col.field"
        :header="col.header"
      >
        <template v-if="col.field === 'product_name'" #body="slotProps">
          <RouterLink
            :to="{
              name: 'productdetail',
              params: {
                id: slotProps.data.id,
                comeFrom: slotProps.data.come_from
              }
            }"
          >
            <Button :label="slotProps.data[col.field]" text />
          </RouterLink>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watchEffect, watch } from "vue";
import { DataTable } from "primevue";
import Column from "primevue/column";
import Button from "primevue/button";
import Select from "primevue/select";
import axiosInstance from "@/api/axiosInstance.js";

const totalProducts = ref([]);
const officialProducts = ref([]);
const additionalProducts = ref([]);
const productType = ref("전체");
const loading = ref(true);

onMounted(async () => {
  loading.value = true;
  const response = await axiosInstance.get(
    "http://127.0.0.1:8000/api/finance/products/"
  );
  officialProducts.value = response.data.official_products || [];
  additionalProducts.value = response.data.additional_products || [];
  totalProducts.value = officialProducts.value.concat(additionalProducts.value);
  loading.value = false;
});

const columnNames = computed(() => {
  if (totalProducts.value.length === 0) return [];
  return [
    "financial_company",
    "product_name",
    "product_type",
    "six",
    "twelve",
    "twentyfour",
    "thirtysix"
  ];
});
const headers = [
  "은행 이름",
  "상품 이름",
  "상품 유형",
  "6 개월",
  "12 개월",
  "24 개월",
  "36 개월"
];

const columnInfos = ref([]);

watchEffect(() => {
  if (columnNames.value.length > 0 && columnInfos.value.length === 0) {
    columnInfos.value = columnNames.value.map((name, idx) => ({
      field: name,
      header: headers[idx] || name
    }));
  }
});

// 필터링된 상품 데이터
const filteredProducts = computed(() => {
  if (productType.value === "전체") {
    return totalProducts.value;
  }

  const typeMapping = {
    예금: "D",
    적금: "S"
  };

  const filterType = typeMapping[productType.value];
  return totalProducts.value.filter(
    product => product.product_type === filterType
  );
});

const finalProducts = computed(() =>
  filteredProducts.value.map(product => {
    const typeMapping = { D: "예금", S: "적금" };
    const rates = { 6: "-", 12: "-", 24: "-", 36: "-" };

    for (const option of product.options) {
      if (rates.hasOwnProperty(option.save_month)) {
        rates[option.save_month] = `${option.interest_rate} %`;
      }
    }

    return {
      come_from: product.come_from,
      id: product.id,
      financial_company: product.financial_company.company_name,
      product_name: product.product_name,
      product_type: typeMapping[product.product_type] || "기타",
      six: rates[6],
      twelve: rates[12],
      twentyfour: rates[24],
      thirtysix: rates[36]
    };
  })
);
</script>

<style scoped>
.product-title {
  margin-bottom: 1rem;
}
.checkproducts-container {
  width: 100%;
}

.select-container {
  margin-bottom: 1rem;
  display: flex;
  justify-content: flex-end;
}

.loading {
  width: 100%;
  text-align: center;
}
</style>
