__author__ = 'hudutech'

from django.conf.urls import url
from payments import views
urlpatterns = [
    url(r'^transfer/(?P<pk>[0-9])/$', views.land_transfer_payment, name='transfer_payment'),
    url(r'^callback/$', views.mpesa_notification_callback, name='callback'),

]
