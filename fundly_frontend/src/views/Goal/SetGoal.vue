<template>
  <div class="goal-container">
    <Form>
      <div class="goal">
        <div class="goal-name">
          <h3>어떤 목표를 달성하고 싶으신가요?</h3>
          <CustomInputText
            v-model="goalName"
            :is-icon="true"
            :icon-class="'pi pi-star'"
            :input-id="'goal-name'"
            :input-placeholder="'예) 전세 자금 마련하기'"
          />
        </div>

        <div class="target-amount">
          <h3>목표 금액을 설정해주세요.</h3>
          <CustomInputNumber
            v-model="targetAmount"
            :key="targetAmountKey"
            :is-icon="true"
            :icon-class="'pi pi-star'"
            :input-id="'target-amount'"
            :input-placeholder="'0'"
            :unit="'만 원'"
          />
        </div>

        <div class="target-period">
          <h3>시작 시기와 끝 시기를 알려주세요.</h3>
          <div class="date-picker">
            <DatePicker
              placeholder="시작 날짜"
              date-format="yy/mm/dd"
              v-model="startDate"
              showButtonBar
            />
            <DatePicker
              placeholder="끝 날짜"
              date-format="yy/mm/dd"
              v-model="endDate"
              showButtonBar
            />
            <Button label="- 6개월" outlined @click="decrementEndDate"></Button>
            <Button label="+ 6개월" outlined @click="incrementEndDate"></Button>
          </div>
          <Message v-if="isDateError" severity="error">시작 시기는 끝보다 앞서야 합니다.</Message>
        </div>

        <div class="goal-method">
          <label for="product-type">
            <h3>목표를 달성할 방식을 알려주세요.</h3>
          </label>
          <SelectButton
            id="product-type"
            v-model="selectedProductType"
            :key="selectedProductTypeKey"
            :options="productType"
            optionValue="value"
            optionLabel="name"
            multiple
            aria-labelledby="multiple"
            fluid
          />
        </div>
        <Message v-if="isError" severity="error">{{ message }}</Message>
      </div>

      <CustomButton
        @click="saveGoal"
        :label-name="isEditMode ? '목표 수정하기' : '목표 설정하기'"
        type="submit"
        justify="end"
      />
    </Form>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axiosInstance from '@/api/axiosInstance'
import Button from 'primevue/button'
import CustomInputNumber from '@/components/input/CustomInputNumber.vue'
import CustomInputText from '@/components/input/CustomInputText.vue'
import SelectButton from 'primevue/selectbutton'
import CustomButton from '@/components/button/CustomButton.vue'
import DatePicker from 'primevue/datepicker'
import { Form } from '@primevue/forms'
import { useConfirm } from 'primevue/useconfirm'
import Message from 'primevue/message'

const confirm = useConfirm()
const route = useRoute()
const router = useRouter()

const goalId = route.params.goalid
const isEditMode = !!goalId

const goalName = ref('')
const targetAmount = ref(null)
const selectedProductType = ref(null)
const startDate = ref('')
const endDate = ref('')
const isError = ref(false)
const targetAmountKey = ref(0)
const selectedProductTypeKey = ref(0)
const message = ref('')

const productType = ref([
  { name: '적금', value: '적금' },
  { name: '예금', value: '예금' },
])

const getProductTypeCode = (selection) => {
  if (selection.includes('적금') && selection.includes('예금')) return 'A'
  if (selection.includes('적금')) return 'S'
  if (selection.includes('예금')) return 'D'
  return 'D'
}

// 6개월씩 감소시키는 버튼
const decrementEndDate = () => {
  // 기준 날짜: endDate가 있으면 그걸 기준으로
  const baseDate = endDate.value ? new Date(endDate.value) : new Date(startDate.value)

  if (!baseDate || isNaN(baseDate)) {
    console.error('유효한 날짜가 없습니다.')
    return
  }

  const newDate = new Date(baseDate)
  newDate.setMonth(newDate.getMonth() - 6)

  // YYYY-MM-DD 형식으로 저장
  endDate.value = newDate.toISOString().slice(0, 10)
}

