import {defineStore} from "pinia";
import axiosInstance from "@/api/axiosInstance";

export const useUserStore = defineStore("user", {
  state: () => ({user: null}),
  actions: {
    async fetchUser() {
      try {
        const response = await axiosInstance.get("http://127.0.0.1:8000/api/auth/current-user/");
        this.user = response.data;
      } catch (error) {
        console.error("사용자 정보를 불러오는 데 실패했습니다.", error);
        this.user = null;
      }
    },
    logout() {
      this.user = null;
    }
  },
  getters: {
    isAuthenticated: state => !!state.user
  }
});