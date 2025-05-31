<template>
  <div class="writepost-container">
    <h2 class="title">{{ isEdit ? "게시글 수정" : "게시글 작성" }}</h2>
    <div class="select-category">
      <Select
        v-model="category"
        placeholder="말머리 선택"
        :options="categories"
      />
    </div>
    <div class="post-title">
      <CustomInputText v-model="title" input-placeholder="게시글 제목" />
    </div>
    <div class="post-content">
      <Textarea
        v-model="content"
        placeholder="게시글 내용"
        style="height: 100%;"
        fluid=""
      />
    </div>
    <CustomButton
      :label-name="isEdit ? '수정하기' : '작성하기'"
      justify="end"
      @click="submitPost"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import Select from "primevue/select";
import Textarea from "primevue/textarea";
import CustomInputText from "@/components/input/CustomInputText.vue";
import CustomButton from "@/components/button/CustomButton.vue";
import axiosInstance from "@/api/axiosInstance";

const route = useRoute();
const router = useRouter();

const postId = route.params.id;
const isEdit = computed(() => !!postId);

const title = ref("");
const content = ref("");
const category = ref("");
const categories = ref(["금융 상품 문의", "기본 지식 공유", "꿀팁 공유", "자유"]);

onMounted(async () => {
  if (isEdit.value) {
    try {
      const { data } = await axiosInstance.get(
        `http://127.0.0.1:8000/api/community/${postId}/`
      );
      title.value = data.title;
      content.value = data.content;
      category.value = data.category;
    } catch (err) {
      console.error("❌ 게시글 정보 불러오기 실패:", err);
    }
  }
});

const submitPost = async () => {
  try {
    const payload = {
      title: title.value,
      content: content.value,
      category: category.value
    };

    if (isEdit.value) {
      await axiosInstance.put(
        `http://127.0.0.1:8000/api/community/${postId}/`,
        payload
      );
      router.replace(`/community/detail/${postId}`);
    } else {
      await axiosInstance.post("http://127.0.0.1:8000/api/community/", payload);
      router.push("/community");
    }
  } catch (err) {
    console.error("❌ 게시글 저장 실패:", err);
  }
};
</script>

<style scoped>
.writepost-container {
  width: 60%;
  height: 70%;
}

.title,
.select-category,
.post-title,
.post-content {
  margin-bottom: 1rem;
}
.post-content {
  width: 100%;
  height: 50%;
}
</style>
