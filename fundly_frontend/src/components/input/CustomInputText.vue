<template>
  <label :for="inputId"
    ><h3>{{ labelName }}</h3></label
  >
  <IconField>
    <InputIcon v-if="isIcon">
      <i :class="iconClass" style="color: var(--p-amber-400)" />
    </InputIcon>
    <InputText
      :id="inputId"
      :value="modelValue"
      :placeholder="inputPlaceholder"
      :type="inputType"
      :autocomplete="inputType === 'password' ? 'current-password' : 'username'"
      @update:modelValue="value => emit('update:modelValue', value)"
      fluid
    />
    <Message
      v-if="error"
      size="small"
      severity="error"
      variant="simple"
      fluid
      >{{ message }}</Message
    >

    <InputIcon> </InputIcon>
  </IconField>
</template>

<script setup>
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
defineProps({
  labelName: String,
  isIcon: Boolean,
  iconClass: String,
  iconColor: String,
  modelValue: String,
  inputId: String,
  inputPlaceholder: String,
  inputType: String,
  error: Boolean,
  message: String
});

const emit = defineEmits(["update:modelValue"]);
</script>

<style scoped></style>
