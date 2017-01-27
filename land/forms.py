__author__ = 'hudutech'

from django import forms
from django.contrib.auth.models import User
from land.models import LandUserProfile, Land, LandTransfers


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=32, )
#     password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LandUserProfileForm(forms.ModelForm):

    class Meta:
        model = LandUserProfile
        exclude = ('user', )


class LandRegistrationForm(forms.ModelForm):

    class Meta:
        model = Land
        exclude = ('user', 'purchased', 'fee_paid', )


class LandTransferForm(forms.Form):
    title_deed = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'title_deed_id', }
    ),)

    transfer_to = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'transfer_to_id', }
    ), label='Transfer_to(Username)')

    relationship = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'relationship_id', 'placeholder': 'Enter relationship eg(brother, son, daughter)'}
    ))

    transfer_size = forms.FloatField()


class LandPurchaseForm(forms.Form):
    title_deed = forms.CharField(max_length=32, disabled=True)
    phone_number = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'placeholder': '07XX XXX XXX'}
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your Paypal Email Address'}
    ))
    deposit = forms.DecimalField(max_digits=10, decimal_places=2, disabled=True)


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    phone_number = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'id': 'phone_number_id', 'placeholder': '07 XX XXX XXX'}
    ))
    email = forms.EmailField()
    message = forms.CharField(max_length=140, widget=forms.Textarea(
        attrs={'id': 'message_id', 'placeholder': 'Your message here ....'}
    ))


class SearchLandForm(forms.Form):
    minimum_price = forms.FloatField(widget=forms.NumberInput(
        attrs={'id': 'minimum_price_id',  'placeholder': 'Enter minimum price'},
    ))
    maximum_price = forms.FloatField(widget=forms.NumberInput(
        attrs={'id': 'maximum_price_id',  'placeholder': 'Enter maximum price'},
    ))
    land_size = forms.FloatField(widget=forms.NumberInput(
        attrs={'id': 'land_size_id', 'placeholder': 'Enter Land Size', }
    ))

    land_location = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'id': 'land_location_id', 'placeholder': 'Enter location to search', }
    ))



