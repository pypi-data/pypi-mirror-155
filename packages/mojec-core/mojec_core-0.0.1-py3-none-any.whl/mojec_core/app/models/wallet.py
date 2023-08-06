from django.db import models

from .base import BaseModelAbstract
from .user import User


class Wallet(BaseModelAbstract, models.Model):
    createdBy = None
    recipientCode = models.CharField(
        db_column='recipientCode', max_length=255, blank=True, null=True)
    recipient = models.JSONField(blank=True, null=True)
    user = models.OneToOneField(User, models.CASCADE, null=False, 
                                blank=False, related_name="wallet")
    name = models.CharField(max_length=255, blank=True, null=True)
    balance = models.DecimalField(default=0, max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'Wallets'


class WalletHistory(BaseModelAbstract, models.Model):
    wallet = models.ForeignKey(Wallet, models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    requestJson = models.JSONField(db_column='requestJSON', blank=True,
                                   null=True)
    transferCode = models.CharField(db_column='transferCode',
                                    max_length=255, blank=True, null=True)
    isCompleted = models.BooleanField(db_column='isCompleted', default=False)

    class Meta:
        db_table = 'WalletHistories'

