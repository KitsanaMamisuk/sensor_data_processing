import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";

// ✅ เพิ่ม Vue-ECharts และลงทะเบียน Renderer
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers"; // Renderer ที่ต้องใช้
import { LineChart } from "echarts/charts"; // ประเภทของกราฟที่ใช้
import { GridComponent, TooltipComponent, LegendComponent } from "echarts/components";
import VChart from "vue-echarts"; // Vue-ECharts component

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent]); // ✅ ลงทะเบียน Renderer & Components

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.component("VChart", VChart); // ✅ ลงทะเบียน VChart เป็น component ทั่วไป

app.mount("#app");
