from django.db import models

from .base import BaseModelAbstract


class Disco(BaseModelAbstract, models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'Discos'
