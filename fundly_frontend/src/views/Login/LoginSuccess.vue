<template>
  <RouterView />
</template>
<script setup>
import { useRoute, useRouter } from "vue-router";
import { onMounted } from "vue";
import axiosInstance from "@/api/axiosInstance";
import { useConfirm } from "primevue/useconfirm";

const confirm = useConfirm();
const route = useRoute();
const router = useRouter();

const confirmSignup = () => {
  confirm.require({
    message: "원활한 이용을 위해 닉네임을 변경해주세요.",
    header: "Fundly에 오신 것을 환영해요!",
    icon: "pi pi-check",
    acceptProps: {
      label: "닉네임 변경 하기"
    },
    rejectProps: {
      label: "다음에 하기"
    },
    accept: () => {
      router.push("/edit/personalinfo");
    },
    reject: () => {
      router.push("/");
    }
  });
};

const failLogin = () => {
  confirm.require({
    message: "로그인을 다시 시도해주세요.",
    header: "오류가 생겼어요.",
    icon: "pi pi-check",
    acceptProps: {
      label: "로그인 화면으로 이동"
    },
    rejectProps: {
      label: "다음에 하기"
    },
    accept: () => {
      router.push("/login");
    }
  });
};

onMounted(async () => {
  console.log(route.query);
  const access = route.query.access;
  const refresh = route.query.refresh;
  const user = route.query.user;

  console.log(access);

  if (access && refresh) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    localStorage.setItem("user", user);

    const response = await axiosInstance.get(
      "http://127.0.0.1:8000/api/user/first-login/"
    );

    if (response.data.message) {
      confirmSignup(); // 개인 정보 수정페이지로 이동
    } else {
      router.push("/");
    }
  } else {
    failLogin();
  }
});
</script>
