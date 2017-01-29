from django.shortcuts import render, render_to_response, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import Q

from land.forms import (
    UserRegistrationForm,
    LandUserProfileForm,
    LandRegistrationForm,
    LandTransferForm,
    LandPurchaseForm,
    SearchLandForm,
    ContactForm,
)
from land.models import (
    LandUserProfile,
    Land,
    LandTransfers,
    LandPurchases,
    ContactUs,
    Notification,
)

from payments.models import LandTransferPayment

from land.phoneNumber import CleanPhoneNumber

from random import randint


@require_http_methods(['POST', 'GET'])
def login_user(request):
    next_url = request.GET.get('next', '')
    #check if user is authenticated and redirect user to root page
    if request.user.is_authenticated():
            return HttpResponseRedirect('/index/')

    # if not request.user.is_authenticated():
    #         return HttpResponseRedirect('/login/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print 'username', username
        print 'password', password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                if next_url == '':
                    return HttpResponseRedirect('/index/')
                elif next_url:
                    return HttpResponseRedirect(next_url)
        else:
            err_message = 'Wrong username / password'
            return render(request, 'land/login.html', {'err_message': err_message, })
    else:
        return render(request, 'land/login.html', )


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


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
            clean_phone_number = CleanPhoneNumber(phone_number).validate_phone_number()
            profile = LandUserProfile.objects.create(
                user=user,
                id_no=id_no,
                phone_number=clean_phone_number
            )
            profile.save()
            success_message = 'Account created successfully'
            return render(request, 'land/signup.html', {'success_message': success_message})
    else:
        signup_form = UserRegistrationForm()
        profile_form = LandUserProfileForm()
    return render(request, 'land/signup.html',
                  {
                      'signup_form': signup_form,
                      'profile_form': profile_form
                  })


@login_required(login_url='/login/')
def my_profile(request):

    profile = get_object_or_404(
        LandUserProfile,
        user=get_object_or_404(User, username=request.user)
    )
    return render(request, 'land/myprofile.html', {'profile': profile, })


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
            land_value = cd['land_value']
            map_sheet = cd['map_sheet']
            land_obj = Land.objects.create(
                user=profile,
                title_deed=title_deed,
                location=location,
                map_sheet=map_sheet,
                size=size,
                photo=photo,
                description=description,
                on_sale=on_sale,
                land_value=land_value
            )
            land_obj.save()
            success_message = 'Land registered successfully'
            return render(request, 'land/register_land.html', {'success_message': success_message})
    else:
        land_form = LandRegistrationForm()
    return render(request, 'land/register_land.html', {'land_form': land_form, })

@login_required(login_url='/login/')
def transfer_land(request, pk=None):
    land = get_object_or_404(Land, pk=pk)
    title_deed = str(land.title_deed)
    initial = {'title_deed': title_deed, }
    if request.method == 'POST':

        transfer_form = LandTransferForm(request.POST, initial=initial)
        if transfer_form.is_valid():
            cd = transfer_form.cleaned_data
            size_transferred = cd['transfer_size']
            relationship = cd['relationship']
            transfer_to = cd['transfer_to']

            range_start = 10 ** (10 - 1)
            range_end = (10 ** 10) - 1
            new_title_deed = randint(range_start, range_end)

            user = get_object_or_404(User, username=request.user)
            profile = get_object_or_404(LandUserProfile, user=user)
            try:

                payment = LandTransferPayment.objects.get(title_deed=title_deed, transferred_size=size_transferred)
                if payment.status == 'Success':
                    land_transfer_obj = LandTransfers.objects.create(
                        title_deed=land,
                        new_title_deed=new_title_deed,
                        owner=profile,
                        transfer_to=transfer_to,
                        size_transferred=size_transferred,
                        relationship=relationship
                    )
                    land_transfer_obj.save()
                    success_message = 'Land Transferred Successfully!'
                    return render(request, 'land/transfer_land.html',
                                  {'success_message': success_message})

                else:
                    return HttpResponse('Please make the payment first')
            except LandTransferPayment.DoesNotExist:
                return HttpResponse('Please make the payment first')

    else:
        transfer_form = LandTransferForm()
    return render(request, 'land/transfer_land.html', {'transfer_form': transfer_form, })


@login_required(login_url='/login/')
def my_land_list(request):
    user = get_object_or_404(User, username=request.user)
    profile = get_object_or_404(LandUserProfile, user=user)
    lands = Land.objects.filter(user=profile, purchased=False)

    return render(request, 'land/my_land_list.html', {'lands': lands}, )


def land_details(request, title_deed=None):
    try:
        land = Land.objects.get(title_deed=title_deed)
        return render(request, 'land/land_details.html', {'land': land, })
    except Land.DoesNotExist:
        message = 'No land that matches the supplied title deed'
        return render(request, 'land/land_details.html', {'error': message})


@login_required(login_url='/login/')
def land_on_sale(request):
    user = get_object_or_404(LandUserProfile, user=get_object_or_404(User, username=str(request.user)))
    lands = Land.objects.filter(on_sale=True).exclude(Q(user=user))
    return render(request, 'land/lands_onsale.html', {'lands': lands, })


