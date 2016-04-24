from datetime import timedelta
import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app_poll_core.sqlop import *  # @UnusedWildImport

from .forms import *  # @UnusedWildImport


def poll_admin_check(user):
    return user.groups.filter(name="polladmin").exists()

def inform_user(request, level, head, msg_list, **kwargs):
    if level in ("O", "o"):
        alert = "alert-success"
    
    if level in ("I", "i"):
        alert = "alert-info"
    
    if level in ("W", "w"):
        alert = "alert-warning"
    
    if level in ("E", "e"):
        alert = "alert-danger"
        
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    return render(request,"home/informuser.html",{
                                                    "user":request.user,
                                                    "polladmin":is_poll_admin,
                                                    "action":kwargs.get("action"),
                                                    "alert":alert,
                                                    "head":head,
                                                    "msg_list":msg_list,
                                                    })
    

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
        if  poll_dict:
            return render(request, "home/userhometab.html", {
                                                "user":request.user,
                                                "polladmin":is_poll_admin,
                                                "poll_dict":poll_dict,
                                        })
        else:
            return inform_user(request, "I", "No Polls", ["for you",],action="home")

@login_required
def user_home_poll_submit_view(request):
    if request.method == "POST":
        postdic = request.POST
        poll_id = request.session["poll_id"]
        #check if this user already  taken this poll
        if is_poll_taken(request.user, poll_id):
            msg_list = []
            msg_list.append("You have already taken this poll.")
            return inform_user(request, "W", "Smart Ass", msg_list,action="home")
            
        form = TakePollForm(postdic, qid=poll_id);
        if form.is_valid():
            if insert_vote(request.user, poll_id, postdic):
                msg_list = []
                msg_list.append("Poll Submitted Successfully.")
                return inform_user(request, "I", "Congrats",msg_list,action="home")
            else:
                msg_list = []
                msg_list.append("Database Error, Click back button and try once more")
                return inform_user(request, "E", "ERROR", msg_list,action="home")
        else:
            msg_list = []
            msg_list.append("Form Error, Click back and make sure you answered every question.")
            return inform_user(request, "E", "ERROR", msg_list,action="home")
         
@login_required
def user_lastpoll_view(request):#show poll taken by user in list
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    label_text = "Click Poll to See Result"
    #post means user requested specific date
    if request.method == "POST":
        postdic = request.POST
        start_date = postdic["sdate"]
        end_date = postdic["edate"]
        form = LinkedDatePickerForm(request.POST, start_date=start_date, end_date=end_date)
        if form.is_valid():
            poll_dict = poll_result(request.user, start_date, end_date)
            return render(request, "home/lastpolltab.html", {
                                                    "user":request.user,
                                                    "polladmin":is_poll_admin,
                                                    "poll_dict":poll_dict,
                                                    "form":form,
                                                    "label_text":label_text,
                                                    })
        else:
            return render(request, "home/lastpolltab.html", {
                                                        "user":request.user,
                                                        "polladmin":is_poll_admin,
                                                        "poll_dict":None,
                                                        "form":form,
                                                        "label_text":label_text,
                                                        })
    else:
        #by default we are showing 3 months poll result
        end_date = date.today();
        start_date = (end_date.replace(day=1) - timedelta(days=89)).replace(day=1)
        poll_dict = poll_result(request.user, start_date, end_date)
        form = LinkedDatePickerForm(start_date=start_date, end_date=end_date)
        return render(request, "home/lastpolltab.html", {
                                                    "user":request.user,
                                                    "polladmin":is_poll_admin,
                                                    "poll_dict":poll_dict,
                                                    "form":form,
                                                    "label_text":label_text,
                                                    })
        
@login_required
def user_showpoll_view(request):#show poll result to user in graphical view
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    if request.method == "POST":
        pollid = request.POST["pollid"]
        if is_member_poll_group(request.user, pollid):
            poll_data = collect_poll_data(pollid)
            return render(request, "home/lastpolltabpoll.html", {
                                                    "user":request.user,
                                                    "polladmin":is_poll_admin,
                                                    "poll_data":poll_data,
                                                    })
        else:
            return inform_user(request, "E", "ERROR", ["You are not authorized to view this poll"],action="lastpoll")
    else:
        #show home page
        return HttpResponseRedirect("/uhome")
    
