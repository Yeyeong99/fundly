import axiosInstance from '@/api/axiosInstance'

export const checkNicknameAndRedirect = async (navigate) => {
  const access = localStorage.getItem('access_token')
  try {
    const res = await axiosInstance.get('http://localhost:8000/api/auth/user', {
      headers: {
        Authorization: `Bearer ${access}`,
      },
    })

    const nickname = res.data.nickname
    if (!nickname) {
      navigate('/setnickname')
    } else {
      navigate('/dashboard')
    }
  } catch (err) {
    console.error('❌ 유저 정보 요청 실패', err)
    navigate('/login') // 에러 발생 시 로그인으로
  }
}
