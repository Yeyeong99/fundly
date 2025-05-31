<template>
  <div class="signup-container">
    <h1>회원가입</h1>
    <Form style="width: 100%">
      <CustomInputText
        v-model="username"
        :input-id="'user-id'"
        :label-name="'사용하실 닉네임을 입력해주세요.'"
        :isicon="true"
        :iconclass="'pi pi-star'"
        :error="nicknameError"
        :message="nicknameMessage"
      />
      <CustomInputText
        v-model="email"
        :input-id="'email'"
        :label-name="'로그인에 사용될 이메일 주소를 알려주세요.'"
        :isicon="true"
        :iconclass="'pi pi-star'"
        :error="emailError"
        :message="emailMessage"
      />
      <CustomInputText
        v-model="password"
        :input-id="'password'"
        :label-name="'사용하실 비밀번호를 입력해주세요.'"
        :input-type="'password'"
        :isicon="true"
        :iconclass="'pi pi-star'"
      />
      <CustomInputText
        v-model="passwordConfirm"
        :input-id="'password-confirm'"
        :label-name="'사용하실 비밀번호를 확인해주세요.'"
        :isicon="true"
        :input-type="'password'"
        :iconclass="'pi pi-star'"
        :error="passwordError"
        :message="passwordMessage"
      />
      <br />
      <CustomButton
        label-name="가입하기"
        :justify="'end'"
        @click="handleSignup"
      />
      <Message v-if="error">{{ message }}</Message>
    </Form>
  </div>
</template>

<script setup>
import { Form } from "@primevue/forms";
import CustomInputText from "@/components/input/CustomInputText.vue";
import CustomButton from "@/components/button/CustomButton.vue";
import axiosInstance from "@/api/axiosInstance";
import { Message } from "primevue";
import { ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const username = ref("");
const password = ref("");
const passwordConfirm = ref("");
const email = ref("");

//error 메세지 출력
const error = ref(false);
const passwordError = ref(false);
const emailError = ref(false);
const nicknameError = ref(false);
const message = ref("");
const passwordMessage = ref("");
const emailMessage = ref("");
const nicknameMessage = ref("");

const handleSignup = async () => {
  if (password.value != passwordConfirm.value) {
    passwordError.value = false;
    passwordMessage.value =
      "비밀번호가 일치하지 않습니다. 다시 한 번 확인해주세요.";
  } else {
    error.value = false;
    emailError.value = false;
    nicknameError.value = false;
    try {
      const res = await axiosInstance.post(
        "http://127.0.0.1:8000/api/auth/signup/",
        {
          username: username.value,
          email: email.value,
          password1: password.value,
          password2: passwordConfirm.value
        }
      );

      const { access, refresh, user } = res.data;

      // 토큰을 localStorage에 저장
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);

      // 로그인 완료
      console.log(access);
      router.push("/");
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
  }
};
</script>

<style scoped>
.signup-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
