<template>
    <div class="chatbot-container">
        
        <h1>
            <img 
            width="40px"
            src="@/assets/ChatGPT.png"
            alt="chatbot-logo"
            >
            안녕하세요.<br/>금융에 대해 궁금하신 점이 있나요?
        </h1>
        <p>금융 관련 지식, 상품에 대해서 질문해주세요!</p>
        <div v-if="loading" class="loading">
            <i class="pi pi-spin pi-spinner" style="font-size: 2.5rem"></i>
            <h3>불러오는 중입니다...</h3>
        </div>
        <div class="result">
            <Message
                v-if="answer"
                icon="pi pi-comment"
            >
                <pre class="answer">{{ answer }}</pre>
            </Message>
            
            <CustomButton
                v-if="answer"
                @click="showVideos = !showVideos"
                :label-name="'관련 영상 확인하기'"
                type="submit"
                justify="end"
            />
        </div>
        <div v-if="showVideos" class="video-grid">
            <VideoCard
                v-for="video in relatedVideos"
                :key="video.id.videoId"
                :card-title="video.snippet.title"
                :page-name="'showyoutube'"
                :params="video.id.videoId"
                :video="video"
                class="video-card"
            />
        </div>
        <div class="card">
            <InputText
                class="search-bar"
                v-model="question"
                type="text" 
                variant="filled" 
                placeholder="어떤 것이 궁금하세요?"
            />
            <Button
                class="search-button"
                type="button"
                icon="pi pi-search"
                @click="handleSearch"
            />
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import { InputText } from 'primevue';
    import axiosInstance from '@/api/axiosInstance';
    import Message from 'primevue/message';
    import Button from "primevue/button";
    import CustomButton from '@/components/button/CustomButton.vue';
    import VideoCard from '@/components/card/VideoCard.vue';
    import { useVideoStore } from '@/stores/video';
    
    const appStore = useVideoStore()
    const question = ref('')
    const answer = ref(null);
    const relatedVideos = ref([]);
    const loading = ref(false)

    // 버튼 클릭하면 영상 나타나게 하게
    const showVideos = ref(false)

    // 검색어 입력하면 호출되어서 답변과 영상 업데이트
    const handleSearch = async () => {
        answer.value = null
        // 검색어가 있는 경우에만 처리
        if (question.value.trim()) {
            // 검색어에 대한 답변 >> 실제 로직에서는 API 호출이나 다른 처리 추가하기
            if (answer.value === null) {
                loading.value = true
            }
            const response = await axiosInstance.post(
                "http://127.0.0.1:8000/api/chatbot/",
                {
                    question: question.value
                }
            )

            answer.value = `${response.data.answer}`
            loading.value = false
            // 관련 동영상 리스트를 검색어 기반으로 업데이트
            appStore.searchKeyword(response.data.keyword);
            relatedVideos.value = appStore.videos;
        }
        else {
            answer.value = ''
            relatedVideos.value = []
        }
    }

    
</script>

<style scoped>
.chatbot-container {
    margin: 20px
}

.result {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.answer {
    text-decoration: none;
    font-size: 1rem;
    font-family: noto-sans;
    white-space: pre-wrap;
    margin-bottom: 2rem;
}

.video-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 20px;
}

.card {
    display: flex;
}
.search-bar {
    align-content: end;
    margin-top: 10px;
}
.search-button {
    margin-top: 10px;
}
</style>