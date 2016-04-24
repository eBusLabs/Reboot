from django.conf.urls import url
from app_user_home.views import *  # @UnusedWildImport

user_home_url = [
    # Examples:
    # url(r"^$", "Reboot.views.home", name="home"),
    # url(r"^blog/", include("blog.urls")),
    url(r"^uhome/$", user_home_view),
    url(r"^uhome/submit/$", user_home_poll_submit_view),
    url(r"lastpolls/$", user_lastpoll_view),
    url(r"lastpolls/showpoll/$", user_showpoll_view),
    url(r"resetpwd/$", user_resetpwd_view),
    url(r"createpoll/$", admin_create_polls_view),
    url(r"allpoll/$", admin_all_polls_draft_view),
    url(r"allpoll/draft/$", admin_all_polls_draft_view),
    url(r"allpoll/draft/action/$", admin_all_polls_draft_open_or_delete_view),
    url(r"allpoll/draft/open/$", admin_all_polls_draft_view_open),
    url(r"allpoll/current/$", admin_all_polls_current_view),
    url(r"allpoll/current/action/$", admin_all_polls_current_see_or_delete_view),
    url(r"allpoll/completed/$", admin_all_polls_completed_view),
    url(r"allpoll/completed/action/$", admin_all_polls_completed_action_view),
    #if nothing match show homepage, this must be last
    #url(r"^.*$",user_home_view)
]

