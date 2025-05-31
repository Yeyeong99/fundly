<template>
  <div v-if="goals && goals.length > 0" class="checkgoal-container">
    <RouterCard
      v-for="goal in goals"
      class="card-item"
      :page-name="'goaldetail'"
      :params="{ goalid: `${goal.id}` }"
      :card-title="goal.goal_name"
      :is-icon="goal.is_success"
      :icon-class="'pi pi-thumbs-up-fill'"
      :is-progressbar="true"
      :is-duration-months="true"
      :value="goal.current_achievement"
      :duration-months="goal.duration_months"
      :backgroundcolor="goal.is_success ? 'success' : ''"
    ></RouterCard>
    <RouterCard
      class="card-item"
      :page-name="'setgoal'"
      :card-title="'목표 추가하기'"
      :is-icon="true"
      :is-progressbar="false"
      :icon-class="'pi pi-plus'"
      :is-round="true"
      :is-flex="true"
      :is-duration-months="false"
      :backgroundcolor="'backgroundcolor'"
    ></RouterCard>
  </div>
  <div v-else class="checkgoal-container-none">
    <h2 class="title">
      현재 설정되어 있는 목표가 없습니다.
      <br />
      함께 목표를 설정해볼까요?
    </h2>
    <RouterLink :to="{ name: 'setgoal' }"
      ><CustomButton :label-name="'목표 설정 하기'"
    /></RouterLink>
  </div>
</template>

<script setup>
import CustomButton from "@/components/button/CustomButton.vue";
import RouterCard from "@/components/card/RouterCard.vue";
import { RouterLink } from "vue-router";
import { onMounted, ref } from "vue";
import axiosInstance from "@/api/axiosInstance";

const goals = ref(null);
onMounted(async () => {
  try {
    const response = await axiosInstance.get(
      "http://127.0.0.1:8000/api/goals/"
    );
    goals.value = response.data;

    for (const goal of goals.value) {
      const products = goal.connected_to_goal || [];
      let currentAmount = 0;

      for (const product of products) {
        currentAmount += product.current_amount || 0;
      }

      goal.current_achievement = Math.floor(
        (currentAmount / goal.total_target_amount) * 100
      );
      if (goal.current_achievement >= 100) {
        goal.is_success = true
      } else {
        goal.is_success = false
      }
    }
      
  } catch (err) {
    console.log(err);
  }
});
</script>

<style scoped>
.checkgoal-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 4개씩 한 줄에 */
  grid-template-rows: repeat(4, auto); /* 최대 4줄 */
  gap: 1rem;
  width: 100%;
  justify-items: center;
}

.checkgoal-container-none {
  text-align: center;
  width: 100%;
  gap: 1rem;
  align-items: center;
}

.title {
  margin-bottom: 3rem;
}

.card-item {
  aspect-ratio: 1/1;
  width: 100%;
}
</style>
