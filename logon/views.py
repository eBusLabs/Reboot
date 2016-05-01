import datetime

from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from logon.forms import *  # @UnusedWildImport
from logon.sqlop import register_user
from django.contrib.auth.decorators import login_required


# Create your views here.
def current_time(request):
    ct = datetime.datetime.now()
    return render(request,"others/currenttime.html",{"current_time":ct,})
    
def registration_view(request):
    pwdmatch = True
    usrexist = False
    emailexist = False
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            postdic = request.POST
            passworda = postdic.get("passworda")
            passwordb = postdic.get("passwordb")
            if (passworda != passwordb):
                pwdmatch = False
                return render(request,"registration/registration.html", {
                                                        "form":form,
                                                        "pwdmatch":pwdmatch,
                                                        "usrexist":usrexist,
                                                        "emailexist":emailexist,
                                                        })
            else:
                result = register_user(postdic)
                if (result is "OK"):
                    msg = "You registered successfully !!!"
                    url = "/logon/"
                    bt = "Take me to logon"
                    return render(request,"generic/success.html", {
                                                                "msg":msg,
                                                                "url":url,
                                                                "bt":bt,   
                                                                   })
                else:
                    if "auth_user.email" in result:
                        emailexist = True
                    if "auth_user.username" in result:
                        usrexist = True
                    return render(request,"registration/registration.html", {
                                                            "form":form,
                                                            "pwdmatch":pwdmatch,
                                                            "usrexist":usrexist,
                                                            "emailexist":emailexist,
                                                            })
        else:
            return render(request,"registration/registration.html", {
                                                        "form":form,
                                                        "pwdmatch":pwdmatch,
                                                        })
    else:
        form = Registration()
        return render(request, "registration/registration.html", {
                                                   "form":form,
                                                   "pwdmatch":pwdmatch,
                                                   })
        
def logon_view(request):
    if request.method == "POST":
        postdic = request.POST
        uid = postdic.get("uid")
        pwd = postdic.get("pwd")
        user = authenticate(username=uid, password=pwd)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect("/uhome/")
            else:
                msg = "Oops !! Your account has been disabled"
                url = "#"
                bt = "Take me customer support"
                return render(request,"generic/failure.html",{
                                                            "msg":msg,
                                                            "url":url,
                                                            "bt":bt,
                                                            })
        else:
            msg = "Oops !! UserID and Password don't match"
            url = "/logon/"
            bt = "Take me to Logon"
            return render(request,"generic/failure.html",{
                                                        "msg":msg,
                                                        "url":url,
                                                        "bt":bt,
                                                        })
    else:
        form = Logon()
        return render(request,"logon/logon.html",{"form":form,})

def request_password_view(request):
    from generic.get_random import get_random_alphanumeric_string
    from django.core.mail import send_mail
    pwd = get_random_alphanumeric_string(6)
    send_mail('Subject here', 'Here is the message.', 'emltstng@gmail.com',
    ['grbgct@gmail.com',], fail_silently=False)
    return HttpResponse(pwd)

@login_required    
def logout_view(request):
    msg = "See you soon " + request.user.first_name
    url = "/logon/"
    bt = "Take me to Logon"
    logout(request)
    return render(request,"generic/success.html",{
                                                "msg":msg,
                                                "url":url,
                                                "bt":bt,
                                                 })

    