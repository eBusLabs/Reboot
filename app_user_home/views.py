import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from app_poll_core.sqlop import *  # @UnusedWildImport

from .forms import *  # @UnusedWildImport
from django.http.response import HttpResponse

def poll_admin_check(user):
    return user.groups.filter(name="polladmin").exists()

@login_required
def user_home_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    poll_dict = get_polls_for_user(request.user)
    if request.method == "POST":
        postdic = request.POST
        poll_id = postdic["pollid"]
        request.session["poll_id"] = poll_id
        form = TakePollForm(qid=poll_id);
        return render(request, "home/usrpoll.html", {
                                                    "user":request.user,
                                                    "polladmin":is_poll_admin,
                                                    "form":form,
                                                    "poll_id":poll_id,
                                                    "action":"take_poll"
                                                    })
    else:
        return render(request, "home/userhometab.html", {
                                                "user":request.user,
                                                "polladmin":is_poll_admin,
                                                "poll_dict":poll_dict,
                                        })

@login_required
def user_home_poll_submit_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    if request.method == "POST":
        postdic = request.POST
        poll_id = request.session["poll_id"]
        #check if this user already  taken this poll
        if is_poll_taken(request.user, poll_id):
            return render(request, "home/usrpoll.html", {
                                                        "user":request.user,
                                                        "polladmin":is_poll_admin,
                                                        "usrpollrc":"taken",
                                                        })
            
            
        form = TakePollForm(postdic, qid=poll_id);
        if form.is_valid():
            if insert_vote(request.user, poll_id, postdic):
                return render(request, "home/usrpoll.html", {
                                                        "user":request.user,
                                                        "polladmin":is_poll_admin,
                                                        "usrpollrc":"pss",
                                                        })
            else:
                return render(request, "home/usrpoll.html", {
                                                        "user":request.user,
                                                        "polladmin":is_poll_admin,
                                                        "usrpollrc":"psfd",
                                                        })
        else:
            return render(request, "home/usrpoll.html", {
                                                    "user":request.user,
                                                    "polladmin":is_poll_admin,
                                                    "usrpollrc":"psf",
                                                    })
         
@login_required
def user_lastpoll_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request, "home/lastpolltab.html", {
                                                "user":request.user,
                                                "polladmin":is_poll_admin,
                                                })
    
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
                return render(request, "home/changepwdtab.html", {
                                                                "errmsgs":errmsgs,      
                                                                "form":form,
                                                                "user":request.user,
                                                                "polladmin":is_poll_admin,
                                                            })
            else:
                try:
                    request.user.set_password(postdic["newpwd"])
                    request.user.save()
                    #update hash so user is not logged out due to invalid session
                    update_session_auth_hash(request, request.user)
                    return render(request, "home/changepwdtab.html", {
                                                                    "pwdcs":"Y",
                                                                    "form":form,
                                                                    "user":request.user,
                                                                    "polladmin":is_poll_admin,
                                                                    })
                except:
                    return render(request, "home/changepwdtab.html", {
                                                                    "pwdcs":"N",
                                                                    "form":form,
                                                                    "user":request.user,
                                                                    "polladmin":is_poll_admin,
                                                                    })
                    
                    
        else:
            return render(request, "home/changepwdtab.html", {
                                                            "form":form,
                                                            "user":request.user,
                                                            "polladmin":is_poll_admin,
                                                            })
    else:
        form = ResetPwdForm()
        return render(request, "home/changepwdtab.html", {
                                                    "form":form,
                                                    "user":request.user,
                                                    "polladmin":is_poll_admin,
                                                    })
    
