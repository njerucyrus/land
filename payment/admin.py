from django.contrib import admin
from payment.models import LandTransferFee, Payment


class LandTransferFeeAdmin(admin.ModelAdmin):
    list_display = ['fee_amount']

    class Meta:
        model = LandTransferFee
admin.site.register(LandTransferFee, LandTransferFeeAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'transaction_id',
        'phone_number',
        'amount',
        'payment_mode',
        'status',
        'details',
        'transaction_date'
    ]

    class Meta:
        model = Payment
admin.site.register(Payment, PaymentAdmin)