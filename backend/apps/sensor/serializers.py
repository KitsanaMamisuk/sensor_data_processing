from .models import SensorData
from model_controller.serializers import ModelControllerSerializer
from rest_framework import serializers


class SensorDataSerializer(ModelControllerSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'
