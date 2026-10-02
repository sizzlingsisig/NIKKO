import { createPinia } from "pinia";

/**
 * Quasar convention: `src/stores/index.ts` is the Pinia *instance factory*
 * (consumed by @quasar/app-vite's generated `entry/app.js`). Feature stores
 * live in their own modules alongside this file.
 */
export default () => createPinia();