@login_required(login_url='/login/')
def purchase_land(request, pk=None):
    land = get_object_or_404(Land, pk=pk)
    deposit = float(land.land_value) * 0.75
    title_deed = land.title_deed
    initial = {'deposit': deposit, 'title_deed': title_deed}

    if request.method == 'POST':
        purchase_form = LandPurchaseForm(request.POST, initial=initial)

        if purchase_form.is_valid():

            cd = purchase_form.cleaned_data
            phone_number = cd['phone_number']
            email = cd['email']
            deposit = cd['deposit']
            user = get_object_or_404(User, username=request.user)
            buyer = get_object_or_404(LandUserProfile, user=user)
            clean_phone_number = CleanPhoneNumber(phone_number).validate_phone_number()
            # set session variables
            request.session['buyer_phone_number'] = clean_phone_number
            request.session['buyer_email'] = email
            request.session['deposit_amount'] = float(deposit)
            request.session['buyer_username'] = str(request.user)
            request.session['seller_username'] = str(land.user.user.username)
            request.session['title_deed'] = str(land.title_deed)

            return HttpResponseRedirect('/land-purchase-payment/')
            # try:
            #     land_purchase = LandPurchases.objects.create(
            #         owner=land.user.user,
            #         land=land,
            #         buyer=buyer,
            #         email=email,
            #         phone_number=clean_phone_number,
            #         deposit=deposit,
            #     )
            #
            #     land_purchase.save()
            #     land.on_sale = False
            #     land.save()
            # except IntegrityError, e:
            #     error_msg = 'Land Already Purchased by another user', e
            #     return render_to_response(
            #         'land/purchase_land.html',
            #         {'error': error_msg, }
            #     )
            # # send notification to the land owner
            # message = 'The Land with title deed({0}), has been purchased by {1} on {2}, a deposit of Ksh ' \
            #           '{3} has been sent into your Paypal account.The buyers Phone number is {4}'.\
            #     format(title_deed, request.user,  timezone.now(), deposit,  clean_phone_number)
            #
            # notification = Notification.objects.create(
            #     user=land.user.user,
            #     message_from=str(request.user),
            #     message=message,
            # )
            # notification.save()
            #
            # success_message = 'You have successfully purchased the land title deed {0}'. \
            #     format(land.title_deed)

    else:
        purchase_form = LandPurchaseForm(initial=initial)
    return render(request, 'land/purchase_land.html', {
        'purchase_form': purchase_form
    })


@login_required(login_url='/login/')
def lands_bought(request):
    user = get_object_or_404(User, username=request.user)
    lands = LandPurchases.objects.filter(owner=user)
    return render(request, 'land/lands_bought.html', {'lands_bought': lands})


def index(request):
    return render(request, 'index.html', {})


def contact_us(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            cd = contact_form.cleaned_data
            first_name = cd['first_name']
            last_name = cd['last_name']
            email = cd['email']
            phone_number = cd['phone_number']
            message = cd['message']
            clean_phone_number = CleanPhoneNumber(phone_number).validate_phone_number()

            contact = ContactUs.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=clean_phone_number,
                message=message
            )
            contact.save()
            success_message = 'Message Sent Successfully'
            return render(request, 'land/contactus.html', {'success_message': success_message})

    else:
        contact_form = ContactForm()
    return render(request, 'land/contactus.html', {'contact_form': contact_form, })


@login_required(login_url='/login/')
def get_notification(request, user):
    user = get_object_or_404(User, username=user)
    notification = Notification.objects.filter(user=user).order_by('date')
    return render(request, 'land/notification.html', {'notification': notification, })


@login_required(login_url='/login/')
def approve_purchased_land(request, title_deed):
    land_obj = get_object_or_404(Land, title_deed=title_deed)
    land = get_object_or_404(LandPurchases, land=land_obj)
    land.approved = True
    land.rejected = False
    land.save()
    message = 'Land Purchase approved successfully'

    # send sms to the buyer to notify him land was approved --pending

    return render(request, 'land/approve_success.html', {'success_message': message, })


@login_required(login_url='/login/')
def reject_purchased_land(request, title_deed):
    land_obj = get_object_or_404(Land, title_deed=title_deed)
    land = get_object_or_404(LandPurchases, land=land_obj)
    land.rejected = True
    land.approved = False
    land.save()
    message = 'Land Purchase rejected'

    # send sms to the buyer to notify him land was approved --pending

    return render(request, 'land/reject_success.html', {'success_message': message, })


@login_required(login_url='/login/')
def search_land_onsale(request):
    if request.method == 'POST':
        search_form = SearchLandForm(request.POST, )
        if search_form.is_valid():
            cd = search_form.cleaned_data
            min_price = cd['minimum_price']
            max_price = cd['maximum_price']
            location = cd['land_location']
            land_size = cd['land_size']

            lands = Land.objects.filter(
                land_value__range=(min_price, max_price),
                location=location, size=land_size, on_sale=True
            )
            return render(request, 'land/search_land_onsale.html', {'lands': lands, })
    else:
        return render(request, 'land/search_land_onsale.html', {'search_form': SearchLandForm(), })


