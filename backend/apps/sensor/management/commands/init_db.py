import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.sensor.models import SensorData


class Command(BaseCommand):
    help = 'Imports sensor data from a CSV file into the SensorData model.'

    def handle(self, *args, **options):
        csv_file_path = os.path.join(os.path.dirname(__file__), 'sensor_data.csv')

        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.DictReader(file)
                sensor_objects = []

                for row in reader:
                    temperature = row['temperature'] if row['temperature'] else None
                    humidity = row['humidity'] if row['humidity'] else None
                    air_quality = row['air_quality'] if row['air_quality'] else None

                    sensor_objects.append(
                        SensorData(
                            timestamp=row['timestamp'],
                            temperature=temperature,
                            humidity=humidity,
                            air_quality=air_quality,
                        )
                    )

                with transaction.atomic():
                    SensorData.objects.bulk_create(sensor_objects)

            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported data from {csv_file_path}')
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.WARNING(f'Error: CSV file not found at {csv_file_path}')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
