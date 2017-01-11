from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'smartland.views.home', name='home'),
    url(r'^', include('land.urls', namespace='land')),
    url(r'^payments/', include('payments.urls', namespace='payments')),


    url(r'^admin/', include(admin.site.urls)),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'SmartLand'