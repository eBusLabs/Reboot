from .models import poll_model, question_model, answer_model

def insert_poll(jsonDict):
    poll_id = 0;
    pn = jsonDict["pollname"]
    #insert poll
    print("Pollname : " + pn)
    try:
        row_poll = poll_model   (
                                poll_name = pn,
                                poll_status = "D",
                                )
        row_poll.save()
        poll_id = row_poll.id
    except Exception as e:
        print ("Updating poll name : " + str(e))
        return False
        
    
    question_list = jsonDict["questions"]
    
    for qadict in question_list:    
        question_name = qadict["question"]
        print("Question : " + question_name)
        try:
            row_q = question_model  (
                                    question = question_name,
                                    poll_name = row_poll,
                                    )
            row_q.save();
            q_id = row_q.id
            for optiondict in qadict["options"]:
                option_name = optiondict["option"]
                print("Option : " + option_name)
                row_o = answer_model(
                                    question = row_q,
                                    option = option_name,
                                    )
                row_o.save()
        except Exception as e:
            print("Updating option or question : " + str(e))
            return False
    
    return True