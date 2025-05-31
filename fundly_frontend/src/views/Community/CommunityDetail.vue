<template>
  <div class="detail-container">
    <div class="detail-top">
      <h2 class="title">{{ title }}</h2>
      <div class="edit-delete" v-if="currentUser && writer === currentUser.username">
        <Button
          type="button"
          icon="pi pi-ellipsis-v"
          @click="toggle"
          aria-haspopup="true"
          aria-controls="overlay_menu"
          text
        />
        <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />
      </div>
    </div>
    <div class="detail-data">
      <h4 class="content-writer">{{ writer }}</h4>
      <p class="content-written-day">{{ date }}</p>
    </div>
    <article class="content">
      <pre class="content">{{ content }}</pre>
    </article>
    <div class="detail-bottom">
      <div class="likes">
        <p>{{ likeCount }}</p>
        <p :class="likeClass" class="like-button" @click="toggleLike">
          <span> 좋아요</span>
        </p>
      </div>
      <h3 class="comments-list-title">댓글 목록</h3>
      <div class="comment-container" v-for="comment in comments" :key="comment.id">
        <div class="comment-top">
          <h4 class="comment-writer">{{ comment.user.username }}</h4>
          <span
            class="pi pi-times"
            v-if="currentUser && comment.user.username === currentUser.username"
            @click="deleteComment(comment.id)"
          ></span>
        </div>
        <p>
          <span class="comment-content">{{ comment.content }}</span>
        </p>
        <span class="comment-created-at">{{ formatDate(comment.created_at) }}</span>
      </div>
      <div class="comment-write">
        <Textarea fluid v-model="commentContent"></Textarea>
        <CustomButton label-name="등록" justify="end" @click="postComment"></CustomButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import { useUserStore } from '@/stores/user'
import axiosInstance from '@/api/axiosInstance'
import Textarea from 'primevue/textarea'
import CustomButton from '@/components/button/CustomButton.vue'
import Button from 'primevue/button'
import Menu from 'primevue/menu'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const currentUser = computed(() => userStore.user)

const id = route.params.id
const title = ref('제목')
const date = ref('작성 일자')
const writer = ref('작성자')
const content = ref('작성 내용')
const comments = ref([])
const likeCount = ref(0)
const isLiked = ref(false)
const likeClass = computed(() => (isLiked.value ? 'pi pi-heart-fill' : 'pi pi-heart'))

// 댓글 작성 시 목록 다시 불러오기
const fetchComments = async () => {
  try {
    const res = await axiosInstance.get(`http://127.0.0.1:8000/api/community/${id}/comments/`)

    comments.value = res.data
  } catch (err) {
    console.error('❌ 댓글 불러오기 실패:', err)
  }
}

const fetchPost = async () => {
  try {
    const response = await axiosInstance.get(`http://127.0.0.1:8000/api/community/${id}/`)
    const post = response.data

    title.value = post.title
    date.value = post.created_at.split('T')[0]
    writer.value = post.user
    content.value = post.content
    likeCount.value = post.num_of_likes
    isLiked.value = post.is_liked
    console.log(isLiked.value)
  } catch (err) {
    console.log('게시글 불러오기 실패:', err)
  }
}

// 게시글 정보 불러오기
onMounted(async () => {
  await userStore.fetchUser()
  await fetchComments()
  await fetchPost()
})

// 게시글 댓글 작성
const commentContent = ref('')
const postComment = async () => {
  try {
    const response = await axiosInstance.post(
      `http://127.0.0.1:8000/api/community/${id}/comments/`,
      { post_id: id, content: commentContent.value },
    )
    commentContent.value = ''
    await fetchComments()
  } catch (err) {
    console.log(err)
  }
}

// 댓글 삭제
const deleteComment = async (comment_id) => {
  try {
    const response = await axiosInstance.delete(
      `http://127.0.0.1:8000/api/community/comments/${comment_id}/`,
    )
    await fetchComments()
  } catch (err) {
    console.log(err)
  }
}

// 게시글 삭제
const deletePost = async () => {
  try {
    const response = await axiosInstance.delete(`http://127.0.0.1:8000/api/community/${id}/`)
    router.push('/community')
  } catch (err) {
    console.log(err)
  }
}

// 게시글 수정
const editPost = async () => {
  try {
    router.push(`/community/edit/${id}`)
  } catch (err) {
    console.log(err)
  }
}

const confirm = useConfirm()

const showDetailDelete = () => {
  confirm.require({
    message: '정말 삭제하시겠습니까?',
    header: '목표 삭제 하기',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: {
      label: '취소',
      severity: 'secondary',
      outlined: true,
    },
    acceptProps: {
      label: '삭제 하기',
    },
    accept() {
      deletePost()
    },
    reject() {},
  })
}

// 좋아요 버튼
const toggleLike = async () => {
  try {
    // 프론트에서 먼저 토글 처리
    isLiked.value = !isLiked.value
    likeCount.value += isLiked.value ? 1 : -1

    // 서버에 반영
    await axiosInstance.post(`http://127.0.0.1:8000/api/community/${id}/likes/`)
  } catch (err) {
    console.error('좋아요 처리 실패:', err)
    // 실패 시 롤백
    isLiked.value = !isLiked.value
    likeClass.value = isLiked.value ? 'pi pi-heart-fill' : 'pi pi-heart'
    likeCount.value += isLiked.value ? 1 : -1
  }
}
// 게시글 delete, edit 버튼
const menu = ref()
const items = ref([
  {
    items: [
      {
        label: '수정',
        icon: 'pi pi-pen-to-square',
        command: editPost,
      },
      {
        label: '삭제',
        icon: 'pi pi-times',
        command: showDetailDelete,
      },
    ],
  },
])

const toggle = (event) => {
  menu.value.toggle(event)
}

// 날짜 포맷 지정

const formatDate = (isoString) => {
  const date = new Date(isoString)
  const yy = String(date.getFullYear()).slice(2)
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const min = String(date.getMinutes()).padStart(2, '0')
  return `${yy}-${mm}-${dd} ${hh}:${min}`
}
</script>

<style scoped>
.detail-container {
  width: 100%;
  height: 70%;
}

.detail-top {
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
}

.title {
  margin: 0;
}

.detail-data {
  width: 100%;
  border-bottom: 0.3px solid var(--p-primary-500);
  display: flex;
  justify-content: space-between;
}

.content-writer,
.content-written-day {
  margin: 0;
  margin-bottom: 0.5rem;
}

article.content {
  margin: 2rem;
}

pre.content {
  text-decoration: none;
  font-size: 1rem;
  font-family: noto-sans;
  white-space: pre-wrap;
  margin-bottom: 2rem;
}
  

.likes {
  display: flex;
  justify-content: space-between;
}

.like-button {
  cursor: pointer;
  margin-bottom: 1.5rem;
}

.comment-top {
  display: flex;
  justify-content: space-between;
}

.comments-list-title {
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-bottom: 0.3px solid var(--p-primary-500);
}

.comment-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.4rem;
  border-bottom: 0.3px dotted var(--p-primary-500);
  margin-bottom: 0.8rem;
  padding: 0.4rem;
}

.comment-content {
  margin-left: 0.5rem;
}

.comment-created-at {
  text-align: end;
}

.pi-times {
  cursor: pointer;
}
</style>
