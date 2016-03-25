from .models import poll_model, question_model, answer_model
from django.db.models.fields import Field

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
    poll_dict = {}
    draft_rows = poll_model.objects.filter(
                                        poll_start__isnull=True,
                                        poll_end__isnull=True,
                                        created_by__exact=user,
                                        )
    for row in draft_rows:
        poll_dict[str(row.id)] = row.poll_name
    
    return poll_dict 