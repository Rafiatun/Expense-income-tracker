from django.core.checks import messages
from django.shortcuts import render
import os
import json
from django.conf import settings
# Create your views here.
from .models import Userpreference
from django.contrib import messages



def pref_index(request):
    currency_data=[]
    file_path=os.path.join(settings.BASE_DIR , 'currencies.json')
    with open(file_path) as json_file:
        data=json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name': k ,'value':v})

    exists=Userpreference.objects.filter(user=request.user).exists()
    user_preferences=None

    if exists:
       user_preferences=Userpreference.objects.get(user=request.user)


    if request.method =="GET":
        return render(request, 'pref_base.html',{'currencies': currency_data ,'user_pref':user_preferences})
    
    else:
        currency=request.POST['currency']
        if exists:
            user_preferences.currency=currency
            user_preferences.save()

        else:
            Userpreference.objects.create(user=request.user, currency=currency)
        
        
        messages.success(request,'Changes saved')
        return render(request, 'pref_base.html',{'currencies': currency_data,'user_pref':user_preferences})
        
