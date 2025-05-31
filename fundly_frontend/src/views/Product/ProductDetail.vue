<template>
  <div class="product-detail-container">
    <div class="product-container">
      <h2>
        {{ productName }}
        <Button
          :icon="likeClass"
          severity="danger"
          variant="text"
          rounded
          aria-label="Favorite"
          @click="handleIsLiked"
        />
      </h2>
      <h3>{{ companyName }}</h3>
    </div>
    <div class="delete">
      <Button
        v-if="isMenu"
        type="button"
        icon="pi pi-ellipsis-v"
        @click="toggle"
        aria-haspopup="true"
        aria-controls="overlay_menu"
        text
      />
      <Menu
        v-if="isMenu"
        ref="menu"
        id="overlay_menu"
        :model="items"
        :popup="true"
      />
    </div>
    <p class="join-way">{{ joinWay }}</p>
    <h4 class="description-title">상세 설명</h4>
    <pre class="description">{{ etcNote }}</pre>
    <div class="rate-info">
      <h4>이율</h4>
      <p v-for="option in productOptions" :key="option.save_month">
        {{ option.save_month }} 개월: {{ option.interest_rate }} % (최고
        {{ option.max_interest_rate }} %)
      </p>
    </div>
    <div class="connect-to-data">
      <div class="select-goal">
        <Select
          v-model="selectedGoal"
          :placeholder="placeholder"
          optionLabel="label"
          optionValue="value"
          :options="goalNames"
        ></Select>
      </div>
      <div class="target-amount">
        <CustomInputNumber
          v-model="targetAmount"
          :input-id="'target-amount'"
          :is-label="true"
          :label-name="targetAmountPlaceholder"
          :unit="'만 원'"
        />
        <CustomInputNumber
          v-model="monthlyPay"
          :input-id="'monthly-pay'"
          :is-label="true"
          :label-name="monthlyPayPlaceholder"
          :unit="'만 원'"
        />
      </div>
      <div class="date-picker">
        <DatePicker
          :placeholder="startDatePlaceholder"
          date-format="yy/mm/dd"
          v-model="startDate"
          showButtonBar
          style="width: 100%"
        />
        <DatePicker
          :placeholder="endDatePlaceholder"
          date-format="yy/mm/dd"
          v-model="endDate"
          style="width: 100%"
          showButtonBar
        />
      </div>
      <Message v-if="isDateError" severity="error"
        >시작 시기는 끝보다 안에 위치해야 합니다.</Message
      >
      <div class="handle-end-date">
        <Button label="- 6개월" outlined @click="decrementEndDate"></Button>
        <Button label="+ 6개월" outlined @click="incrementEndDate"></Button>
      </div>
      <div class="connected" v-if="route.path.includes('connected')">
        <div class="current-amount">
          <p>현재 저축된 금액을 수정할 수 있습니다.</p>
          <CustomInputNumber
            input-id="current-amount"
            v-model="currentAmount"
            unit="만 원"
          />
          <Message v-if="isLarger" severity="error"
            >목표 금액보다 큰 값은 안됩니다.</Message
          >
        </div>
      </div>
    </div>
    <CustomButton
      @click="connectToGoal"
      :label-name="'목표와 연결하기'"
      type="submit"
      justify="end"
    />
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { useConfirm } from "primevue/useconfirm";
import { onMounted, ref, watch, computed } from "vue";

import Select from "primevue/select";
import DatePicker from "primevue/datepicker";
import CustomButton from "@/components/button/CustomButton.vue";
import Button from "primevue/button";
import CustomInputNumber from "@/components/input/CustomInputNumber.vue";
import axiosInstance from "@/api/axiosInstance.js";
import Message from "primevue/message";
import Menu from "primevue/menu";

const confirm = useConfirm();
const router = useRouter();
const route = useRoute();

// 파라미터에서 필요한 값 가져오기
const productId = Number(route.params.id);
const goalId = Number(route.params.goalid);
const comeFrom = route.params.comeFrom;

// 상품 정보
const companyName = ref("");
const productName = ref("");
const joinWay = ref("");
const endInterestRate = ref("");
const etcNote = ref("");
const isLiked = ref(false);
const likeClass = computed(() =>
  isLiked.value ? "pi pi-heart-fill" : "pi pi-heart"
);
const productOptions = ref("");

// 입력 정보
const placeholder = ref("");
const targetAmountPlaceholder = ref("");
const monthlyPayPlaceholder = ref("");
const startDatePlaceholder = ref("");
const endDatePlaceholder = ref("");
const productInfo = ref("");
const isLarger = ref(false);

// 목표에 연결
const goals = ref([]);
const goalNames = ref([]);
const selectedGoal = ref("");
const startDate = ref("");
const endDate = ref("");
const targetAmount = ref();
const currentAmount = ref();
const monthlyPay = ref();
const isMenu = ref(false);

