from django.db import models

from .user_address import UserAddress
from .base import BaseModelAbstract
from .user import User
from .work_order_service import WorkOrderServiceCategory


class WorkOrder(BaseModelAbstract, models.Model):
    serviceSubCategory = models.ForeignKey(
        WorkOrderServiceCategory, models.SET_NULL,
        db_column='serviceSubCategory', blank=True, null=True)
    address = models.ForeignKey(UserAddress, models.SET_NULL, blank=True, 
                                null=True)
    agent = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, 
                              related_name="workorders_agent_set")
    description = models.TextField(blank=True, null=True)
    orderId = models.CharField(db_column='orderId', max_length=30,
                               blank=False, null=False)
    assessmentReport = models.TextField(
        db_column='assessmentReport', blank=True, null=True)
    completionReport = models.TextField(
        db_column='completionReport', blank=True, null=True)
    transactionReference = models.TextField(
        db_column='transactionReference', blank=True, null=True, 
        max_length=255
    )
    generalStatus = models.CharField(db_column='generalStatus', default='new',
                                     max_length=30)
    currentStatus = models.CharField(db_column='currentStatus',
                                     default='unPaid', max_length=30)
    noteForAgent = models.TextField(db_column='noteForAgent', blank=True,
                                    null=True)
    additionalNote = models.TextField(db_column='additionalNote',
                                      blank=True, null=True)
    date = models.DateTimeField(blank=False, null=False)
    fee = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    totalAmount = models.DecimalField(db_column='totalAmount',
                                      max_digits=15, decimal_places=2,
                                      default=0)
    actualServiceCharge = models.DecimalField(
        db_column='actualServiceCharge', max_digits=15, decimal_places=2,
        default=0)
    remainingServiceCharge = models.DecimalField(
        db_column='remainingServiceCharge', max_digits=15, decimal_places=2,
        default=0)
    remainingtotalAmount = models.DecimalField(
        db_column='remainingtotalAmount', max_digits=15, decimal_places=2,
        default=0)
    totalMaterialsFee = models.DecimalField(db_column='totalMaterialsFee',
                                            max_digits=15, decimal_places=2,
                                            default=0)
    isCommitmentFeePaid = models.BooleanField(db_column='isCommitmentFeePaid',
                                              blank=True, null=True)
    agentEnroute = models.BooleanField(db_column='agentEnroute',
                                       blank=True, null=True)
    agentArrived = models.BooleanField(db_column='agentArrived',
                                       blank=True, null=True)
    isAssessmentCompleted = models.BooleanField(
        db_column='isAssessmentCompleted', blank=True, null=True
    )
    paymentCompleted = models.BooleanField(db_column='paymentCompleted',
                                           blank=True, null=True)
    jobStartedAt = models.DateTimeField(db_column='jobStartedAt',
                                        blank=True, null=True)
    jobCompletedAt = models.DateTimeField(db_column='jobCompletedAt',
                                          blank=True, null=True)
    isAgentJobComplete = models.BooleanField(db_column='isAgentJobComplete',
                                             blank=True, null=True)
    customerCompletionConfirmation = models.BooleanField(
        db_column='customerCompletionConfirmation', blank=True, null=True)
    isAgentReview = models.BooleanField(db_column='isAgentReview',
                                        default=False)
    isCustomerReview = models.BooleanField(
        db_column='isCustomerReview', default=False
    )
    paymentJson = models.JSONField(db_column='paymentJson',
                                   blank=True, null=True)
    agentEnrouteAt = models.DateTimeField(db_column='agentEnrouteAt',
                                          blank=True, null=True)
    agentArrivedAt = models.DateTimeField(db_column='agentArrivedAt',
                                          blank=True, null=True)

    class Meta:
        db_table = 'WorkOrders'
