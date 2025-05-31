<template>
  <div class="side-bar collapse">
    <div class="basic-menu">
      <h3>기본 메뉴</h3>
      <div class="basic-menu-list">
        <RouterLink v-for="menu in basicMenu" :key="menu.name" :to="{ name: menu.name[0] }"
          ><CustomTextButton
            :label-name="menu.labelname"
            :class-name="{ active: menu.name.includes(route.name) }"
        /></RouterLink>
      </div>
    </div>
    <div class="my-page">
      <h3>마이 페이지</h3>
      <div class="my-page-list">
        <RouterLink v-for="menu in myPage" :key="menu.name" :to="{ name: menu.name[0] }"
          ><CustomTextButton
            :label-name="menu.labelname"
            :class-name="{ active: menu.name.includes(route.name) }"
        /></RouterLink>
        <CustomTextButton @click="confirmLogout" :label-name="'로그아웃'"> </CustomTextButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useRoute, useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import { ref } from 'vue'
import CustomTextButton from '@/components/button/CustomTextButton.vue'

const route = useRoute()
const router = useRouter()
const confirm = useConfirm()

const basicMenu = ref([
  {
    name: ['checkgoal', 'goaldetail'],
    labelname: '목표 확인 하기',
    path: '/',
  },
  {
    name: ['setgoal'],
    labelname: '목표 추가 하기',
    path: '/setgoal',
  },
  {
    name: ['checkproducts'],
    labelname: '금융 상품 목록',
    path: '/checkproducts',
  },
  {
    name: ['recommendproducts'],
    labelname: '금융 상품 추천',
    path: '/recommendproducts',
  },
  {
    name: ['searchbank'],
    labelname: '주변 은행 찾기',
    path: '/searchbank',
  },
  {
    name: ['community', 'detail', 'writepost'],
    labelname: '커뮤니티',
    path: '/community',
  },
  {
    name: ['checkspot'],
    labelname: '현물 시세 확인하기',
    path: '/checkspot',
  },
  {
    name: ['chatbot'],
    labelname: '질문하기',
    path: '/chatbot',
  },
])

const myPage = [
  {
    name: ['checkuser'],
    labelname: '개인 정보 변경',
    path: '/checkuser',
  },
  {
    name: ['likeproducts'],
    labelname: '찜한 상품 보기',
    path: '/likeproducts',
  },
]

// 로그아웃
const logout = () => {
  // 예: localStorage에 저장된 토큰 삭제
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')

  // 로그인 페이지로 이동 (vue-router 사용 시)
  router.push({ name: 'login' })
}
const confirmLogout = () => {
  confirm.require({
    message: '로그아웃 하시겠습니까?',
    header: '확인',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: {
      label: '로그인 유지 하기',
      severity: 'secondary',
      outlined: true,
    },
    acceptProps: {
      label: '로그아웃 하기',
    },
    accept: () => {
      logout()
    },
  })
}
</script>

<style scoped>
.side-bar {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-left: 2.5rem;
  border-right: 0.3px solid var(--p-gray-300);
}

.basic-menu,
.my-page {
  text-align: end;
}

h3 {
  padding-right: 2rem;
}
.basic-menu-list,
.my-page-list {
  margin-left: 1rem;
  display: flex;
  flex-direction: column;
}

.basic-menu-list {
  margin-bottom: 4rem;
}

@media (max-width: 768px) {
  .collapse {
    display: none;
  }
}
</style>