@login_required
def user_resetpwd_view(request):
    is_poll_admin = request.user.groups.filter(name="polladmin").exists()
    if request.method == "POST":
        form = ResetPwdForm(request.POST)
        if form.is_valid():
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
            msg_list = []
            msg_list.append("Error parsing JSON")
            return inform_user(request, "E", "Error", msg_list,action="createpoll")
            
        pollname = jsonDict["pollname"]
        if not pollname:
            form_ok = False
            
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
                return inform_user(request, "O", "Congrats", ["Poll created successfully"],action="createpoll")
            else:
                return inform_user(request, "E", "Database", ["Error Updating database"],action="createpoll")
        else: #form not ok
            return inform_user(request, "E", "Form Error", ["Form is incorrect."],action="createpoll")
    else: # method is not post
        return render(request, "home/createpolltab.html", {
                                                        "user":request.user,
                                                        "polladmin":True,
                                                        })
        
@login_required
@user_passes_test(poll_admin_check)
def admin_all_polls_draft_view(request):
    poll_dict = draft_poll(request.user)
    return render(request,"home/alltab.html", {
                                                "polladmin":True,
                                                "user":request.user,
                                                "alldraft":True, 
                                                "poll_dict":poll_dict,
                                                })
        
@login_required
@user_passes_test(poll_admin_check)
def admin_all_polls_draft_open_or_delete_view(request):
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
                return inform_user(request, "O", "Success", ["Poll deleted successfully"],action="allpoll")

            else:
                return inform_user(request, "E", "Error", ["Database Error"],action="allpoll")
    else:
        return HttpResponseRedirect("uhome")
        
        
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
                return inform_user(request, "O", "Success", ["Poll opened successfully"],action="allpoll")
            else: #error updating database
                return inform_user(request, "E", "Error", ["Error updating database"],action="allpoll")
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
@user_passes_test(poll_admin_check)
def admin_all_polls_current_view(request):
    poll_dict = get_current_polls(request.user)
    return render(request,"home/alltab.html", {
                                                "polladmin":True,
                                                "user":request.user,
                                                "allcurrent":True, 
                                                "poll_dict":poll_dict,
                                                })


@login_required
@user_passes_test(poll_admin_check)
def admin_all_polls_current_see_or_delete_view(request):
    if request.method == "POST":
        postdic = request.POST
        action = postdic["draftaction"]
        poll_id = postdic["pollid"]
        if action == "O":
            poll_data = collect_poll_data(poll_id)
            return render(request, "home/alltab.html", {
                                                    "user":request.user,
                                                    "polladmin":True,
                                                     "allcurrent_show":True, 
                                                    "poll_data":poll_data,
                                                    })
        if action == "D":
            if delete_poll(poll_id):
                return inform_user(request, "O", "Success", ["Poll deleted successfully"],action="allpoll")

            else:
                return inform_user(request, "E", "Error", ["Database Error"],action="allpoll")
    else:
        #show home page
        return HttpResponseRedirect("/uhome")

    
@login_required
@user_passes_test(poll_admin_check)
def admin_all_polls_completed_view(request):
    label_text = "View Result or Delete Poll"
    if request.method == "POST":
        postdic = request.POST
        start_date = postdic["sdate"]
        end_date = postdic["edate"]
        form = LinkedDatePickerForm(request.POST, start_date=start_date, end_date=end_date)
        if form.is_valid():
            poll_dict = get_completed_polls(request.user, start_date, end_date)
            return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "form":form,
                                                    "allcompleted":True, 
                                                    "poll_dict":poll_dict,
                                                    "label_text":label_text,
                                                    })
        else:
            return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "form":form,
                                                    "allcompleted":True, 
                                                    "poll_dict":None,
                                                    "label_text":label_text,
                                                    })
    else:
        end_date = date.today();
        start_date = (end_date.replace(day=1) - timedelta(days=89)).replace(day=1)
        form = LinkedDatePickerForm(start_date=start_date, end_date=end_date)
        poll_dict = get_completed_polls(request.user, start_date, end_date)
        return render(request,"home/alltab.html", {
                                                    "polladmin":True,
                                                    "user":request.user,
                                                    "form":form,
                                                    "allcompleted":True, 
                                                    "poll_dict":poll_dict,
                                                    "label_text":label_text,
                                                    })
        
@login_required
@user_passes_test(poll_admin_check)
def admin_all_polls_completed_action_view(request):
    if request.method == "POST":
        postdic = request.POST
        action = postdic["draftaction"]
        poll_id = postdic["pollid"]
        if action == "O":
            poll_data = collect_poll_data(poll_id)
            return render(request, "home/alltab.html", {
                                                    "user":request.user,
                                                    "polladmin":True,
                                                     "allcompleted_show":True, 
                                                    "poll_data":poll_data,
                                                    })
        if action == "D":
            if delete_poll(poll_id):
                return inform_user(request, "O", "Success", ["Poll deleted successfully"],action="allpoll")
  
            else:
                return inform_user(request, "E", "Error", ["Database Error"],action="allpoll")
              
    else:
        #if request is not post show user home page
        return HttpResponseRedirect("/uhome")
    

