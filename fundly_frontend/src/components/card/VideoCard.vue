<template>
    <Card :backgroundcolor class="hover card center">
        <template #title>
            {{ cardTitle }}
        </template>
        <template #content>
            <div>
                <!-- 썸네일 -->
                 
                <RouterLink
                  :to="{ name: pageName, params: { id: params } }"
                  class="decorate"
                >
                  <img
                    :src="video.snippet.thumbnails.medium.url"
                    :alt="video.snippet.title"
                    class="thumbnail"
                  />
                  <!-- <CustomTextButton :label-name="video.snippet.title"/> -->
                </RouterLink>
        
              <!-- 채널명 -->
              <h3 class="channel-name">{{ video.snippet.channelTitle }}</h3>
            </div>
        </template>
    </Card>
</template>

<script setup>
    import Card from 'primevue/card';
    import CustomTextButton from '../button/CustomTextButton.vue';
    import { RouterLink } from 'vue-router';
    
defineProps({
  pageName: String,
  params: Object,
  cardTitle: String,
  video: Object,
  backgroundcolor: String
});
</script>

<style scoped>
.decorate {
  text-decoration: none;
}

.card {
  height: 100%;    
}

.thumbnail {
  width: 100%;
  height: auto;
}

.text-end {
  text-align: end;
}

.channel-name {
  color: var(--p-text-color);
  font-weight: bold;
}

.pi {
  padding: 0.4rem;
  border: 0.1px solid;
  border-radius: 1rem;
}

.backgroundcolor {
  color: var(--p-primary-50);
  background-color: var(--p-indigo-300);
}
</style>