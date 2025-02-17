<script setup lang="ts">
import { ref, computed } from 'vue';
import { use } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import { useSensorData } from '@/stores/sensor';

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent]);

const { sensorData, loading, error, fetchData } = useSensorData(); // Use the composable

const chartOptions = computed(() => { // Make chartOptions a computed property
  if (!sensorData.value || sensorData.value.length === 0) {
    return {}; // Return empty object if no data
  }
  return {
    tooltip: { trigger: 'axis' },
    legend: { data: ['Temperature', 'Humidity', 'Air Quality'] },
    xAxis: { type: 'category', data: sensorData.value.map((d) => d.timestamp) },
    yAxis: { type: 'value' },
    series: [
      {
        name: 'Temperature',
        type: 'line',
        data: sensorData.value.map((d) => d.temperature),
        itemStyle: {
          color: (params) => (sensorData.value[params.dataIndex].temperature_anomaly ? 'red' : 'blue'),
        },
      },
      {
        name: 'Humidity',
        type: 'line',
        data: sensorData.value.map((d) => d.humidity),
        itemStyle: {
          color: (params) => (sensorData.value[params.dataIndex].humidity_anomaly ? 'red' : 'green'),
        },
      },
      {
        name: 'Air Quality',
        type: 'line',
        data: sensorData.value.map((d) => d.air_quality),
        itemStyle: {
          color: (params) => (sensorData.value[params.dataIndex].air_quality_anomaly ? 'red' : 'purple'),
        },
      },
    ],
  };
});


</script>

<template>
  <div style="margin: 0 0;">
    <center><h1>Sensor Data Trends</h1></center>
    <div v-if="loading">Loading...</div>
    <div v-if="error">Error: {{ error }}</div>
    <v-chart v-if="sensorData && sensorData.length > 0" class="chart" :option="chartOptions" autoresize />
    <div v-else-if="!loading && !error">No Data Available.</div>
  </div>
</template>

<style scoped>
  .chart{
    width: 1000px;
    height: 1000px;
    color: #fff;
  }
</style>