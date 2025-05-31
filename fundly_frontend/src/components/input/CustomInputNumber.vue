<template>
  <IconField :style="inlineBlock ? { display: 'inline-block' } : {}">
    <InputIcon v-if="isIcon">
      <i :class="iconClass" style="color: var(--p-amber-400)" />
    </InputIcon>
    <FloatLabel>
      <div></div>
      <InputNumber
        :id="inputId"
        inputId="over_label"
        v-model="internalValue"
        :placeholder="inputPlaceholder"
        fluid
      />
      <label for="over_label" v-if="props.isLabel">{{ props.labelName }}</label>
    </FloatLabel>
    <InputIcon v-if="unit">
      <span>{{ unit }}</span>
    </InputIcon>
  </IconField>
</template>

<script setup>
import { ref, watch } from 'vue'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputNumber from 'primevue/inputnumber'
import { FloatLabel } from 'primevue'
const props = defineProps({
  labelName: String,
  isIcon: Boolean,
  isLabel: Boolean,
  inlineBlock: Boolean,
  iconClass: String,
  modelValue: Number,
  inputId: String,
  inputPlaceholder: String,
  unit: String,
})

const emit = defineEmits(['update:modelValue'])

// 내부 상태로 값 관리
const internalValue = ref(props.modelValue)

// 부모 modelValue가 변경되면 internalValue도 업데이트
watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal !== internalValue.value) {
      internalValue.value = newVal
    }
  },
)

// internalValue가 변경되면 부모에 emit
watch(internalValue, (newVal) => {
  if (newVal !== props.modelValue) {
    emit('update:modelValue', newVal)
  }
})
</script>

<style scoped></style>
