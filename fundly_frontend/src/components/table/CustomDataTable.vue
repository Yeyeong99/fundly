<!-- CustomDataTable.vue -->
<template>
  <DataTable
    v-model:filters="filters"
    :value="props.data"
    paginator
    :rows="5"
    tableStyle="width: 100%;"
    :globalFilterFields="globalFilterFields"
  >
    <template #header>
      <div class="flex">
        <IconField>
          <InputIcon>
            <i class="pi pi-search" />
          </InputIcon>
          <InputText v-model="filters['global'].value" :placeholder="props.searchPlaceholder" />
        </IconField>
      </div>
    </template>
    <Column
      v-for="column in props.columnInfos"
      :key="column.field"
      :field="column.field"
      :header="column.header"
      :filterField="column.field"
    >
      <template v-if="column.field === 'financial_company'" #body="slotProps">
        {{ slotProps.data.financial_company.company_name }}
      </template>
      <template
        v-if="column.field === 'title' || column.field === 'product_name'"
        #body="slotProps"
      >
        <RouterLink
          :to="{
            name: props.pageName,
            params: { id: slotProps.data.id, comeFrom: slotProps.data.come_from },
          }"
        >
          <Button :label="slotProps.data[column.field]" text />
        </RouterLink>
      </template>
      <template v-if="column.field === 'product_type'" #body="slotProps">
        {{ slotProps.data.product_type === 'D' ? '예금' : '적금' }}
      </template>
    </Column>
  </DataTable>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { FilterMatchMode } from '@primevue/core/api'
import { ref, onMounted } from 'vue'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Button from 'primevue/button'

const props = defineProps({
  type: String,
  data: Array, // Object에서 Array로 변경
  searchPlaceholder: String,
  columnInfos: Array,
  pageName: String,
})


const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
})
const globalFilterFields = ref([])

onMounted(() => {
  if (props.type === 'community') {
    filters.value = {
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      title: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
      user: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    }
    globalFilterFields.value = ['user', 'title']
  } else if (props.type === 'products') {
    filters.value = {
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      product_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
      financial_company: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
    }
    globalFilterFields.value = ['product_name', 'financial_company']
  }
})
</script>

<style scoped>
.flex {
  display: flex;
  justify-content: flex-end;
}
</style>
