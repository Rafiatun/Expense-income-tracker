from django.urls import path
from django.urls.resolvers import URLPattern
from . views import *
from .import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns=[
    path('register' , RequestView.as_view() , name="register"),
    path('login',csrf_exempt(Loginview.as_view()), name="login"),
    path('logout',csrf_exempt(Logoutview.as_view()), name="logout"),
    path('validateusername' , csrf_exempt(UsernameValidationView.as_view()) , name="validate_username"),
    path('validateemail' , csrf_exempt(EmailValidationView.as_view()) , name="validate_email"),
    path('validatepass' , csrf_exempt(EmailValidationView.as_view()) , name="validate_pass"),
    path('activate/<uidb64>/<token>' , csrf_exempt(Verificationview.as_view()) , name="activate")
]

