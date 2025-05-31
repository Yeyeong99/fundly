<template>
  <div class="community-container">
    <h2>자유롭게 의견과 정보를 공유할 수 있어요.</h2>

    <CustomDataTable
      :columnInfos="columnInfos"
      :data="posts"
      :searchplaceholder="'작성자 / 제목 검색'"
      :type="'products'"
      :pageName="'detail'"
    >
    </CustomDataTable>
    <br />
    <RouterLink :to="{ name: 'writepost' }" class="text-decoration"
      ><CustomButton :label-name="'게시글 작성하기'" :justify="'end'"
    /></RouterLink>
  </div>
</template>

<script setup>
import { onMounted, ref, watchEffect } from "vue";
import CustomButton from "@/components/button/CustomButton.vue";
import CustomDataTable from "@/components/table/CustomDataTable.vue";
import axiosInstance from "@/api/axiosInstance";

const posts = ref([]);

const columnHeader = ["분류", "제목", "작성자", "날짜", "좋아요"];

// 일단 빈 배열로 초기화
let columnInfos = ref([]);

// posts가 변경될 때마다 columnInfos를 생성
watchEffect(() => {
  if (posts.value.length > 0) {
    const columnNames = Object.keys(posts.value[0]).slice(1);
    columnInfos.value = columnNames.map((name, idx) => ({
      field: name,
      header: columnHeader[idx] || name
    }));
  }
});

onMounted(async () => {
  try {
    const response = await axiosInstance.get(
      "http://127.0.0.1:8000/api/community/"
    );
    posts.value = response.data;
    console.log(posts.value);
    
  } catch (err) {
    console.log(err);
  }
});
</script>

<style scoped>
.community-container {
  width: 100%;
}

.text-decoration {
  text-decoration: none;
}

.flex {
  display: flex;
  justify-content: flex-end;
}
</style>
