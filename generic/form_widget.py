from django import forms

def get_text_widget(attr_dict):
    custom_widget = forms.TextInput(attrs=attr_dict)
    return custom_widget
    
def get_pwd_widget(attr_dict):
    custom_widget = forms.PasswordInput(attrs=attr_dict)
    return custom_widget 
    
def get_email_widget(attr_dict):
    custom_widget = forms.EmailInput(attrs=attr_dict)
    return custom_widget