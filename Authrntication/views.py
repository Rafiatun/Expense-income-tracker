from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import sys
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import tokengenerator
from django.contrib import auth
from Expense.views import *
from Expense.urls import *
from django.shortcuts import redirect
# Create your views here.
class PasswordValidation(View):
    def post(self,request):
       data=json.loads(request.body)
       password= data['password']

       if not str(password).isalnum():
           return JsonResponse({'password_error': 'User name only should contain alphanumeric character'},status=400)
       if User.objects.filter(password=password).exists():
           return JsonResponse({'password_error': 'Username exists.Choose another name'})
       
       return JsonResponse({'password_valid': True})



class EmailValidationView(View):
    def post(self,request):
       data=json.loads(request.body)
       email= data['email']

       if not validate_email(email):
           return JsonResponse({'email_error': 'Email is invalid'},status=400)
       if User.objects.filter(email=email).exists():
           return JsonResponse({'email_error': 'Email is in use.Use another email'})
       
       return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self,request):
       data=json.loads(request.body)
       username= data['username']

       if not str(username).isalnum():
           return JsonResponse({'username_error': 'User name only should contain alphanumeric character'},status=400)
       if User.objects.filter(username=username).exists():
           return JsonResponse({'username_error': 'Username exists.Choose another name'})
       
       return JsonResponse({'Username_valid': True})


class RequestView(View):
    def get(self,request):
        return render(request, 'register.html')

    def post(self,request):
        # get_user_data
        # validate

        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        context={
            'fieldvalue':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<8:
                    messages.error(request, 'Your password is too short.it hase to contain 8 character minimum')
                    return render(request, 'register.html' ,context)

                user=User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active=True
                user.save()
                
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': tokengenerator.make_token(user),
                }
                
                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = "http://"+ current_site.domain+link
                
                email_subject="Activate your account"
                email_body= "hello " + user.username + " please use the link to verify your account     " + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'no-reply@semicolon.com',
                    [email],)

                email.send(fail_silently=False)
    
                messages.success(request,"Account successfully created.")
                return render(request, 'register.html',context)
        return render(request, 'register.html',context)


class Verificationview(View):
    def get(self,request,uidb64,token):
        try:
            id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            if not tokengenerator.check_token(user,token):
                return redirect('login'+'?message='+'User already activated')


            if user.is_active:
                return redirect('login')
            user.active=True
            user.save()
            messages.success(request,"Account activated successfully")

        except Exception as ex:
            pass
            
        return redirect('login')



class Loginview(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username +'you are now logged in')
                    return redirect('home')
            messages.error(request, 'Account is not active,please check your email')
            return render(request, 'login.html')

        messages.error(request, 'Please fill all fields')
        return render(request, 'login.html')


class Logoutview(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,"    You are logged out")
        return redirect('login')