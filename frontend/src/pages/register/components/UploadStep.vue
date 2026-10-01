<script setup lang="ts">
import Form5Dropzone from "@/components/Form5Dropzone.vue";
import ParseLog from "@/components/ParseLog.vue";
import type { LogLine } from "@/domain/mockData";

defineProps<{
  isParsing: boolean;
  logLines: readonly LogLine[];
}>();

const emit = defineEmits<{
  accept: [file: File];
  reject: [message: string];
}>();
</script>

<template>
  <!-- The document window and the counter log ride straight in the
       DocketPanel body — the panel's ruled frame is this step's only frame,
       and the copy the old AppCard subtitle carried lives in the sidebar
       briefing and the dropzone now. No second card wraps them. -->
  <Form5Dropzone
    @accept="emit('accept', $event)"
    @reject="emit('reject', $event)"
  />
  <ParseLog :lines="logLines" />
</template>

<style scoped lang="scss">
// The document window and the counter log each carry their own rules, so this
// step needs no local styles. Kept as a scoped block anchor only if a future
// state (parse error, retry) needs to ride the slip's own margins.
</style>
