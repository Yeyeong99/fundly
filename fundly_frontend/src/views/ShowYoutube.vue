<template>
    <div
        class="ma-6 youtube-container"
        v-if="detailStore.videoDetail"
    >
        <Video
            :video="detailStore.videoDetail"
        />

    </div>
    
</template>

<script setup>
    import { onMounted } from 'vue';
    import { useRoute } from 'vue-router';
    import { useDetailStore } from '@/stores/detail';
    import Video from '@/components/Video.vue';

    const detailStore = useDetailStore()
    const route = useRoute()

    onMounted(() => {
        const videoId = route.params.id
        detailStore.getVideoDetail(videoId)
    })
</script>

<style scoped>


.video {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-bottom: 6rem;
}
</style>
