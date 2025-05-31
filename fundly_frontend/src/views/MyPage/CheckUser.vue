<template>
  <div class="checkuser-container">
    <h2>개인 정보 변경</h2>
    <Form style="width: 100%">
      <CustomInputText
        v-model="password"
        :input-id="'password'"
        :label-name="'정보 변경을 위해 현재 비밀번호를 입력해주세요.'"
        :input-type="'password'"
        :isicon="true"
        :iconclass="'pi pi-star'"
        :error="error"
        :message="message"
      />
      <br />
      <CustomButton label-name="인증하기" :justify="'end'" @click="handleCheckUser" />
    </Form>
  </div>
</template>

<script setup>
import { Form } from '@primevue/forms'
import CustomInputText from '@/components/input/CustomInputText.vue'
import CustomButton from '@/components/button/CustomButton.vue'
import axiosInstance from '@/api/axiosInstance'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const password = ref('')
const error = ref(false)
const message = ref('')
onMounted(async () => {
  try {
    const response = await axiosInstance.post('http://127.0.0.1:8000/api/user/verify-password/', {
      password: '',
    })
    console.log(response.data.message)
    if (response.data.message === false) {
      router.push('/edit/personalinfo')
    }
  } catch (err) {
    console.error(err)
  }
})

const handleCheckUser = async () => {
  try {
    const res = await axiosInstance.post('http://127.0.0.1:8000/api/user/verify-password/', {
      password: password.value,
    })

    if (res.data.error) {
      error.value = true
      message.value = '올바른 비밀번호를 입력해주세요.'
    } else {
      error.value = false
      router.replace('/edit/personalinfo')
    }
  } catch (err) {
    error.value = true
    message.value = '올바른 비밀번호를 입력해주세요.'
  }
}
</script>

<style scoped>
.checkuser-container {
  width: 100%;
}
</style>
