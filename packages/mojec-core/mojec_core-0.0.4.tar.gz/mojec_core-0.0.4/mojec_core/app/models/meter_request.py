from django.db import models

from .base import BaseModelAbstract
from .disco import Disco


class MeterRequest(BaseModelAbstract, models.Model):
    disco = models.ForeignKey(Disco, models.SET_NULL,
                              blank=True, null=True)
    quantity = models.IntegerField(default=1)
    phone = models.CharField(max_length=11, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'MeterRequests'
