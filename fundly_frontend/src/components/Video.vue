<template>
    <div class="video-wrapper">
        
        <iframe
            width="100%"
            height="315" 
            :src="`https://www.youtube.com/embed/${video.id.videoId || video.id}`" 
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
        ></iframe>
        <!-- 제목 -->
        <h1>{{ video.snippet.title }}</h1>
        <p>{{ video.snippet.publishedAt }}</p>
        <!-- 채널명 -->
        <h3 class="channel-name">채널명 : {{ video.snippet.channelTitle }}</h3>
        <!-- 상세정보 -->
        <pre class="description">{{ video.snippet.description }}</pre>

    </div>
</template>

<script setup>
    defineProps({
        video: Object,
    })
</script>

<style scoped>
    .video-wrapper {
        margin-bottom: 20px;
    }
    
    .channel-name {
        display: flex;
        justify-content: end;
    }

    .description {
        text-decoration: none;
        font-size: 1rem;
        font-family: noto-sans;
        white-space: pre-wrap;
        margin-bottom: 2rem;
    }
</style>