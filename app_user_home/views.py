import json

from authtools.views import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app_poll_core.sqlop import insert_poll, draft_poll

from .forms import *  # @UnusedWildImport
from django.http.response import HttpResponse


@login_required
def user_home_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"home","polladmin":is_poll_admin})
    
@login_required
def user_lastpoll_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html", {"user":request.user,"action":"lastpoll","polladmin":is_poll_admin})
    
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
    if request.method == "POST":
        form_ok = True
        jsonData = request.POST["jsonData"]
        rs = ""
        try:
            jsonDict = json.loads(jsonData)
        except:
            return render(request, "home/userhome.html", {"user":request.user,
                                                            "action":"createpoll",
                                                            "polladmin":is_poll_admin,
                                                            "rc":"EPJ" #error parsing json
                                                            })
            
        pollname = jsonDict["pollname"]
        if not pollname:
            form_ok = False
            
        rs = rs + "pollname : " + pollname + "<br>"  
        question_list = jsonDict["questions"]
        
        #check if list is empty
        if not question_list:
            form_ok = False
        else:    
        # loop through questions
            for qadict in question_list:
                question_name = qadict["question"]
                if not question_name:
                    form_ok = False
                    break
                else: #question is not empty
                    rs = rs + "question : " + question_name  + "<br>"
                    #loop through option
                    option_count = len(qadict["options"])
                    if option_count < 2:
                        form_ok = False
                        break
                    for optiondict in qadict["options"]:
                        option_name = optiondict["option"]
                        if not option_name:
                            form_ok = False
                            break
                        else:
                            rs = rs + "option : " + option_name + "<br>"
                    else:
                        continue
                    break
                    
        if form_ok:            
            insert_success = insert_poll(request.user, jsonDict)
            if insert_success:
                return render(request, "home/userhome.html", {  "user":request.user,
                                                                "action":"createpoll",
                                                                "polladmin":is_poll_admin,
                                                                "rc":"Y",
                                                            })
            else:
                return render(request, "home/userhome.html", {  "user":request.user,
                                                                "action":"createpoll",
                                                                "polladmin":is_poll_admin,
                                                                "rc":"DB",
                                                            })
        else: #form not ok
            return render(request, "home/userhome.html", {  "user":request.user,
                                                          "action":"createpoll",
                                                          "polladmin":is_poll_admin,
                                                          "rc":"FE", #form error    
                                                        })
    else: # method is not post
        return render(request, "home/userhome.html", {"user":request.user,
                                                      "action":"createpoll",
                                                      "polladmin":is_poll_admin})
@login_required
def admin_all_polls_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/userhome.html",{
                                                "polladmin":is_poll_admin,
                                                "user":request.user,
                                                "action":"allpoll",
                                                "alldraft":True
                                                }) 

@login_required
def admin_all_polls_draft_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    if request.method == "POST":
        postdic = request.POST
        pollid = postdic["pollid"]
        action = postdic["draftaction"]
        return HttpResponse(pollid + "<br>" + action)
    else:
        poll_dict = draft_poll(request.user)
        return render(request,"home/userhome.html", {
                                                    "polladmin":is_poll_admin,
                                                    "user":request.user,
                                                    "action":"allpoll",
                                                    "alldraft":True, 
                                                    "poll_dict":poll_dict,
                                                    })

@login_required
def admin_all_polls_current_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request,"home/userhome.html", {
                                                "polladmin":is_poll_admin,
                                                "user":request.user,
                                                "action":"allpoll",
                                                "allcurrent":True, 
                                                })
    
@login_required
def admin_all_polls_completed_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request,"home/userhome.html", {
                                                "polladmin":is_poll_admin,
                                                "user":request.user,
                                                "action":"allpoll",
                                                "allcompleted":True, 
                                                })
