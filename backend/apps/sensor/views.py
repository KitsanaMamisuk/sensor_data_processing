from decimal import InvalidOperation
from typing import Optional, Union
from apps.sensor.choices import TimeWindow
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework import status
from .serializers import (
    SensorDataSerializer,
    SensorAggregationTimeWindowSerializer,
    SensorAggregationDataSerializer,
    SensorProcessedDataSerializer,
)
from django.db import transaction
from .models import SensorData
from datetime import timedelta
from django.http import Http404
from django.db.models import QuerySet
import csv
import io
import pandas as pd
import numpy as np
from django.utils import timezone

class SensorDataView(APIView):
    serializer_class = SensorDataSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, 
            context={'request': request}, 
            many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SensorDataIngestView(APIView):
    serializer_class = SensorDataSerializer

    @staticmethod
    def validate_float(value) -> Optional[Union[float, None]]:
        try:
            return float(value)
        except (InvalidOperation, ValueError, TypeError):
            return None

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)

        if len(request.FILES.getlist('file', None)) > 1:
            raise ValidationError({'error': 'Please upload 1 files'})

        if not file:
            raise ValidationError({'error': 'No file uploaded.'})

        if not file.name.endswith('.csv'):
            raise ValidationError(
                {'error': 'Invalid file format. Please upload a CSV file.'}
            )

        try:
            decoded_file = file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            required_headers = {'timestamp', 'temperature', 'humidity', 'air_quality'}
            if not required_headers.issubset(reader.fieldnames):
                raise ValidationError(
                    {
                        'error': f'Missing required columns: {required_headers - set(reader.fieldnames)}'
                    }
                )

            sensor_data_list = []
            for row in reader:
                timestamp = row['timestamp']
                if not timestamp:
                    raise ValueError({'error': 'Timestamp Invalid'})
                temperature = self.validate_float(row.get('temperature'))
                humidity = self.validate_float(row.get('humidity'))
                air_quality = self.validate_float(row.get('air_quality'))
                sensor_data_list.append(
                    SensorData(
                        timestamp=timestamp,
                        temperature=temperature,
                        humidity=humidity,
                        air_quality=air_quality,
                    )
                )
            # Bulk create data with transection
            with transaction.atomic():
                SensorData.objects.bulk_create(sensor_data_list, batch_size=500)

            return Response(
                {
                    'detail': f'Sensor data ingested successfully count {len(sensor_data_list)} rows'
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            raise ValidationError({'error': f'An error occurred {e}'})


class SensorProcessedView(APIView):
    serializer_class = SensorProcessedDataSerializer

    @staticmethod
    def clean_data(queryset: QuerySet) -> pd.DataFrame:
        try:
            df = pd.DataFrame.from_records(queryset.values())

            if df.empty:
                return df

            # Remove duplicates
            df = df.drop_duplicates()

            # Handle missing values (Fill with column mean)
            df.fillna(df.mean(), inplace=True)

            return df
        except Exception as e:
            raise ValueError({'error': f'An error occurred {e}'})

    @staticmethod
    def detect_anomalies(df: pd.DataFrame, threshold=3.0) -> pd.DataFrame:
        try:
            for column in ['temperature', 'humidity', 'air_quality']:
                if column in df.columns:
                    mean = df[column].mean()
                    std = df[column].std()
                    df[f'{column}_anomaly'] = (
                        np.abs(df[column] - mean) / std
                    ) > threshold
            return df
        except Exception as e:
            raise ValueError({'error': f'An error occurred {e}'})

    def get(self, request, *args, **kwargs):
        queryset = SensorData.objects.all().order_by('timestamp')
        if not queryset.exists():
            raise Http404()
        df = self.clean_data(queryset)
        df = self.detect_anomalies(df)
        response_serializer = self.serializer_class(
            df.to_dict(orient='records'), many=True
        )

        return Response(response_serializer.data)


class SensorAggregatedView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = SensorAggregationTimeWindowSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        time_window = serializer.validated_data['time_window']

        # Map time window
        time_delta_map = {
            '10m': timedelta(minutes=10),
            '1h': timedelta(hours=1),
            '24h': timedelta(hours=24),
        }
        try:
            start_time = timezone.now() - time_delta_map[time_window]
        except (TypeError, ValueError) as e:
            raise ValueError({'error': f'An error occurred {e}'})

        # Fetch data in a single query
        data = SensorData.objects.prefetch_related('timestamp').filter(timestamp__gte=start_time).values_list(
            'temperature', 'humidity', 'air_quality'
        )
        if not data:
            raise Http404()
        # Convert to NumPy array for fast calculation
        data_array = np.array(data, dtype=np.float64)
        temperature, humidity, air_quality = (
            data_array.T
        )  # Transpose to separate columns
        response_data = {
            'time_window': time_window,
            'temperature': {
                'mean': float(np.nanmean(temperature)),
                'min': float(np.nanmin(temperature)),
                'max': float(np.nanmax(temperature)),
            },
            'humidity': {
                'mean': float(np.nanmean(humidity)),
                'min': float(np.nanmin(humidity)),
                'max': float(np.nanmax(humidity)),
            },
            'air_quality': {
                'mean': float(np.nanmean(air_quality)),
                'min': float(np.nanmin(air_quality)),
                'max': float(np.nanmax(air_quality)),
            },
        }

        output_serializer = SensorAggregationDataSerializer(response_data)
        return Response(output_serializer.data)


class TimeWindowView(APIView):
    def get(self, request, *args, **kwargs):
        data_list = [TimeWindow.TEN_MIN, TimeWindow.ONE_HOUR, TimeWindow.ONE_DAY]
        response_data = []

        for item in data_list:
            data = {
                'label': item.label,
                'value': item.value,
            }
            response_data.append(data)

        return Response(response_data)
