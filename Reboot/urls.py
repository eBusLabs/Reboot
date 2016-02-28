from django.conf.urls import include, url
from django.contrib import admin
from Reboot.views import home_view
from logon.urls import logonurl
from app_user_home.urls import user_home_url
urlpatterns = [
    # Examples:
    # url(r'^$', 'Reboot.views.home_view', name='home_view'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',home_view),
] + logonurl + user_home_url
