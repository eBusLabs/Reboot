from django import forms
from generic import form_widget


class ResetPwdForm(forms.Form):
    attrs = {"class":"form-control", "placeholder":"Password", "required":"", "autofocus":"", "type":"password"}
    oldpwd = forms.CharField(10, 4, widget=form_widget.get_pwd_widget(attrs))
    del attrs["autofocus"]
    
    attrs["placeholder"] = "New Password"
    newpwd = forms.CharField(10, 4, widget=form_widget.get_pwd_widget(attrs))
    
    attrs["placeholder"] = "Confirm Password"
    cnfpwd = forms.CharField(10, 4, widget=form_widget.get_pwd_widget(attrs))