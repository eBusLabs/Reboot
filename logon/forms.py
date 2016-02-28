from django import forms
from generic import form_widget
            
class Registration(forms.Form):
    attrs = {'class':'form-control','placeholder': 'Enter User ID','required':'','autofocus':''}
    user_name = forms.CharField(30, 4, label='User Id : ', widget=form_widget.get_text_widget(attrs))
    del attrs['autofocus']
    
    attrs['placeholder'] = 'Enter First Name'
    first_name = forms.CharField(30, 1, label='First Name : ', widget=form_widget.get_text_widget(attrs))
    
    attrs['placeholder'] = 'Enter Last Name'
    last_name = forms.CharField(30, 1, label='Last Name : ', widget=form_widget.get_text_widget(attrs))
    
    attrs['placeholder'] = 'Enter Email'
    email = forms.EmailField(30, 4, label='Email : ', widget=form_widget.get_email_widget(attrs))
    
    attrs['placeholder'] = 'Enter Password'
    passworda = forms.CharField(10,4,label='New Password : ',widget=form_widget.get_pwd_widget(attrs))
    
    attrs['placeholder'] = 'Confirm Password'
    passwordb = forms.CharField(10,4,label='Confirm Password : ',widget=form_widget.get_pwd_widget(attrs))
    
class Logon(forms.Form):
    attrs = {'class':'form-control','placeholder': 'Enter User ID','required':'','autofocus':''}
    uid = forms.CharField(30, 4, label='User ID : ',widget=form_widget.get_text_widget(attrs))
    del attrs['autofocus']
    
    attrs['placeholder'] = 'Enter Password'
    pwd = forms.CharField(10, 4, label='Password : ',widget=form_widget.get_pwd_widget(attrs))
    

    
        
