from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'smartland.views.home', name='home'),
    url(r'^', include('land.urls', namespace='land')),

    url(r'^admin/', include(admin.site.urls)),
]

admin.site.site_header = 'SmartLand'