const getMonthDifference = (startDate, endDate) => {
  const start = new Date(startDate);
  const end = new Date(endDate);

  const yearDiff = end.getFullYear() - start.getFullYear();
  const monthDiff = end.getMonth() - start.getMonth();

  return yearDiff * 12 + monthDiff + 1; // +1은 시작월 포함
};

const handleIsLiked = async () => {
  try {
    const response = await axiosInstance.post(
      "http://127.0.0.1:8000/api/wishlist/",
      {
        product_pk: productId,
        come_from: comeFrom
      }
    );
    if (response.data.is_liked) {
      isLiked.value = true;
    } else {
      isLiked.value = false;
    }
  } catch (err) {
    console.error(err);
  }
};

// 6개월씩 감소시키는 버튼
const decrementEndDate = () => {
  // 기준 날짜: endDate가 있으면 그걸 기준으로
  const baseDate = endDate.value
    ? new Date(endDate.value)
    : new Date(startDate.value);

  if (!baseDate || isNaN(baseDate)) {
    console.error("유효한 날짜가 없습니다.");
    return;
  }

  const newDate = new Date(baseDate);
  newDate.setMonth(newDate.getMonth() - 6);

  // YYYY-MM-DD 형식으로 저장
  endDate.value = newDate.toISOString().slice(0, 10);
};

// 6개월씩 증가시키는 버튼
const incrementEndDate = () => {
  // 기준 날짜를 endDate가 있으면 그걸 기준으로, 없으면 startDate로
  const baseDate = endDate.value
    ? new Date(endDate.value)
    : new Date(startDate.value);

  if (!baseDate || isNaN(baseDate)) {
    console.error("유효한 날짜가 없습니다.");
    return;
  }

  const newDate = new Date(baseDate);
  newDate.setMonth(newDate.getMonth() + 6);

  // YYYY-MM-DD 형식으로 저장
  endDate.value = newDate.toISOString().slice(0, 10);
};
const isDateError = ref(false);

watch([startDate, endDate], ([newStart, newEnd]) => {
  if (newStart && newEnd) {
    const start = new Date(newStart);
    const end = new Date(newEnd);
    isDateError.value = start > end;
  } else {
    isDateError.value = false;
  }
});

onMounted(async () => {
  const response = await axiosInstance.get(
    `http://127.0.0.1:8000/api/finance/products/${comeFrom}/${productId}/`
  );

  // 찜 확인용
  const wishlistResponse = await axiosInstance.get(
    "http://127.0.0.1:8000/api/wishlist/"
  );

  const wishlist = wishlistResponse.data;
  const productInfoLike = { id: productId, come_from: comeFrom };

  isLiked.value = wishlist.some(item => {
    const product = item.financial_product || item.additional_product;
    return (
      product?.id === productInfoLike.id &&
      product?.come_from === productInfoLike.come_from
    );
  });

  productInfo.value = response.data.product;
  productOptions.value = response.data.options;
  const goalsResponse = await axiosInstance.get(
    "http://127.0.0.1:8000/api/goals/"
  );

  companyName.value = productInfo.value.financial_company.company_name;
  productName.value = productInfo.value.product_name;
  joinWay.value = productInfo.value.join_way;
  endInterestRate.value = productInfo.value.end_interest_rate;
  etcNote.value = productInfo.value.etc_note;
  goals.value = goalsResponse.data;

  goalNames.value = goals.value.map(goal => ({
    label: goal.goal_name,
    value: goal.id
  }));
  if (route.path.includes("connected")) {
    const connectedToGoalData = await axiosInstance.get(
      `http://127.0.0.1:8000/api/goals/${goalId}/`
    );
    const matchedGoal = goalNames.value.find(
      goal => goal.label === connectedToGoalData.data.goal_name
    );
    if (matchedGoal) {
      selectedGoal.value = matchedGoal.value; // ✔️ Select 박스에 기본 선택값 표시됨
    }

    isMenu.value = true;
  } else {
    placeholder.value = "연결할 목표를 설정해주세요.";
    if (productInfo.value.product_type === "S") {
      monthlyPayPlaceholder.value = "매월 납입할 금액";
    } else {
      monthlyPayPlaceholder.value = "납입할 금액";
    }
    targetAmountPlaceholder.value = "전체 목표 금액";
    startDatePlaceholder.value = "납입 시작 날짜";
    endDatePlaceholder.value = "납입 끝 날짜";
  }
});

