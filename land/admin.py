from django.contrib import admin
from land.models import (
    LandUserProfile,
    Land,
    ChangeLandOwnership,
    Notification,
    LandTransfer,
)


# REGISTER ALL MODELS TO ADMIN SITE

class LandUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id_no', 'district', 'ward', 'location', 'address']

    class Meta:
        model = LandUserProfile
admin.site.register(LandUserProfile, LandUserProfileAdmin)


class LandAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'title_deed_no',
        'registry_map_sheet_no',
        'approximate_size',
        'location',
        'district',
        'is_onsale',
        'bought',
        'transferred_completely',
        'remaining_size',
        'sale_price',
        'date_updated'
    ]

    class Meta:
        model = Land
admin.site.register(Land, LandAdmin)


class ChangeLandOwnershipAdmin(admin.ModelAdmin):
    list_display = [
        'owner',
        'new_owner',
        'old_title_deed_no',
        'new_title_deed_no',
        'transfer_size'
    ]

    class Meta:
        model = ChangeLandOwnership
admin.site.register(ChangeLandOwnership, ChangeLandOwnershipAdmin)


class LandTransferAdmin(admin.ModelAdmin):
    list_display = ['first_name',
                    'middle_name',
                    'last_name',
                    'id_no',
                    'district',
                    'location',
                    'sub_location',
                    'transfer_from',
                    'transfer_size',
                    'title_deed',
                    'date'
                    ]

    class Meta:
        model = LandTransfer
admin.site.register(LandTransfer, LandTransferAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'sent_to', 'text', 'date_sent', 'is_read']

    class Meta:
        model = Notification
admin.site.register(Notification, NotificationAdmin)