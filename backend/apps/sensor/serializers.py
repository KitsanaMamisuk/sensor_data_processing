from apps.sensor.choices import TimeWindow
from .models import SensorData
from rest_framework import serializers
from apps.sensor.utils import validate_float


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

    def validate_temperature(self, temperature):
        temperature = validate_float(temperature)
        return temperature
    
    def validate_humidity(self, humidity):
        humidity = validate_float(humidity)
        return humidity
    
    def validate_air_quality(self, air_quality):
        air_quality = validate_float(air_quality)
        return air_quality

class SensorAggregationTimeWindowSerializer(serializers.Serializer):
    time_window = serializers.ChoiceField(choices=TimeWindow.choices, required=True)


class SensorAggregationDataSerializer(serializers.Serializer):
    time_window = serializers.CharField()
    temperature = serializers.DictField()
    humidity = serializers.DictField()
    air_quality = serializers.DictField()


class SensorProcessedDataSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    temperature = serializers.FloatField()
    humidity = serializers.FloatField()
    air_quality = serializers.FloatField()
    temperature_anomaly = serializers.BooleanField()
    humidity_anomaly = serializers.BooleanField()
    air_quality_anomaly = serializers.BooleanField()
