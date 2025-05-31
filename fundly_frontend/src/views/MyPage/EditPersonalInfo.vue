<template>
  <div class="editpersonalinfo-container">
    <div class="title">
      <h1>
      개인 정보 수정
      </h1>
      <Button
        icon="pi pi-sign-out"
        label="탈퇴"
        iconPos="top"
        severity="danger"
        rounded
        variant="text"
        @click="confirmSignout"
      />
    </div>
    
    <CustomButton
      label-name="비밀번호 변경하기"
      :justify="'home'"
      @click="handleEditPassword"
    />
    <Form style="width: 100%">
      <CustomInputText
        v-model="username"
        :input-id="'user-id'"
        :label-name="'수정하실 닉네임을 입력해주세요.'"
        :is-icon="true"
        :error="nicknameError"
        :message="nicknameMessage"
        :icon-class="'pi pi-star'"
      />
      <div class="birth-date">
        <h3>생년월일을 입력해주세요</h3>
        <div class="date-picker">
          <DatePicker
            placeholder="ex) 2025/05/28"
            date-format="yy/mm/dd"
            v-model="birthDate"
            showButtonBar
          />
        </div>
      </div>
      <h3>재직 여부를 선택해주세요.</h3>

      <div class="job mb-2">
        <Select
          v-model="selectedJob"
          :options="job"
          placeholder="재직 여부"
          fluid=""
        ></Select>
      </div>
      <div class="finanacial-status mb-2">
        <h3>현재 자산 현황을 선택해주세요.</h3>
        <Select
          v-model="selectedFinancialStatus"
          :options="assetRange"
          placeholder="자산 현황"
          fluid=""
        ></Select>
      </div>
      <div class="salary mb-2">
        <h3>현재 급여를 선택해주세요.</h3>
        <Select
          v-model="selectedSalary"
          :options="moneyRange"
          placeholder="급여"
          fluid=""
        ></Select>
      </div>
      <br />
      
      <CustomButton
        label-name="수정하기"
        :justify="'end'"
        @click="handleEditPersonalInfo"
      />
    </Form>
  </div>
</template>

<script setup>
import { Form } from "@primevue/forms";
import CustomInputText from "@/components/input/CustomInputText.vue";
import CustomInputNumber from "@/components/input/CustomInputNumber.vue";
import CustomButton from "@/components/button/CustomButton.vue";
import { Button } from "primevue";
import axiosInstance from "@/api/axiosInstance";
import DatePicker from "primevue/datepicker";
import Select from "primevue/select";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useConfirm } from "primevue/useconfirm";

const router = useRouter();
const confirm = useConfirm();

//error 메세지 출력
const error = ref(false);
const emailError = ref(false);
const nicknameError = ref(false);
const message = ref("");
const emailMessage = ref("");
const nicknameMessage = ref("");

const username = ref("");
const birthDate = ref(null);
const assetRange = ref([
  "1,000만원 미만",
  "1,000만원 이상 3,000만원 미만",
  "3,000만원 이상 5,000만원 미만",
  "5,000만원 이상 1억 미만",
  "1억 이상"
]);
const moneyRange = ref([
  "100만원 미만",
  "100만원 이상 200만원 미만",
  "200만원 이상 300만원 미만",
  "300만원 이상 400만원 미만",
  "400만원 이상 500만원 미만",
  "500만원 이상"
]);
const job = ref([
  "직장인",
  "공무원",
  "군인",
  "전문직",
  "학생",
  "취업준비생",
  "자영업자",
  "프리랜서",
  "예술가/창작자",
  "주부",
  "은퇴자",
  "무직"
]);

const selectedJob = ref("");
const selectedFinancialStatus = ref("");
const selectedSalary = ref("");

const confirmChangeInfo = goalId => {
  confirm.require({
    message: "",
    header: "회원 정보 수정이 완료되었어요.",
    acceptProps: {
      label: "목표로 돌아가기"
    },
    rejectProps: {
      label: "페이지 머무르기"
    },
    accept: () => {
      router.push("/");
    },
    reject: () => {
      nicknameError.value = false
    }
  });
};

onMounted(async () => {
  const response = await axiosInstance.get(
    "http://127.0.0.1:8000/api/user/profile/"
  );
  console.log(response);

  username.value = response.data.username;
  birthDate.value = response.data.birth_date;
  selectedJob.value = response.data.work_type;
  selectedFinancialStatus.value = response.data.assets;
  selectedSalary.value = response.data.salary;
});

const handleEditPersonalInfo = async () => {
  try {
    const response = await axiosInstance.put(
      "http://127.0.0.1:8000/api/user/profile/",
      {
        username: username.value,
        birth_date: new Date(birthDate.value).toISOString().split("T")[0],
        work_type: selectedJob.value,
        assets: selectedFinancialStatus.value,
        salary: selectedSalary.value
      }
    );
    confirmChangeInfo();
  } catch (err) {
    const errorData = err.response?.data || {};
    console.error("⛔ 회원가입:", errorData);

    // 서버 응답에 따른 상세 메시지 처리
    if (errorData.email) {
      emailError.value = true;
      emailMessage.value = "이미 존재하는 이메일입니다.";
    }
    if (errorData.username) {
      nicknameError.value = true;
      nicknameMessage.value = "이미 존재하는 닉네임입니다.";
    }
    if (errorData.non_field_errors) {
      error.value = true;
      message.value = "모든 필드를 입력해야합니다.";
    }
  }
};

const handleEditPassword = () => {
  router.replace("/edit/password");
};

const signout = async() => {
  await axiosInstance.delete(
    "http://127.0.0.1:8000/api/auth/signout/"
  )
  router.replace("/login")
}

const confirmSignout = () => {
  confirm.require({
    message: '회원 탈퇴 하시겠습니까?',
    header: '확인',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: {
      label: '회원 유지 하기',
      severity: 'secondary',
      outlined: true,
    },
    acceptProps: {
      label: '회원 탈퇴 하기',
    },
    accept: () => {
      signout()
    },
  })
}
</script>

<style scoped>
.editpersonalinfo-container {
  width: 100%;
}

.title {
  display: flex;
  gap: 1rem;
}

.date-picker {
  display: flex;
  gap: 1rem;
}

.job {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  justify-content: center;
}
</style>
