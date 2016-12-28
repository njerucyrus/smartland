__author__ = 'hudutech'

from django import forms
from django.contrib.auth.models import User
from land.models import LandUserProfile, Land, LandTransfers


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, )
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


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
        exclude = ('user', )


class LandTransferForm(forms.ModelForm):

    class Meta:
        model = LandTransfers
        exclude = ('new_title_deed', 'owner', 'date_transferred', )




