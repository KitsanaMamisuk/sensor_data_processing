from django.db import models


class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=False, db_index=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    air_quality = models.FloatField(null=True, blank=True)
