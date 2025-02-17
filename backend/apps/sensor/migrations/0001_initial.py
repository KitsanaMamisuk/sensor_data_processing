# Generated by Django 5.1.6 on 2025-02-17 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('humidity', models.FloatField(blank=True, null=True)),
                ('air_quality', models.FloatField(blank=True, null=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('timestamp', 'temperature', 'humidity', 'air_quality'), name='unique_sensor_data')],
            },
        ),
    ]
