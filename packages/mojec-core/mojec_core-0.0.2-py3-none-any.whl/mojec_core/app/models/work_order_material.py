from django.db import models

from .work_order import WorkOrder
from .base import BaseModelAbstract


class WorkOrderMaterial(BaseModelAbstract, models.Model):
    workOrder = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL,
                                  null=True, blank=True)
    item = models.UUIDField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    productName = models.TextField(db_column='productName', blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'WorkOrderMaterials'

