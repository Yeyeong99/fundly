<template>
  <div v-if="loading" class="loading">
    <i class="pi pi-spin pi-spinner" style="font-size: 2.5rem"></i>
    <h3>상품 추천 중입니다...</h3>
  </div>
  <div class="goal-container">
    <h2>{{ username }}님과 비슷한 상황과 목표를 가진 사람들은<br />어떤 상품을 선택했을까요?</h2>
    <h4>상품 정보를 확인 하기 위해 다음 항목을 입력해주세요.</h4>
    <Form>
      <div class="personal-info">
        <div class="age mb-2">
          <DatePicker
            v-model="birthDate"
            fluid=""
            placeholder="생년월일을 선택해주세요."
            date-format="yy/mm/dd"
          />
        </div>
        <div class="job mb-2">
          <Select v-model="selectedJob" :options="job" placeholder="재직 여부" fluid=""></Select>
        </div>
        <div class="finanacial-status mb-2">
          <Select
            v-model="selectedFinancialStatus"
            :options="assetRange"
            placeholder="자산 현황"
            fluid=""
          ></Select>
        </div>
        <div class="goal mb-2">
          <Select v-model="selectedGoal" :options="goal" placeholder="목표" fluid=""></Select>
        </div>
        <div class="salary mb-2">
          <Select
            v-model="selectedSalary"
            :options="moneyRange"
            placeholder="급여"
            fluid=""
          ></Select>
        </div>
      </div>
      <CustomButton
        label-name="상품 확인 하기"
        type="submit"
        justify="end"
        @click="handleRecommend"
      ></CustomButton>
    </Form>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/user";
import { Form } from "@primevue/forms";
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { DatePicker } from "primevue";
import axiosInstance from "@/api/axiosInstance";
import CustomInputNumber from "@/components/input/CustomInputNumber.vue";
import Select from "primevue/select";
import CustomButton from "@/components/button/CustomButton.vue";
import { palette } from "@primeuix/themes";

const loading = ref(false)
const router = useRouter()
const userStore = useUserStore();
onMounted(async () => {
  await userStore.fetchUser();

});

const username = computed(() => userStore.user?.username ?? '')

const birthDate = ref(null);
const assetRange = ref(['1,000만원 미만', '1,000만원 이상 3,000만원 미만', '3,000만원 이상 5,000만원 미만', '5,000만원 이상 1억 미만', '1억 이상'])
const moneyRange = ref(["100만원 미만", "100만원 이상 200만원 미만", "200만원 이상 300만원 미만", "300만원 이상 400만원 미만", "400만원 이상 500만원 미만", "500만원 이상"]);
const job = ref([
  '직장인',
  '공무원',
  '군인',
  '전문직',
  '학생',
  '취업준비생',
  '자영업자',
  '프리랜서',
  '예술가/창작자',
  '주부',
  '은퇴자',
  '무직'
]
);
const goal = ref([]);

const selectedJob = ref("");
const selectedFinancialStatus = ref("");
const selectedGoal = ref("");
const selectedSalary = ref("");

onMounted(async () => {
  const response = await axiosInstance.get(
    "http://127.0.0.1:8000/api/goals/"
  )

  for (let i = 0; i < response.data.length; i++) {
    const goalInfo = response.data[i];

    goal.value.push(goalInfo.goal_name)
  }

  const userinfo = await axiosInstance.get(
    "http://127.0.0.1:8000/api/user/profile/"
  )

  birthDate.value = userinfo.data.birth_date
  selectedJob.value = userinfo.data.work_type
  selectedSalary.value = userinfo.data.salary
  selectedFinancialStatus.value = userinfo.data.assets

})

// 생년월일 포맷 함수
function formatBirthDate(input) {
  const date = new Date(input);

  if (isNaN(date.getTime())) {
    throw new Error("유효하지 않은 생년월일입니다.");
  }

  return date.toISOString().split("T")[0];
}

const handleRecommend = async () => {

  // 필수 입력값 체크
  if (!username.value || !selectedJob.value || !selectedFinancialStatus.value || !selectedSalary.value || !selectedGoal.value) {
    alert("모든 항목을 입력해주세요.");
    return;
  }

  let birthDateString;

  try {
    birthDateString = formatBirthDate(birthDate.value)
  }
  catch (err) {
    alert(err.message)
    return
  }

  const payload = {
    username: username.value,
    birth_date: birthDateString,
    work_type: selectedJob.value,
    assets: selectedFinancialStatus.value,
    salary: selectedSalary.value,
    goal: selectedGoal.value,
  }

  const userInfo = {
    birth_date: birthDateString,
    work_type: selectedJob.value,
    assets: selectedFinancialStatus.value,
    salary: selectedSalary.value,
  }

  console.log(payload)

  try {
    loading.value = true
    await axiosInstance.post(
      "http://127.0.0.1:8000/api/recommendation/",
      payload
    )

    await axiosInstance.put(
      "http://127.0.0.1:8000/api/user/profile/",
      userInfo
    )
    loading.value = false
    alert('결과 생성 완료! 추천 상품을 확인해보세요!')

    router.replace('/recommendedresult')
  }
  catch (err) {
    loading.value = false
    console.error(err)
  }
}
</script>

<style scoped>
h2,
h4 {
  margin-bottom: 0.5rem;
}
.goal-container {
  width: 100%;
}

.mb-2 {
  margin-bottom: 1rem;
}
.personal-info {
  margin-bottom: 2rem;
}

.btn-container {
  display: flex;
  justify-content: flex-end;
}
</style>
