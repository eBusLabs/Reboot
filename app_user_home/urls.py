from django.conf.urls import url
from app_user_home.views import *  # @UnusedWildImport

user_home_url = [
    # Examples:
    # url(r"^$", "Reboot.views.home", name="home"),
    # url(r"^blog/", include("blog.urls")),
    url(r"^uhome/$",user_home_view),
    url(r"lastpolls/$",user_lastpoll_view),
    url(r"profile/$",user_profile_view),
    url(r"setting/$",user_setting_view),
    url(r"resetpwd/$",user_resetpwd_view),
]
