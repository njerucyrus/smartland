__author__ = 'hudutech'

from django.conf.urls import url
from land import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^register-land/$', views.register_land, name='register_land'),
    url(r'^transfer-land/(?P<pk>[0-9])/$', views.transfer_land, name='transfer_land'),
    url(r'^mylands/$', views.my_land_list, name='mylands'),
    url(r'^lands-onsale/$', views.land_on_sale, name='lands_onsale'),
    url(r'^purchase/(?P<pk>[0-9])/$', views.purchase_land, name='purchase'),
    url(r'^contactus/$', views.contact_us, name='contactus'),
    url(r'^lands-bought/$', views.lands_bought, name='lands_bought'),
    url(r'^notifications/(?P<user>[-\w]+)/$', views.get_notification, name='notification'),
    url(r'^approve/(?P<title_deed>[-\w]+)/$', views.approve_purchased_land, name='approve'),
    url(r'^reject/(?P<title_deed>[-\w]+)/$', views.reject_purchased_land, name='reject'),


]
