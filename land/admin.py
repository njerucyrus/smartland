from django.contrib import admin
from land.models import *


class LandUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id_no', 'phone_number']

    class Meta:
        model = LandUserProfile


class LandAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'title_deed',
        'map_sheet',
        'location',
        'size',
        'land_value',
        'on_sale',
        'photo',
        'description',
        'fee_paid',
        'purchased',
    ]

    class Meta:
        model = Land


class LandTransfersAdmin(admin.ModelAdmin):
    list_display = [
        'title_deed',
        'new_title_deed',
        'owner',
        'transfer_to',
        'size_transferred',
        'relationship',
        'date_transferred'
    ]

    class Meta:
        model = LandTransfers


class LandPurchasesAdmin(admin.ModelAdmin):
    list_display = [
        'land',
        'owner',
        'buyer',
        'deposit',
        'phone_number',
        'email',
        'paid',
        'approved',
        'rejected',
        'date'
    ]

    class Meta:
        model = LandPurchases


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'email', 'message']

    class Meta:
        model = ContactUs


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_from', 'message', 'read', 'date']

    class Meta:
        model = Notification


admin.site.register(LandUserProfile, LandUserProfileAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(LandTransfers, LandTransfersAdmin)
admin.site.register(LandPurchases, LandPurchasesAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Notification, NotificationAdmin)

