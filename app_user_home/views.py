from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_home_view(request):
    if request.user.is_authenticated():
        return render(request, "home/userhome.html", {"user":request.user,"action":"home"})
    
@login_required
def user_lastpoll_view(request):
    if request.user.is_authenticated():
        return render(request, "home/userhome.html", {"user":request.user,"action":"lastpoll"})
    
@login_required
def user_profile_view(request):
    if request.user.is_authenticated():
        return render(request, "home/userhome.html", {"user":request.user,"action":"profile"})
    
@login_required
def user_setting_view(request):
    if request.user.is_authenticated():
        return render(request, "home/userhome.html", {"user":request.user,"action":"setting"})

@login_required
def user_resetpwd_view(request):
    if request.user.is_authenticated():
        return render(request, "home/userhome.html", {"user":request.user,"action":"resetpwd"})
    
