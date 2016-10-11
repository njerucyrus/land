from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# create app models ---representation of the database tables--


class LandUserProfile(models.Model):
    user = models.OneToOneField(User,)
    id_no = models.PositiveIntegerField("National ID")
    phone_number = models.CharField(max_length=13, )
    district = models.CharField(max_length=128)
    ward = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    address = models.CharField(max_length=128)

    def __unicode__(self):
        return str(self.user.username)


class Land(models.Model):
    user = models.ForeignKey(User, verbose_name="Land Owner")
    profile = models.ForeignKey(LandUserProfile, )
    title_deed_no = models.CharField(max_length=32, unique=True)
    registry_map_sheet_no = models.CharField(max_length=32, unique=True)
    approximate_size = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=128)
    district = models.CharField(max_length=128)
    is_onsale = models.BooleanField(default=True)
    bought = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title_deed_no


class LandSales(models.Model):
    land = models.ForeignKey(Land, )
    owner = models.CharField(max_length=32, )
    buyer = models.CharField(max_length=32, )
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    uncleared_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transfer_made = models.BooleanField(default=False, )
    date_deposited = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.land.title_deed_no)


class LandTransfer(models.Model):
    owner = models.ForeignKey(User, verbose_name="Owner", related_name="LandOwner")
    new_owner = models.ForeignKey(User, verbose_name="New Owner")
    old_title_deed_no = models.OneToOneField(Land, )
    new_title_deed_no = models.CharField(max_length=32)
    transfer_size = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return str(self.new_title_deed_no)


class LandTransferHistoryLog(models.Model):
    transfer_from = models.CharField(max_length=128, )
    transfer_to = models.CharField(max_length=128, )
    initial_title_deed = models.CharField(max_length=128, )
    initial_map_sheet = models.CharField(max_length=128, )
    new_map_sheet = models.CharField(max_length=128, )
    initial_title_deed = models.CharField(max_length=128, )
    new_title_deed = models.CharField(max_length=128, )
    date_transferred = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        self.initial_title_deed


class Notification(models.Model):
    sender = models.CharField(max_length=13)
    land_id = models.ForeignKey(Land, on_delete=models.DO_NOTHING)
    sent_to = models.CharField(max_length=13, default='')
    text = models.TextField(max_length=200)
    is_read = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Notifications'

    def __unicode__(self):
        return "Message From {0}".format(self.sender)