@login_required
@user_passes_test(poll_admin_check)
def admin_create_polls_view(request):
    if request.method == "POST":
        form_ok = True
        jsonData = request.POST["jsonData"]
        rs = ""
        try:
            jsonDict = json.loads(jsonData)
        except:
            return render(request, "home/createpolltab.html", {
                                                            "user":request.user,
                                                            "polladmin":True,
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
                return render(request, "home/createpolltab.html", {  
                                                                "user":request.user,
                                                                "polladmin":True,
                                                                "rc":"Y",
                                                            })
            else:
                return render(request, "home/createpolltab.html", {  
                                                                "user":request.user,
                                                                "polladmin":True,
                                                                "rc":"DB",
                                                            })
        else: #form not ok
            return render(request, "home/createpolltab.html", {  
                                                            "user":request.user,
                                                            "polladmin":True,
                                                            "rc":"FE", #form error    
                                                            })
    else: # method is not post
        return render(request, "home/createpolltab.html", {
                                                        "user":request.user,
                                                        "polladmin":True,
                                                        })
@login_required
@user_passes_test(poll_admin_check)
def admin_all_polls_view(request):
    poll_dict = draft_poll(request.user)
    return render(request, "home/alltab.html",{
                                                "polladmin":True,
                                                "user":request.user,
                                                "alldraft":True,
                                                "poll_dict":poll_dict,
                                                }) 

@login_required
@user_passes_test(poll_admin_check)
def admin_all_polls_draft_view(request):
    if request.method == "POST":
        postdic = request.POST
        action = postdic["draftaction"]
        poll_id = postdic["pollid"]
        poll_name = postdic["poll_name"]
        if action == "O":
            groups = get_groups("ebus")
            form = OpenPollForm()
            return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "form":form,
                                                    "alldraft_open":True,
                                                    "poll_name":poll_name,
                                                    "poll_id":poll_id,
                                                    "group_list":groups,
                                                    }) 
        if action == "D":
            if delete_poll(poll_id):
                return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "alldraft":True, 
                                                    "alldraftrc":"DPS",
                                                    })
            else:
                return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "alldraft":True, 
                                                    "alldraftrc":"DPF",
                                                    })
    else:
        poll_dict = draft_poll(request.user)
        return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "alldraft":True, 
                                                    "poll_dict":poll_dict,
                                                    })
        
@login_required
@user_passes_test(poll_admin_check)
def admin_all_polls_draft_view_open(request):
    groups = get_groups("ebus")
    if request.method == "POST":
        form = OpenPollForm(request.POST)
        postdic = request.POST
        poll_id = postdic["poll_id"]
        poll_name = postdic["poll_name"]
        if form.is_valid():
            group_list = postdic.getlist("group_names")
            # check group_list manually, as i don't add this in form
            if group_list:
                for item in group_list:
                    if is_group_exist(item):
                        pass
                    else: #invalid group
                        return render(request,"home/alltab.html", {
                                                        "polladmin":True,
                                                        "user":request.user,
                                                        "form":form,
                                                        "alldraft_open":True,
                                                        "poll_name":poll_name,
                                                        "poll_id":poll_id,
                                                        "group_list":groups,
                                                        "empty_group":True,
                                                        }) 
            else: #group_list is empty
                return render(request,"home/alltab.html", {
                                                        "polladmin":True,
                                                        "user":request.user,
                                                        "form":form,
                                                        "alldraft_open":True,
                                                        "poll_name":poll_name,
                                                        "poll_id":poll_id,
                                                        "group_list":groups,
                                                        "empty_group":True,
                                                        }) 
                    
            start_date = postdic["start_date"]
            end_date = postdic["end_date"]
            if open_poll(poll_id, start_date, end_date, group_list):#update database
                return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "alldraft":True, 
                                                    "alldraftrc":"OPS",
                                                    })
            else: #error updating database
                return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "alldraft":True, 
                                                    "alldraftrc":"OPF",
                                                    })
        else: #invalid form, return with errors
            return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "form":form,
                                                    "alldraft_open":True,
                                                    "poll_name":poll_name,
                                                    "poll_id":poll_id,
                                                    "group_list":groups,
                                                    }) 
    
@login_required
def admin_all_polls_current_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request,"home/alltab.html", {
                                                "polladmin":is_poll_admin,
                                                "user":request.user,
                                                "allcurrent":True, 
                                                })
    
@login_required
def admin_all_polls_completed_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request,"home/alltab.html", {
                                                "polladmin":is_poll_admin,
                                                "user":request.user,
                                                "allcompleted":True, 
                                                })
