__author__ = 'hudutech'

from django.conf.urls import url
from payments import views
urlpatterns = [
    url(r'^transfer/(?P<pk>[0-9])/$', views.land_transfer_payment, name='transfer_payment'),
    url(r'^purchase/(?P<pk>[0-9])/$', views.purchase_land, name='purchase'),
    url(r'^callback/$', views.mpesa_notification_callback, name='callback'),
    url(r'^fee-history/$', views.transaction_history, name='history'),
    url(r'^process/$', views.land_payment_process, name='process'),
    url(r'^done/$', views.payment_done, name='done'),
    url(r'^canceled/$', views.payment_canceled, name='cancelled'),

]
