from django.db import models


class SensorData(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    air_quality = models.FloatField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['timestamp', 'temperature', 'humidity', 'air_quality'], name='unique_sensor_data')
        ]
        
    def __str__(self):
        return self.timestamp