from django.shortcuts import render, get_object_or_404, HttpResponse, render_to_response
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from land.models import Land, LandUserProfile, LandPurchases, Notification
from payments.forms import LandTransferFeeForm

from django.utils import timezone
from django.db import IntegrityError
from land.forms import LandPurchaseForm
from payments.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from payments.models import LandTransferPayment, LandTransferFee, LandPurchasePayment
from land.phoneNumber import CleanPhoneNumber
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
import json
import hashlib
import random


def land_transfer_payment(request, pk=None):
    land = get_object_or_404(Land, pk=pk)
    title_deed = land.title_deed
    transfer_fee_amt = LandTransferFee.objects.all()[0]
    fee = float(transfer_fee_amt.fee_charged)
    form_initial = {'amount': fee, }
    if request.method == 'POST':
        payment_form = LandTransferFeeForm(request.POST, initial=form_initial)

        if payment_form.is_valid():
            cd = payment_form.cleaned_data
            phone_number = CleanPhoneNumber(cd['phone_number']).validate_phone_number()
            amount = float(cd['amount'])
            size = float(cd['size'])

            # create checkout here
            try:
                username = settings.USERNAME
                api_key = settings.API_KEY
                product_name = settings.PRODUCT_NAME
                currency_code = settings.CURRENCY_CODE
                metadata = {'shop_id': '555', 'item_id': 'land_fee'}

                """  this code will be inactive in production """
                if settings.SAND_BOX:
                    gateway = AfricasTalkingGateway(username, api_key, "sandbox")
                    transaction_id = gateway.initiateMobilePaymentCheckout(
                        product_name,
                        phone_number,
                        currency_code,
                        amount,
                        metadata
                    )

                    payment = LandTransferPayment.objects.create(
                        transaction_id=transaction_id,
                        title_deed=title_deed,
                        transferred_size=size,
                        phone_number=phone_number,
                        payment_mode='Mpesa',
                        amount=amount,
                    )
                    payment.save()
                    land.fee_paid = True
                    land.save()

                    success_message = 'Payment Initiated successfully Check your phone to complete the payment'
                    return render(request, 'payments/transfer_payment.html',
                                  {'success_message': success_message}, )

                    """ end of sandbox checkout code """
                else:
                    gateway = AfricasTalkingGateway(username, api_key)
                    transaction_id = gateway.initiateMobilePaymentCheckout(
                        product_name,
                        phone_number,
                        currency_code,
                        amount,
                        metadata
                    )
                    # create payment model instance
                    payment = LandTransferPayment.objects.create(
                        transaction_id=transaction_id,
                        title_deed=title_deed,
                        transferred_size=size,
                        phone_number=phone_number,
                        payment_mode='Mpesa',
                        amount=amount,
                    )
                    payment.save()
                    land.fee_paid = False
                    land.save()
                    success_message = 'Payment Initiated successfully Check your phone to complete the payment'
                    return render(request, 'payments/transfer_payment.html',
                                  {'success_message': success_message}, )

            except AfricasTalkingGatewayException, e:
                err_message = 'Error occurred please try again later'
                print str(e)

                return render(request,
                              'payments/transfer_payment.html',
                              {'err_message': err_message}, )
    else:
        payment_form = LandTransferFeeForm(initial=form_initial)
    return render(
        request,
        'payments/transfer_payment.html',
        {'payment_form': payment_form}
    )


@require_http_methods(['POST'])
@csrf_exempt
def mpesa_notification_callback(request):
    try:
        data = json.loads(request.body)
        transaction_id = data['transactionId']
        status = data['status']
        category = data['category']
        provider = data['provider']
        shop_id = data['requestMetadata']['shop_id']
        item_id = data['requestMetadata']['item_id']

        phone_number = CleanPhoneNumber(data['source']).validate_phone_number()
        amount = data['value']

        if status == 'Success' and category == 'MobileCheckout':
            if shop_id == '555' and item_id == 'land_fee':
                payment = get_object_or_404(LandTransferPayment, transaction_id=transaction_id)
                payment.status = status
                payment.payment_mode = provider
                payment.save()
                land = get_object_or_404(Land, title_deed=payment.title_deed)
                land.fee_paid = True
                land.save()
                username = settings.USERNAME
                api_key = settings.API_KEY
                if settings.SAND_BOX:
                    # send confirmation message
                    gateway = AfricasTalkingGateway(username, api_key, 'sandbox')
                    message = "Land Transfer fee of {0} has been " \
                              "received you can now transfer your land." \
                              " Thank you for using SmartLand".format(amount, )
                    gateway.sendMessage(phone_number, message)

                else:
                    gateway = AfricasTalkingGateway(username, api_key)
                    message = "Land Transfer fee of KSH {0} has been " \
                              "received you can now transfer your land." \
                              " Thank you for using SmartLand".format(amount, )
                    gateway.sendMessage(phone_number, message)

                return HttpResponse('transaction completed successfully')

            elif shop_id == '556' and item_id == 'land_purchase':
                land_purchase_payment = get_object_or_404(LandPurchasePayment, transaction_id=transaction_id)
                land_purchase_payment.status = status
                land_purchase_payment.save()
                land = get_object_or_404(Land, title_deed=land_purchase_payment.title_deed)
                land_purchase = get_object_or_404(LandPurchases, land=land)
                land_purchase.paid = True
                land_purchase.save()

                land.on_sale = False
                land.purchased = True
                land.save()
                # #send notification to the land owner
                message = "Someone has just purchased your land by placing a deposit of {0}, buyers info is" \
                          "Email {1} PhoneNumber {2}".format(amount, land_purchase_payment.buyer_email, phone_number)

                notification = Notification.objects.create(
                    user=land.user.user,
                    message_from=str(request.user),
                    message=message,
                )
                notification.save()
                return HttpResponse('Transaction completed successfully')

        else:
            return HttpResponse('error occurred transaction not completed')

    except (KeyError, AfricasTalkingGatewayException) as e:
        print 'error occurred', str(e)
        return HttpResponse('error occurred transaction not completed', str(e))


