from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from land.forms import (
    LoginForm,
    UserRegistrationForm,
    LandUserProfileForm,
    LandRegistrationForm,
    LandTransferForm,
)
from land.models import LandUserProfile, Land, LandTransfers

from random import randint


def login_user(request):
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)

                    if next_url == '':
                        return HttpResponseRedirect('/')
                    elif next_url:
                        return HttpResponseRedirect(next_url)
            else:
                err_message = 'wrong username / password'

                login_form = LoginForm()
                return render(request,
                              'land_app_templates/login.html',
                              {'form': login_form, 'message': err_message, }
                              )
    else:
        login_form = LoginForm()
    return render(request, 'land_app_templates/login.html', {'login_form': login_form, })


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')



@login_required(login_url='/login/')
def signup(request):
    if request.method == 'POST':
        signup_form = UserRegistrationForm(request.POST)
        profile_form = LandUserProfileForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(signup_form.cleaned_data['password2'])
            user.save()
            data = profile_form.cleaned_data
            id_no = data['id_no']
            phone_number = data['phone_number']
            profile = LandUserProfile.objects.create(
                user=user,
                id_no=id_no,
                phone_number=phone_number
            )
            profile.save()
            success_message = 'Account created successfully'
            return render(request, 'land_app_templates/signup.html', {'success_message': success_message})
    else:
        signup_form = UserRegistrationForm()
        profile_form = LandUserProfileForm()
    return render(request, 'land_app_templates/signup.html',
                  {
                      'signup_form': signup_form,
                      'profile_form': profile_form
                  })


@login_required(login_url='/login/')
def register_land(request):
    user = get_object_or_404(User, username=request.user)
    profile = get_object_or_404(LandUserProfile, user=user)
    if request.method == 'POST':
        land_form = LandRegistrationForm(request.POST, request.FILES)
        if land_form.is_valid():
            cd = land_form.cleaned_data
            title_deed = cd['title_deed']
            location = cd['location']
            size = cd['size']
            photo = cd['photo']
            description = cd['description']
            on_sale = cd['on_sale']
            land_obj = Land.objects.create(
                user=profile,
                title_deed=title_deed,
                location=location,
                size=size,
                photo=photo,
                description=description,
                on_sale=on_sale
            )
            land_obj.save()
            success_message = 'Land registered successfully'
            return render(request, 'land_app_templates/register_land.html', {'success_message': success_message})
    else:
        land_form = LandRegistrationForm()
    return render(request, 'land_app_templates/register_land.html', {'land_form': land_form, })


def transfer_land(request, pk=None):
    land = get_object_or_404(Land, pk=pk)

    initial = {'title_deed': land}
    if request.method == 'POST':
        transfer_form = LandTransferForm(request.POST, initial=initial)
        if transfer_form.is_valid():
            cd = transfer_form.cleaned_data
            size_transferred = cd['size_transferred']
            relationship = cd['relationship']
            id_no = cd['transferred_to']
            profile = get_object_or_404(LandUserProfile, id_no=id_no)

            user = get_object_or_404(User, username=request.user)
            owner_profile = get_object_or_404(LandUserProfile, user=user)
            other_profile = get_object_or_404(LandUserProfile, user=profile.user)

            range_start = 10 ** (10 - 1)
            range_end = (10 ** 10) - 1
            new_title_deed = randint(range_start, range_end)

            land_transfer_obj = LandTransfers.objects.create(
                title_deed=land,
                new_title_deed=new_title_deed,
                owner=owner_profile,
                transferred_to=other_profile,
                size_transferred=size_transferred,
                relationship=relationship
            )
            land_transfer_obj.save()













