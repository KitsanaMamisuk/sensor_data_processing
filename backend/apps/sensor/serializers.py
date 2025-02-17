from apps.sensor.choices import TimeWindow
from .models import SensorData
from rest_framework import serializers


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'


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
