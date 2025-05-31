<template>
  <p>카카오 로그인 처리 중입니다...</p>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axioInstance from '@/api/axiosInstance'
import { checkNicknameAndRedirect } from '@/utils/checkNicknameAndRedirect' // ✅ 유틸 함수 경로는 상황에 맞게 수정하세요.

const router = useRouter()

onMounted(async () => {
  const url = new URL(window.location.href)
  const code = url.searchParams.get('code')

  if (code) {
    try {
      const res = await axioInstance.post('http://127.0.0.1:8000/api/auth/kakao/login/', {
        code,
        redirect_uri: 'http://localhost:5173/api/auth/kakao/callback/', // ✅ Vue도 redirect_uri 명시
      })

      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)

      checkNicknameAndRedirect(router) // ✅ 닉네임 확인 후 이동
    } catch (err) {
      console.error('⛔ 카카오 로그인 실패:', err.response?.data || err)
      alert('카카오 로그인 실패')
      router.push('/login')
    }
  }
})
</script>
