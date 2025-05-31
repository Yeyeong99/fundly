<template>
  <div class="changepassword-container">
    <h1>비밀번호 수정</h1>
    <Form style="width: 100%;">
      <CustomInputText
        v-model="password"
        :input-id="'password'"
        :label-name="'새로운 비밀번호를 입력해주세요.'"
        :input-type="'password'"
        :isicon="true"
        :iconclass="'pi pi-star'"
      />
      <CustomInputText
        v-model="passwordConfirm"
        :input-id="'password-confirm'"
        :label-name="'다시 한번 입력해주세요.'"
        :isicon="true"
        :input-type="'password'"
        :iconclass="'pi pi-star'"
        :error="error"
        :message="message"
      />
      <br />
      <CustomButton
        label-name="수정하기"
        :justify="'end'"
        @click="handleEditPassword"
      />
    </Form>
  </div>
</template>

<script setup>
  import { Form } from "@primevue/forms";
  import CustomInputText from "@/components/input/CustomInputText.vue";
  import CustomButton from "@/components/button/CustomButton.vue";
  import axiosInstance from "@/api/axiosInstance";
  import { ref } from "vue";
  import { useRouter } from "vue-router";

  const router = useRouter();
  const password = ref('')
  const passwordConfirm = ref('')
  const error = ref(false)
  const message = ref("")

  const handleEditPassword = async () => {
    if (password.value != passwordConfirm.value) {
      error.value = true;
      message.value = "비밀번호가 일치하지 않습니다. 다시 한 번 확인해주세요.";
    } 
    else {
      error.value = false
      try {
        const res = await axiosInstance.patch(
          "http://127.0.0.1:8000/api/user/change-password/",
          {
            password: password.value
          }
        )
        alert("비밀번호가 수정되었습니다.")
        router.replace('/')    // 일단 홈으로 이동
      }
      catch (err) {
        console.error(err)
        alert('비밀번호 수정 실패')
        router.push('/edit/password')
      }
    }
  }

</script>

<style scoped>
.changepassword-container {
  width: 100%;
}
</style>