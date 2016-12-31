__author__ = 'hudutech'

from django import forms


class LandTransferFeeForm(forms.Form):
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(
        attrs={'id': 'phone_number_id', }
    ))
    size = forms.FloatField()
    amount = forms.FloatField()


class LandPurchasePayment(forms.Form):
    land_size = forms.FloatField()
    amount = forms.FloatField()