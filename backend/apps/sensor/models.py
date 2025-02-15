from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=False, db_index=True)
    temperature = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    humidity = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    air_quality = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    