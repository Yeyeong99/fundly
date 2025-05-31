// Utilities
import axios from "axios";
import { ref, computed } from "vue";
import { defineStore } from "pinia";


export const useVideoStore = defineStore("app", () => {
  const API_KEY = import.meta.env.VITE_API_KEY;
  const API_URL = "https://www.googleapis.com/youtube/v3/search";

  const videos = ref([]); // 컴포넌트에서 사용할 반응형 데이터

  const searchKeyword = async (keyword) => {
    const params = {
      key: API_KEY,
      part: "snippet",
      type: "video",
      q: keyword,
      maxResults: 6,
    };

    try {
      const res = await axios.get(API_URL, { params });
      videos.value = res.data.items;
      console.log(videos.value);
    } catch (error) {
      console.error("검색 실패:", error);
    }
  };

  // 저장된 비디오 찾는 getters
  const savedVideos = computed(() => {
    return videos.value.filter((video) => video.isSaved === true)
  })


  // 비디오 저장
  const saveVideo = function (newVideo) {
    // isSaved 처리하기
    const video = videos.value.find((video) => video.id.videoId === newVideo.id)
    if (video === undefined) {
      videos.value.push(newVideo)
      newVideo.isSaved = true
    }
    else {
      video.isSaved = true
    }
    
  }

  // 비디오 삭제하기 >> 재배열
  const deleteVideo = function (selectedId) {
      videos.value = videos.value.filter((video) => video.id.videoId !== selectedId)
  }

  // 비디오 좋아요
  const likeVideo = function (selectedId) {
    // isSaved 처리하기
    const video = videos.value.find((video) => video.id.videoId === selectedId)
    video.isLiked = true
  }

  return {
    videos,
    savedVideos,
    searchKeyword,
    saveVideo,
    deleteVideo,
    likeVideo,
  };
});