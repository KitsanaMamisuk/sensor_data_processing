export interface SensorData {
    timestamp: string;
    temperature: number;
    humidity: number;
    air_quality: number;
    temperature_anomaly: boolean;
    humidity_anomaly: boolean;
    air_quality_anomaly: boolean;
  }
  