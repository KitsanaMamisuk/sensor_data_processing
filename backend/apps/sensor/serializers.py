from .models import SensorData
from model_controller.serializers import ModelControllerSerializer
from rest_framework import serializers


class SensorDataSerializer(ModelControllerSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'


class SensorAggregationTimeWindowSerializer(serializers.Serializer):
    time_window = serializers.ChoiceField(choices=['10m', '1h', '24h'], required=True)


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

