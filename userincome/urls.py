from django.urls import path
from django.urls.resolvers import URLPattern
from .import views
from django.views.decorators.csrf import csrf_exempt
from userincome.views import *

urlpatterns=[
    path('income' , views.home , name="income"),
    path('add_income' , views.add_income , name="add_income"),
    path('editincome/<int:id>', csrf_exempt(views.income_edit) ,name="editincome"),
    path('deleteincome/<int:id>', views.income_delete ,name="deleteincome"),
    path('search_income', csrf_exempt(views.search_income) ,name="search_income")
   
]