@login_required(login_url='/login/')
@require_http_methods(['GET'])
def transaction_history(request):
    profile = get_object_or_404(
        LandUserProfile,
        user=User.objects.get(username=str(request.user))
    )

    transfer_payments = LandTransferPayment.objects.filter(
        phone_number=str(profile.phone_number),
        status='Success'
    )
    return render(
        request,
        'payments/transfer_payments_history.html',
        {'payments': transfer_payments, }
    )



@csrf_exempt
def land_payment_process(request):
    title_deed = request.session.get('title_deed')
    land = get_object_or_404(Land, title_deed=title_deed)
    buyer_username = request.session.get('buyer_username')
    seller_username = request.session.get('seller_username')
    buyer = get_object_or_404(
        LandUserProfile,
        user=get_object_or_404(User, username=buyer_username)
    )

    seller = get_object_or_404(
        LandUserProfile,
        user=get_object_or_404(User, username=seller_username)
    )
    amount = request.session.get('deposit_amount')

    start = 10 ** (8 - 1)
    end = 10 ** 8 - 1
    number = random.randint(start, end)
    row_number = str(number)
    hash_object = hashlib.sha256(row_number)
    transaction_id_digest = str(hash_object.hex_digest())

    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % amount.quantize(
            Decimal('.01')),
        'item_name': 'Land  {}'.format(land.title_deed),
        'invoice': str(land.title_deed),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payments:done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payments:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,
                  'payments/process.html',
                  {'land': land, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'payments/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payments/canceled.html')


# land purchase  payment method here MPESA PAYMENT

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
            deposit = float(cd['deposit'])
            email = cd['email']
            user = get_object_or_404(User, username=request.user)
            buyer = get_object_or_404(LandUserProfile, user=user)
            clean_phone_number = CleanPhoneNumber(phone_number).validate_phone_number()
            try:
                username = settings.USERNAME
                api_key = settings.API_KEY
                product_name = settings.PRODUCT_NAME
                currency_code = settings.CURRENCY_CODE
                metadata = {'shop_id': '556', 'item_id': 'land_purchase'}

                if settings.SAND_BOX:
                    gateway = AfricasTalkingGateway(username, api_key, "sandbox")
                    transaction_id = gateway.initiateMobilePaymentCheckout(
                        product_name,
                        phone_number,
                        currency_code,
                        deposit,
                        metadata
                    )

                    # create payment model object here and model objects as per required
                    land_purchase = LandPurchases.objects.create(
                        owner=land.user.user,
                        land=land,
                        buyer=buyer,
                        email=email,
                        phone_number=clean_phone_number,
                        deposit=deposit, )

                    land_payment = LandPurchasePayment.objects.create(
                        transaction_id=transaction_id,
                        title_deed=title_deed,
                        purchased_size=land.size,
                        payment_mode='Mpesa',
                        buyer_email=email,
                        amount=deposit,
                        status="PendingConfirmation"
                    )
                    land_payment.save()
                    land_purchase.save()
                    # mark the land on sale until the transaction is complete
                    land.on_sale = True
                    land.save()
                    message = 'Transaction initiated successfully . Check your phone to complete the payment'
                    return render(request, 'land/purchase_land.html', {'success_message': message})
                else:

                    gateway = AfricasTalkingGateway(username, api_key)
                    transaction_id = gateway.initiateMobilePaymentCheckout(
                        product_name,
                        phone_number,
                        currency_code,
                        deposit,
                        metadata
                    )

                    # create payment model object here and model objects as per required
                    land_purchase = LandPurchases.objects.create(
                        owner=land.user.user,
                        land=land,
                        buyer=buyer,
                        email=email,
                        phone_number=clean_phone_number,
                        deposit=deposit, )

                    land_payment = LandPurchasePayment.create(
                        transaction_id=transaction_id,
                        title_deed=title_deed,
                        purchased_size=land.size,
                        payment_mode='Mpesa',
                        buyer_email=email,
                        amount=deposit,
                        status="PendingConfirmation"
                    )
                    land_payment.save()
                    land_purchase.save()
                    land.on_sale = True
                    land.save()
                    message = 'Transaction initiated successfully . Check your phone to complete the payment'
                    return render(request, 'land/purchase_land.html', {'message': message})
            except (IntegrityError, AfricasTalkingGatewayException) as e:
                error_msg = 'Error occurred', e
                return render(request, 'land/purchase_land.html',{'error': error_msg, }
                )
            # # send notification to the land owner
            # message = 'The Land with title deed({0}), has been purchased by {1} on {2}, a deposit of Ksh ' \
            #           '{3} has been sent into your Paypal account.The buyers Phone number is {4}'. \
            #     format(title_deed, request.user, timezone.now(), deposit, clean_phone_number)
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













