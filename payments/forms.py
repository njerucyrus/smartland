__author__ = 'hudutech'

from django import forms


class LandTransferFeeForm(forms.Form):
    phone_number = forms.CharField(max_length=10, widget=forms.NumberInput(
        attrs={'id': 'phone_number_id', 'placeholder': '07XX XXX XXX', }
    ))
    size = forms.FloatField()
    amount = forms.FloatField(disabled=True)


class LandPurchasePayment(forms.Form):
    land_size = forms.FloatField()
    amount = forms.FloatField()