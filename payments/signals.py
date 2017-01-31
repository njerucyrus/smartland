__author__ = 'hudutech'

from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from land.models import LandPurchases, Land
import hashlib
import random


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # create secure transaction id
        land = get_object_or_404(Land, title_deed=ipn_obj.invoice)



