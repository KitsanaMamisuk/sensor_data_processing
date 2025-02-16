from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.sensor.views import SensorDataIngestView, SensorProcessedView, SensorAggregatedView


router = DefaultRouter()

app_name = 'api_urls'



urlpatterns = [
    path('data/', SensorDataIngestView.as_view(), name='sensor-data-ingest'),
    path('processed/', SensorProcessedView.as_view(), name='sensor-processed'),
    path('aggregated/', SensorAggregatedView.as_view(), name='sensor-aggregated'),
]
urlpatterns += router.urls