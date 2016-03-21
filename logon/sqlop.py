from django.contrib.auth.models import User
from django.db import IntegrityError

def register_user(postdic):
    user_name = postdic.get('user_name')
    first_name = postdic.get('first_name') 
    last_name = postdic.get('last_name')
    email = postdic.get('email')
    passworda = postdic.get('passworda')
    
    try:
        user = User.objects.create_user(password=passworda
                                    ,first_name=first_name
                                    ,last_name=last_name
                                    ,email=email
                                    ,username=user_name)
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save()
        return 'OK'
    except IntegrityError as ie:
        return str(ie)
        
    except Exception as e:
        return str(e)
        
    
    
    
    
    