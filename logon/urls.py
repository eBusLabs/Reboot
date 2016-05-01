from django.conf.urls import url
from logon.views import *  # @UnusedWildImport

logonurl = [
    # Examples:
    # url(r'^$', 'Reboot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^now/$',current_time),
    url(r'^registration/$',registration_view),
    url(r'^logon/$',logon_view),
    url(r'^logon/requestpwd/$',request_password_view),
    url(r"^logout/",logout_view)
]
