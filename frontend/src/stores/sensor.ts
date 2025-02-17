import { ref, onMounted } from 'vue';
import axios from 'axios';
import type { SensorData } from '@/types/sensor';


export const useSensorData = () => {
  const sensorData = ref<SensorData[]>([]); // Type the sensorData ref
  const loading = ref(false); // Add a loading state
  const error = ref<string | null>(null); // Add an error state

  const fetchData = async () => {
    loading.value = true;
    error.value = null; // Reset error on each fetch attempt
    try {
      const response = await axios.get('http://localhost:8000/sensor/processed/');
      sensorData.value = response.data;
    } catch (err) {
      console.error('Failed to fetch data:', err);
      error.value = err.message; // Store the error message
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchData);

  return { sensorData, loading, error, fetchData }; // Return data, loading, error, and the fetch function
};