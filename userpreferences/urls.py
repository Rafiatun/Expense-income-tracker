from django.urls.resolvers import URLPattern
from . views import *
from .import views
from django.urls import path

urlpatterns=[
    path('pref_index' , views.pref_index ,name="pref_index")
]