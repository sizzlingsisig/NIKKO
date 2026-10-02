<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import MainLayout from "@/layouts/MainLayout.vue";

const route = useRoute();

// Pages render inside MainLayout unless they opt out with meta: { layout: false }
const layout = computed(() =>
  route.meta.layout === false ? "div" : MainLayout
);
</script>
