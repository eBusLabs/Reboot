from .models import poll_model, question_model, answer_model
from collections import OrderedDict
from django.contrib.auth.models import Group
from app_poll_core.models import poll_group_model
from datetime import date

def insert_poll(user, jsonDict):
    pn = jsonDict["pollname"]
    #insert poll
    try:
        row_poll = poll_model   (
                                poll_name = pn,
                                created_by = user,
                                )
        row_poll.save()
    except Exception as e:
        print ("Updating poll name : " + str(e))
        return False
        
    
    question_list = jsonDict["questions"]
    
    for qadict in question_list:    
        question_name = qadict["question"]
        try:
            row_q = question_model  (
                                    question = question_name,
                                    poll_name = row_poll,
                                    )
            row_q.save();
            for optiondict in qadict["options"]:
                option_name = optiondict["option"]
                row_o = answer_model(
                                    question = row_q,
                                    option = option_name,
                                    )
                row_o.save()
        except Exception as e:
            print("Updating option or question : " + str(e))
            return False
    
    return True

def draft_poll(user):
    poll_dict = OrderedDict()
    draft_rows = poll_model.objects.filter(
                                        poll_start__isnull=True,
                                        poll_end__isnull=True,
                                        created_by=user,
                                        ).order_by("-id") #- sign revert the order, isn't python cool
    for row in draft_rows:
        poll_dict[str(row.id)] = row.poll_name
    
    return poll_dict 

def is_group_exist(group_name):
    return Group.objects.filter(name=group_name).exists()

def get_groups(starts_with=""):
    group_list = []
    group_rows = Group.objects.filter(
                                        name__startswith=starts_with
                                    )
    for row in group_rows:
        group_list.append(row.name)
    
    return group_list

def open_poll(poll_id, poll_start, poll_end, group_list):
    row = poll_model.objects.get(id=poll_id)
    row.poll_start = poll_start
    row.poll_end = poll_end
    try:
        row.save()
        #insert into poll_group_model
        for group in group_list:
            row_poll_group = poll_group_model(
                                            poll_group = group,
                                            poll_name = row,    
                                            )
            row_poll_group.save()
    except:
        return False
    
    return True

def delete_poll(poll_id):
    try:
        row = poll_model.objects.get(id=poll_id)
        row.delete()
    except:
        return False
    
    return True

def get_polls_for_user(user):
        poll_available = poll_model.objects.filter(poll_end__gte=date.today())
        poll_list = {}
        for poll in poll_available:
            for grp in poll_group_model.objects.filter(poll_name=poll.id):
                if user.groups.filter(name=grp).exists():
                    poll_list[str(poll.id)] = poll.poll_name
                    break
        return poll_list
    













































