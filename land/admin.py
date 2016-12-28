from django.contrib import admin
from land.models import *


class LandUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id_no', 'phone_number']

    class Meta:
        model = LandUserProfile


class LandAdmin(admin.ModelAdmin):
    list_display = ['user', 'title_deed', 'location', 'size', 'on_sale', 'description']

    class Meta:
        model = Land


class LandTransfersAdmin(admin.ModelAdmin):
    list_display = [
        'title_deed',
        'new_title_deed',
        'owner',
        'transferred_to',
        'size_transferred',
        'relationship',
        'date_transferred'
    ]


admin.site.register(LandUserProfile, LandUserProfileAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(LandTransfers, LandTransfersAdmin)