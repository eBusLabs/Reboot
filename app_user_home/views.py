from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def user_home_view(request):
    if request.user.is_authenticated():
        is_poll_admin = request.user.groups.filter(name="polladmin").exists()
        print ("is poll admin " + str(is_poll_admin))
        return render(request, "home/userhome.html", {"user":request.user,"action":"home","polladmin":is_poll_admin})
    
@login_required
def user_lastpoll_view(request):
    if request.user.is_authenticated():
        is_poll_admin = request.user.groups.filter(name="polladmin").exists()
        return render(request, "home/userhome.html", {"user":request.user,"action":"lastpoll","polladmin":is_poll_admin})
    
@login_required
def user_profile_view(request):
    if request.user.is_authenticated():
        is_poll_admin = request.user.groups.filter(name="polladmin").exists()
        return render(request, "home/userhome.html", {"user":request.user,"action":"profile","polladmin":is_poll_admin})
    
@login_required
def user_setting_view(request):
    if request.user.is_authenticated():
        is_poll_admin = request.user.groups.filter(name="polladmin").exists()
        return render(request, "home/userhome.html", {"user":request.user,"action":"setting","polladmin":is_poll_admin})

@login_required
def user_resetpwd_view(request):
    if request.user.is_authenticated():
        is_poll_admin = request.user.groups.filter(name="polladmin").exists()
        return render(request, "home/userhome.html", {"user":request.user,"action":"resetpwd","polladmin":is_poll_admin})
    
@login_required
def admin_create_polls_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"addpoll","polladmin":is_poll_admin})
    pass

@login_required
def admin_current_polls_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"currpoll","polladmin":is_poll_admin})
    pass

@login_required
def admin_all_polls_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"allpoll","polladmin":is_poll_admin}) 

@login_required
def admin_delete_polls_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"delpoll","polladmin":is_poll_admin})
