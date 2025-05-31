<template>
  <div class="checkspot-container">
    <h1>현물 시세 확인</h1>
    <div class="spot-type">
      <SelectButton
        id="spot-type"
        v-model="selectedSpotType"
        :options="spotType"
        optionValue="value"
        optionLabel="name"
        fluid
      />
    </div>
    <div v-if="isGold" class="card">
      <h3>금 시세</h3>
      <div class="chart">
        <Chart
          style="width: 90rem; height: 40rem"
          v-if="goldData"
          type="line"
          :data="chartGoldData"
          :options="chartOptions"
          fluid
        />
      </div>
    </div>
    <div v-else class="card">
      <h3>은 시세</h3>
      <Chart style="width: 90rem; height: 40rem" v-if="silverData" type="line" :data="chartSilverData" :options="chartOptions" fluid />
    </div>
  </div>
</template>

<script setup>
import axiosInstance from '@/api/axiosInstance'
import { ref, onMounted, watch } from 'vue'
import Chart from 'primevue/chart'
import SelectButton from 'primevue/selectbutton'

const isGold = ref(true)

const goldData = ref(null)
const goldOpenPrices = ref([])
const goldClosePrices = ref([])
const goldHighPrices = ref([])
const goldLowPrices = ref([])
const goldVolumns = ref([])
const goldDates = ref([])
const chartGoldData = ref()

const silverData = ref(null)
const silverOpenPrices = ref([])
const silverClosePrices = ref([])
const silverHighPrices = ref([])
const silverLowPrices = ref([])
const silverVolumns = ref([])
const silverDates = ref([])
const chartSilverData = ref()

const chartOptions = ref()

const selectedSpotType = ref('금')

const spotType = ref([
  { name: '금', value: '금' },
  { name: '은', value: '은' },
])

const getSpotType = (selection) => {
  if (selection.includes('금')) return true
  if (selection.includes('은')) return false
  return true
}

watch(selectedSpotType, (newValue) => {
  isGold.value = getSpotType(newValue)
})

const setChartGoldData = () => {
  const documentStyle = getComputedStyle(document.documentElement)

  return {
    labels: goldDates,
    datasets: [
      {
        label: '시가',
        data: goldOpenPrices,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-cyan-500'),
        yAxisID: 'y',
        tension: 0.4,
        pointStyle: false,
      },
      {
        label: '종가',
        data: goldClosePrices,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-orange-500'),
        yAxisID: 'y',
        tension: 0.4,
        pointStyle: false,
      },
      {
        label: '최고가',
        data: goldHighPrices,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-red-500'),
        yAxisID: 'y',
        tension: 0.4,
        pointStyle: true,
      },
      {
        label: '최저가',
        data: goldLowPrices,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-blue-500'),
        yAxisID: 'y',
        tension: 0.4,
        pointStyle: true,
      },
      {
        label: '거래량',
        data: goldVolumns,
        fill: false,
        borderDash: [5, 5],
        borderColor: documentStyle.getPropertyValue('--p-purple-500'),
        yAxisID: 'y1',
        tension: 0.4,
        pointStyle: false,
      },
    ],
  }
}

const setChartSilverData = () => {
  const documentStyle = getComputedStyle(document.documentElement)

  return {
    labels: silverDates,
    datasets: [
      {
        label: '시가',
        data: silverOpenPrices,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-cyan-500'),
        yAxisID: 'y',
        tension: 0.4,
      },
      {
        label: '종가',
        data: silverClosePrices,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-orange-500'),
        yAxisID: 'y',
        tension: 0.4,
      },
      {
        label: '최고가',
        data: silverHighPrices,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-red-500'),
        yAxisID: 'y',
        tension: 0.4,
      },
      {
        label: '최저가',
        data: silverLowPrices,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-blue-500'),
        yAxisID: 'y',
        tension: 0.4,
      },
      {
        label: '거래량',
        data: silverVolumns,
        fill: false,
        borderColor: documentStyle.getPropertyValue('--p-purple-500'),
        yAxisID: 'y1',
        tension: 0.4,
      },
    ],
  }
}

const setChartOptions = () => {
  const documentStyle = getComputedStyle(document.documentElement)
  const textColor = documentStyle.getPropertyValue('--p-text-color')
  const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color')
  const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color')

  return {
    stacked: false,
    maintainAspectRatio: false,
    aspectRatio: 1,
    plugins: {
      legend: {
        labels: {
          color: textColor,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
        },
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
        },
        scales: {
          suggestedMin: 1500,
          suggestedMax: 3000,
        },
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          drawOnChartArea: false,
          color: surfaceBorder,
        },
      },
    },
  }
}

onMounted(async () => {
  const res = await axiosInstance.get('http://127.0.0.1:8000/api/finance/show/spot/')
  goldData.value = res.data.gold_data
  silverData.value = res.data.silver_data

  for (let i = 0; i < goldData.value.length; i++) {
    const date = goldData.value[i]['date']
    const openPrice = goldData.value[i]['open_price']
    const closePrice = goldData.value[i]['close_price']
    const highPrice = goldData.value[i]['high_price']
    const lowPrice = goldData.value[i]['low_price']
    const volume = goldData.value[i]['volume']

    goldDates.value.push(date)
    goldOpenPrices.value.push(openPrice)
    goldClosePrices.value.push(closePrice)
    goldHighPrices.value.push(highPrice)
    goldLowPrices.value.push(lowPrice)
    goldVolumns.value.push(volume)
  }

  for (let i = 0; i < res.data.silver_data.length; i++) {
    const date = res.data.silver_data[i]['date']
    const openPrice = res.data.silver_data[i]['open_price']
    const closePrice = res.data.silver_data[i]['close_price']
    const highPrice = res.data.silver_data[i]['high_price']
    const lowPrice = res.data.silver_data[i]['low_price']
    const volume = res.data.silver_data[i]['volume']

    silverDates.value.push(date)
    silverOpenPrices.value.push(openPrice)
    silverClosePrices.value.push(closePrice)
    silverHighPrices.value.push(highPrice)
    silverLowPrices.value.push(lowPrice)
    silverVolumns.value.push(volume)
  }
})

onMounted(() => {
  chartGoldData.value = setChartGoldData()
  chartSilverData.value = setChartSilverData()
  chartOptions.value = setChartOptions()
})
</script>

<style scoped>
.checkspot-container {
  width: 100%;
}

.chart {
  width: 60%;
  overflow: scroll;
}

.card {
  width: 100%;
}
</style>
