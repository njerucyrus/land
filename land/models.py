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
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title_deed_no


class LandTransfer(models.Model):
    owner = models.ForeignKey(User, verbose_name="Owner", related_name="LandOwner")
    new_owner = models.ForeignKey(User, verbose_name="New Owner")
    old_title_deed_no = models.OneToOneField(Land, )
    new_title_deed_no = models.CharField(max_length=32)
    transfer_size = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return str(self.new_title_deed_no)


class Notification(models.Model):
    sender = models.CharField(max_length=13)
    sent_to = models.CharField(max_length=13, default='')
    text = models.TextField(max_length=200)
    is_read = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Notifications'

    def __unicode__(self):
        return "Message From {0}".format(self.sender)





