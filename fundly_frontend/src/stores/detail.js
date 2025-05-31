// src/stores/detail.js
import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useDetailStore = defineStore("detail", () => {
  const API_KEY = import.meta.env.VITE_API_KEY;
  const API_URL = "https://www.googleapis.com/youtube/v3/videos";

  const videoDetail = ref(null);

  const getVideoDetail = async (videoId) => {
    const params = {
      key: API_KEY,
      part: "snippet",
      id: videoId,
    };

    try {
      const res = await axios.get(API_URL, { params });
      videoDetail.value = res.data.items[0];
      
      console.log(videoDetail)
    } catch (e) {
      console.error("비디오 상세 정보 로딩 실패:", e);
    }
  };

  

  return {
    videoDetail,
    getVideoDetail,
  };
});