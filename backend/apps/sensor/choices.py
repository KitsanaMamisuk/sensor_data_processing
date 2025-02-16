from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeWindow(models.TextChoices):
    TEN_MIN = '10m', _('10m')
    ONE_HOUR = '1h', _('1h')
    ONE_DAY = '24h', _('24h')