// 6개월씩 증가시키는 버튼
const incrementEndDate = () => {
  // 기준 날짜를 endDate가 있으면 그걸 기준으로, 없으면 startDate로
  const baseDate = endDate.value ? new Date(endDate.value) : new Date(startDate.value)

  if (!baseDate || isNaN(baseDate)) {
    console.error('유효한 날짜가 없습니다.')
    return
  }

  const newDate = new Date(baseDate)
  newDate.setMonth(newDate.getMonth() + 6)

  // YYYY-MM-DD 형식으로 저장
  endDate.value = newDate.toISOString().slice(0, 10)
}

// 시작 - 끝 시기 검사
const isDateError = ref(false)

watch([startDate, endDate], ([newStart, newEnd]) => {
  if (newStart && newEnd) {
    const start = new Date(newStart)
    const end = new Date(newEnd)
    isDateError.value = start > end
  } else {
    isDateError.value = false
  }
})

const confirmGoal = () => {
  confirm.require({
    message: `예금과 적금 상품을 등록하면,\n목표 달성까지의 여정을 한눈에 볼 수 있어요.`,
    header: '목표가 성공적으로 설정되었어요!',
    icon: 'pi pi-check',
    rejectProps: {
      label: '금융 상품 추천 받기',
      outlined: true,
    },
    acceptProps: {
      label: '금융 상품 목록 보기',
    },
    accept: () => {
      router.replace('/checkproducts')
    },
    reject: () => {
      router.replace('/recommendproducts')
    },
  })
}

const saveGoal = async () => {
  if (
    !goalName.value ||
    targetAmount.value === null ||
    targetAmount.value === '' ||
    !selectedProductType.value ||
    selectedProductType.value.length === 0 ||
    !startDate.value ||
    !endDate.value ||
    isDateError.value
  ) {
    isError.value = true
    message.value = '모든 값을 입력해주세요.'
    return
  } else {
    isError.value = false
  }
  const productTypeCode = getProductTypeCode(selectedProductType.value)

  const start = new Date(startDate.value)
  const end = new Date(endDate.value)
  const payload = {
    goal_name: goalName.value,
    total_target_amount: Number(targetAmount.value) * 10000,
    product_type: productTypeCode,
    start_date: start.toISOString().slice(0, 10),
    end_date: end.toISOString().slice(0, 10),
  }

  try {
    if (isEditMode) {
      await axiosInstance.put(`http://127.0.0.1:8000/api/goals/${goalId}/`, payload)
      router.replace(`/checkgoal/${goalId}`)
    } else {
      await axiosInstance.post('http://127.0.0.1:8000/api/goals/', payload)
      confirmGoal()
    }
  } catch (err) {
    console.error('에러 발생:', err)
  }
}

onMounted(async () => {
  if (isEditMode) {
    try {
      const response = await axiosInstance.get(`http://127.0.0.1:8000/api/goals/${goalId}/`)
      const data = response.data

      goalName.value = data.goal_name
      targetAmount.value = Number(data.total_target_amount) / 10000
      targetAmountKey.value++

      if (data.product_type === 'A') {
        selectedProductType.value = ['적금', '예금']
      } else if (data.product_type === 'S') {
        selectedProductType.value = ['적금']
      } else if (data.product_type === 'D') {
        selectedProductType.value = ['예금']
      }
      selectedProductType.value = [...selectedProductType.value]
      selectedProductTypeKey.value++
      startDate.value = new Date(data.start_date)
      endDate.value = new Date(data.end_date)
    } catch (err) {
      console.error('목표 정보 불러오기 실패:', err)
    }
  }
})
</script>

<style scoped>
h3 {
  margin-bottom: 1rem;
}
.goal-container {
  width: 100%;
}
.goal {
  margin-bottom: 2rem;
}
.goal-name,
.target-amount,
.target-period {
  margin-bottom: 1rem;
}
.date-picker {
  display: flex;
  justify-content: space-between;
}
.goal-method {
  margin-bottom: 1rem;
}
</style>
