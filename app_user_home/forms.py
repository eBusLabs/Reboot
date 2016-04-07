from django import forms  # @UnusedImport

from generic.form_widget import *  # @UnusedWildImport
from app_poll_core.sqlop import get_questions, get_options

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

class TakePollForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.qid = kwargs.pop("qid")
        super(TakePollForm, self).__init__(*args, **kwargs)
        attrs = {}
        question_rows = get_questions(self.qid)
        count = 0
        for question_row in question_rows:
            choices = []
            question_id = question_row.id;
            question_value = question_row.question;
            options_rows = get_options(question_id)
            for option_row in options_rows:
                choice = (option_row.id, option_row.option)
                choices.append(choice)
            self.fields["question_" + str(count)] = forms.ChoiceField(label=question_value, choices=tuple(choices), widget=get_radio_widget(attrs))
            count = count + 1