const deleteGoal = async () => {
  try {
    const goalObj = goals.value.find(goal => goal.id === selectedGoal.value);

    if (!goalObj) {
      console.error("해당 목표를 찾을 수 없습니다.");
      return;
    }
    const goalId = goalObj.id;

    await axiosInstance.delete(
      `http://127.0.0.1:8000/api/custom/goals/${goalId}/come-from/${comeFrom}/product/${productId}/`
    );
    router.push(`/checkgoal/${goalId}`);
  } catch (err) {
    console.log(err);
  }
};
const showDisconnectedDelete = () => {
  confirm.require({
    message: "목표에서 해당 상품을 삭제할까요?",
    header: "목표와 연결 끊기",
    icon: "pi pi-exclamation-triangle",
    rejectProps: {
      label: "취소",
      severity: "secondary",
      outlined: true
    },
    acceptProps: {
      label: "삭제 하기"
    },
    accept() {
      deleteGoal();
    },
    reject() {}
  });
};

const confirmCheckGoal = goalId => {
  confirm.require({
    message: `목표 페이지로 이동합니다.`,
    header: "목표와 성공적으로 연결되었어요!",
    icon: "pi pi-check",
    rejectProps: {
      label: "상품 더 둘러보기",
      outlined: true
    },
    acceptProps: {
      label: "목표 확인 하기"
    },
    accept: () => {
      router.replace(`/checkgoal/${goalId}`);
    },
    reject: () => {
      router.replace("/checkproducts");
    }
  });
};
// 게시글 delete, edit 버튼
const menu = ref();
const items = ref([
  {
    items: [
      {
        label: "삭제",
        icon: "pi pi-times",
        command: showDisconnectedDelete
      }
    ]
  }
]);

const toggle = event => {
  menu.value.toggle(event);
};

watch(selectedGoal, newGoalId => {
  const selected = goals.value.find(goal => goal.id === newGoalId);
  if (!selected) return;

  // 선택된 목표의 정보로 값 채우기
  if (selected.start_date) startDate.value = selected.start_date;
  if (selected.end_date) endDate.value = selected.end_date;

  if (selected.total_target_amount) {
    targetAmount.value = selected.total_target_amount / 10000; // 원 → 만 원 단위로 변환
  }
  if (route.path.includes("connected")) {
    const currentGoal = ref("");
    currentGoal.value = selected.connected_to_goal.find(
      product => product.financial_product === productId
    );
    targetAmount.value = currentGoal.value.target_amount / 10000;
    currentAmount.value = currentGoal.value.current_amount / 10000;
    monthlyPay.value = currentGoal.value.monthly_pay / 10000;
  }
});

const connectToGoal = async () => {
  try {
    const goalObj = goals.value.find(goal => goal.id === selectedGoal.value);

    if (!goalObj) {
      console.error("해당 목표를 찾을 수 없습니다.");
      return;
    }
    const goalId = goalObj.id;
    const durationMonths = getMonthDifference(startDate.value, endDate.value);

    if (route.path.includes("connected")) {
      const payload = {
        goal: goalId,
        financial_product: productId,
        start_date: new Date(startDate.value).toISOString().slice(0, 10),
        target_amount: targetAmount.value * 10000,
        duration_months: durationMonths,
        monthly_pay: monthlyPay.value * 10000,
        current_amount: currentAmount.value * 10000
      };

      try {
        if (monthlyPay.value > targetAmount.value) {
          isLarger.value = true;
          return;
        }
        await axiosInstance.put(
          `http://127.0.0.1:8000/api/custom/goals/${goalId}/come-from/${comeFrom}/product/${productId}/`,
          payload
        );
        router.push(`/checkgoal/${goalId}/`);
      } catch (error) {
        console.log(error);
      }
    } else {
      const payload = {
        goal: goalId,
        financial_product: productId,
        start_date: new Date(startDate.value).toISOString().slice(0, 10),
        target_amount: targetAmount.value * 10000,
        duration_months: durationMonths,
        monthly_pay: monthlyPay.value * 10000
      };

      await axiosInstance.post("http://127.0.0.1:8000/api/custom/", payload);
      confirmCheckGoal(goalId);
    }
  } catch (error) {
    console.log(error);
  }
};
</script>

<style scoped>
.product-detail-container {
  width: 100%;
}

.product-container {
  display: flex;
  justify-content: space-between;
}

.join-way {
  text-align: end;
}

.select-goal {
  margin-bottom: 2rem;
}
.description {
  text-decoration: none;
  font-size: 1rem;
  font-family: noto-sans;
  white-space: pre-wrap;
  margin-bottom: 3rem;
}

.date-picker {
  width: 84%;
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.target-amount {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.rate-info {
  border-bottom: 0.1px solid var(--p-primary-300);
  margin-bottom: 3rem;
}

.connect-to-data {
  width: 80%;
  margin-bottom: 1rem;
}

.handle-end-date {
  width: 84%;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.delete {
  display: flex;
  justify-content: end;
}

h2,
h3 {
  margin: 0;
}
</style>
