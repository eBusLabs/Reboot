from django import forms  # @UnusedImport

from generic.form_widget import *  # @UnusedWildImport
from app_poll_core.sqlop import get_groups

class ResetPwdForm(forms.Form):
    attrs = {"class":"form-control", "placeholder":"Password", "required":"", "autofocus":"", "type":"password"}
    oldpwd = forms.CharField(10, 4, widget=get_pwd_widget(attrs))
    del attrs["autofocus"]
    
    attrs["placeholder"] = "New Password"
    newpwd = forms.CharField(10, 4, widget=get_pwd_widget(attrs))
    
    attrs["placeholder"] = "Confirm Password"
    cnfpwd = forms.CharField(10, 4, widget=get_pwd_widget(attrs))
    
class OpenPollForm(forms.Form):
    attrs = {"class":"form-control"}
    start_date = forms.DateField(widget = get_date_widget(attrs))
    end_date = forms.DateField(widget = get_date_widget(attrs))


