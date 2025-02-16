from decimal import InvalidOperation
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from rest_framework import status
from .serializers import SensorDataSerializer, SensorAggregationTimeWindowSerializer, SensorAggregationDataSerializer, SensorProcessedDataSerializer
from django.db import transaction
from .models import SensorData
from datetime import timedelta
from django.http import Http404
import csv
import io
import pandas as pd
import numpy as np


class SensorDataIngestView(APIView):
    serializer_class = SensorDataSerializer

    @staticmethod
    def validate_float(value):
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
