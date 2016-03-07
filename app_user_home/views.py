from authtools.views import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import *  # @UnusedWildImport


@login_required
def user_home_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"home","polladmin":is_poll_admin})
    
@login_required
def user_lastpoll_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"lastpoll","polladmin":is_poll_admin})
    
@login_required
def user_profile_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    render(request, "home/userhome.html", {"user":request.user,"action":"profile","polladmin":is_poll_admin})
    
@login_required
def user_setting_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"setting","polladmin":is_poll_admin})

@login_required
def user_resetpwd_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    if request.method == "POST":
        form = ResetPwdForm(request.POST)
        if form.is_valid():
            #tulip containing error
            errmsgs = []
            # Check is old password is authentic
            postdic = request.POST
            if not request.user.check_password(postdic["oldpwd"]):
                errmsgs.append("Old password is incorrect")
            # Check if new password are match
            if not (postdic["newpwd"] == postdic["cnfpwd"]):
                errmsgs.append("New password don't match")
            
            if errmsgs:    
                return render(request, "home/userhome.html", {
                                                        "errmsgs":errmsgs,      
                                                        "form":form,
                                                        "user":request.user,
                                                        "action":"resetpwd",
                                                        "polladmin":is_poll_admin})
            else:
                try:
                    request.user.set_password(postdic["newpwd"])
                    request.user.save()
                    #update hash so user is not logged out due to invalid session
                    update_session_auth_hash(request, request.user)
                    return render(request, "home/userhome.html", {
                                                    "pwdcs":"Y",
                                                    "form":form,
                                                    "user":request.user,
                                                    "action":"resetpwd",
                                                    "polladmin":is_poll_admin})
                except:
                    return render(request, "home/userhome.html", {
                                                    "pwdcs":"N",
                                                    "form":form,
                                                    "user":request.user,
                                                    "action":"resetpwd",
                                                    "polladmin":is_poll_admin})
                    
                    
        else:
            return render(request, "home/userhome.html", {
                                                    "form":form,
                                                    "user":request.user,
                                                    "action":"resetpwd",
                                                    "polladmin":is_poll_admin})
    else:
        form = ResetPwdForm()
        return render(request, "home/userhome.html", {
                                                    "form":form,
                                                    "user":request.user,
                                                    "action":"resetpwd",
                                                    "polladmin":is_poll_admin})
    
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
