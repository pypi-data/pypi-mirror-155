from django.db import models
from .base import BaseModelAbstract


class WorkOrderService(BaseModelAbstract, models.Model):
    name = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, default='active', blank=True, 
                              null=True)

    class Meta:
        db_table = 'WorkOrderServices'


class WorkOrderServiceCategory(BaseModelAbstract, models.Model):
    service = models.ForeignKey(
        WorkOrderService, models.SET_NULL, db_column='service',
        blank=True, null=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    chargeType = models.CharField(db_column='chargeType', blank=True,
                                  null=True, max_length=30)
    commission = models.DecimalField(
        max_digits=15, decimal_places=2, default=0
    )
    serviceCharge = models.DecimalField(
        db_column='serviceCharge', max_digits=15,
        decimal_places=2, default=0
    )
    commitmentFee = models.DecimalField(
        db_column='commitmentFee', max_digits=15,
        decimal_places=2, default=0)
    status = models.CharField(max_length=30, default='active', blank=True, 
                              null=True)

    class Meta:
        db_table = 'WOServiceCategories'
