from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.sensor.views import SensorDataView, SensorDataIngestView, SensorProcessedView, SensorAggregatedView


router = DefaultRouter()

app_name = 'api_urls'



urlpatterns = [
    path('data/', SensorDataView.as_view(), name='sensor-data-ingest'),
    path('processed/', SensorProcessedView.as_view(), name='sensor-processed'),
    path('aggregated/', SensorAggregatedView.as_view(), name='sensor-aggregated'),
    path('upload-file/', SensorDataIngestView.as_view(), name='upload-file'),
    
]
urlpatterns += router.urls