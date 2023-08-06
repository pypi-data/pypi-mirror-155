from django.db import models
from .user import User
from .base import BaseModelAbstract
from .work_order_service import WorkOrderService


class TransactionLog(BaseModelAbstract, models.Model):
    transactionRef = models.CharField(unique=True, max_length=255)
    paymentRef = models.CharField(db_column='paymentRef', max_length=255,
                                  blank=True, null=True)
    paymentType = models.ForeignKey("PaymentType", models.SET_NULL,
                                    blank=True, null=True)
    paymentVendor = models.ForeignKey(
        "PaymentVendor", models.SET_NULL,
        blank=True, null=True)
    service = models.ForeignKey(WorkOrderService, models.SET_NULL,
                                blank=True, null=True)
    serviceDescription = models.TextField(
        db_column='serviceDescription', blank=True, null=True)
    platform = models.CharField(max_length=30, blank=True, null=True)
    requestJson = models.JSONField(
        db_column='requestJSON', blank=True, null=True)
    responseJson = models.JSONField(
        db_column='responseJSON', blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    isPaid = models.BooleanField(default=False) 
    status = models.CharField(max_length=30, blank=True, null=True)
    vendorStatus = models.CharField(max_length=30, blank=True, null=True)
    callbackJson = models.JSONField(db_column='callbackJSON', blank=True, 
                                    null=True)  # Field name made lowercase.
    verifyJson = models.JSONField(db_column='verifyJSON', blank=True, 
                                  null=True)  # Field name made lowercase.
    webhookJson = models.JSONField(db_column='webhookJSON', blank=True, 
                                   null=True)  # Field name made lowercase.
    recipient = models.ForeignKey(User, models.SET_NULL, blank=True, 
                                  null=True, 
                                  related_name="received_transactions")
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = 'TransactionLogs'
