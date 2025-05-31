<template>
  <div class="bank-container">
    <div class="title">
      <h2>주변의 가까운 은행을 찾아보세요.</h2>
    </div>
    <div class="container">
      <section>
        <div id="map"></div>
      </section>
      <section class="address">
        <div class="select-address">
          <p>광역시 / 도</p>
          <Select
            v-model="mapStore.selectedDo"
            :options="mapStore.mapData"
            optionLabel="name"
            optionValue="name"
            placeholder="광역시 / 도를 선택해주세요."
            @change="updateSi"
            class="w-full"
            fluid
          />

          <p>시 / 군 / 구</p>
          <Select
            v-model="mapStore.selectedSi"
            :options="siList"
            placeholder="시 / 군 / 구를 선택해주세요."
            :disabled="!siList.length"
            class="w-full"
            fluid
          />

          <p>은행</p>
          <Select
            v-model="mapStore.selectedBank"
            :options="mapStore.bankData"
            placeholder="은행을 선택해주세요."
            class="w-full"
            fluid
          />
        </div>
        <div class="button-container">
          <CustomButton
            label-name="찾기"
            severity="secondary"
            type="submit"
            @click="mapStore.search"
            size="medium"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useMapStore } from "@/stores/kakaoMapStore";
import CustomButton from "@/components/button/CustomButton.vue";
import Select from "primevue/select";

const mapStore = useMapStore();

onMounted(async () => {
  await mapStore.initMap("map");
  await mapStore.getCurrentLocation()
  await mapStore.loadData();
});

const siList = computed(() => {
  const selected = mapStore.mapData.find(d => d.name === mapStore.selectedDo);
  return selected ? selected.countries : [];
});

function updateSi() {
  mapStore.selectedSi = "";
}
</script>

<style scoped>
.bank-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  width: 100%;
}

.title {
  margin: 3rem 0 1rem 0;
}

.container {
  width: 100%;
  justify-content: center;
  align-items: center;
  gap: 3rem;
}

.container > section:first-child {
  flex: 2 0 0; /* grow는 가능, shrink은 막음 */
  position: relative;
  min-width: 350px;
}

.container > section:last-child {
  flex: 1 0 0;
  min-width: 300px;
}

#map {
  height: 25rem;
  width: 100%;
}

.address {
  margin-bottom: 2rem;
}
.select-address {
  margin-bottom: 2rem;
}
.button-container {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .container > section:first-child {
    overflow: hidden;
    min-height: 300px;
  }
}
</style>
