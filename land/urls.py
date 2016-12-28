__author__ = 'hudutech'

from django.conf.urls import url
from land import views
urlpatterns = [
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^register-land/$', views.register_land, name='register_land'),
]
