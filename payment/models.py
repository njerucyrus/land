from __future__ import unicode_literals

from django.db import models


class LandTransferFee(models.Model):
    fee_amount = models.DecimalField("Transaction Fee: (Ksh)", max_digits=10, decimal_places=2)

    def __unicode__(self):
        return str(self.fee_amount)


class Payment(models.Model):
    transaction_id = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=13)
    payment_mode = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=32)
    transaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Payments'

    def __unicode__(self):
        return self.transaction_id


