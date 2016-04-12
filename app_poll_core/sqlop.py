from collections import OrderedDict
from datetime import date

from django.contrib.auth.models import Group
from django.db.models import F

from app_poll_core.models import poll_group_model, history_model

from .models import poll_model, question_model, answer_model


def insert_poll(user, jsonDict):
    pn = jsonDict["pollname"]
    # insert poll
    try:
        row_poll = poll_model   (
                                poll_name=pn,
                                created_by=user,
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
                                    question=question_name,
                                    poll_name=row_poll,
                                    )
            row_q.save();
            for optiondict in qadict["options"]:
                option_name = optiondict["option"]
                row_o = answer_model(
                                    question=row_q,
                                    option=option_name,
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
                                        ).order_by("-id")  # - sign revert the order, isn't python cool
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
        # insert into poll_group_model
        for group in group_list:
            row_poll_group = poll_group_model(
                                            poll_group=group,
                                            poll_name=row,
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
                    if not is_poll_taken(user, poll.id):
                        poll_list[str(poll.id)] = poll.poll_name
                        break
        return poll_list
    
def get_questions(poll_id):
    question_list = question_model.objects.filter(poll_name=poll_id)
    return question_list

def get_options(question_id):
    option_list = answer_model.objects.filter(question=question_id)
    return option_list

def insert_vote(user, poll_id, postdic):
    poll = None
    try:
        poll = poll_model.objects.get(id=poll_id)
        poll.total_vote = F("total_vote") + 1
        poll.save(update_fields=["total_vote"])
        for key in postdic:
            if key.startswith("question_"):
                option = answer_model.objects.get(id=postdic[key])
                option.vote = F("vote") + 1
                option.save(update_fields=["vote"])
    except Exception as e:
        print (str(e))  # logtrace
        return False
    
    try:
        history_model_row = history_model(
                                        user=user.id,
                                        poll_name=poll,
                                        taken=True,
                                        )
        history_model_row.save()
    except Exception as e:
        print (str(e))  # logtrace
        return False
    
    return True;
    
def is_poll_taken(user, poll_id):
    row = history_model.objects.filter(user=user.id, poll_name=poll_id)
    if row:
        return True
    else:
        return False
        
def poll_result(user, start_date, end_date):
    poll_list = {}
    try:
        polls = poll_model.objects.filter(poll_end__lt=end_date, poll_end__gte=start_date)
        for poll in polls:
            for grp in poll_group_model.objects.filter(poll_name=poll.id):
                if user.groups.filter(name=grp).exists():
                    poll_list[poll.id] = poll.poll_name
                    break
            
        
    except:
        #logtrace
        poll_list = {}
    return poll_list

def is_member_poll_group(user, pollid):
    is_allowed = False
    poll = poll_model.objects.get(id=pollid)
    if poll:
        for group in poll_group_model.objects.filter(poll_name=poll.id):
            if user.groups.filter(name=group).exists():
                is_allowed = True
                break
    else:
        return False
    
    return is_allowed








































