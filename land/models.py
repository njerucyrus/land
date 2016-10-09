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
    title_deed_no = models.CharField(max_length=32, unique=True)
    registry_map_sheet_no = models.CharField(max_length=32, unique=True)
    approximate_size = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=128)
    district = models.CharField(max_length=128)
    is_onsale = models.BooleanField(default=True)
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





