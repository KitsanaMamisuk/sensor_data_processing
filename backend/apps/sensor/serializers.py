from .models import SensorData
from model_controller.serializers import ModelControllerSerializer
from rest_framework import serializers


class SensorDataSerializer(ModelControllerSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'
class SensorProcessedDataSerializer(serializers.Serializer):    timestamp = serializers.DateTimeField()    temperature = serializers.FloatField()    humidity = serializers.FloatField()    air_quality = serializers.FloatField()    temperature_anomaly = serializers.BooleanField()    humidity_anomaly = serializers.BooleanField()    air_quality_anomaly = serializers.BooleanField()