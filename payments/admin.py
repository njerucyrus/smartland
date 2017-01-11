from django.contrib import admin

from payments.models import (
    LandPurchasePayment,
    LandTransferFee,
    LandTransferPayment
)


class LandTransferFeeAdmin(admin.ModelAdmin):
    list_display = ['land_size', 'fee_charged']

    class Meta:
        model = LandTransferFee

admin.site.register(LandTransferFee, LandTransferFeeAdmin)


class LandTransferPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id',
        'title_deed',
        'transferred_size',
        'phone_number',
        'payment_mode',
        'amount',
        'status',
        'date'
    ]

    class Meta:
        model = LandTransferPayment

admin.site.register(LandTransferPayment, LandTransferPaymentAdmin)


class LandPurchasePaymentAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id',
        'title_deed',
        'purchased_size',
        'payment_mode',
        'buyer_email',
        'amount',
        'status',
        'date'
    ]

    class Meta:
        model = LandPurchasePayment

admin.site.register(LandPurchasePayment, LandPurchasePaymentAdmin)

