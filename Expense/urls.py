from django.urls import path
from django.urls.resolvers import URLPattern
from . views import *
from .import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns=[
    path('' , views.home , name="home"),
    path('add-expense', views.add_expense ,name="add_expense"),
    path('edit/<int:id>', views.expense_edit ,name="expense_edit"),
    path('delete/<int:id>', views.expense_delete ,name="expense_delete"),
    path('search_expense', csrf_exempt(views.search_expense) ,name="search_expense"),
    path('expense_category_summary',csrf_exempt(views.expense_category_summary),name="expense_category_summary"),
    path('stats' , views.stats_view,name="stats"),
    path('export_csv',views.export_csv,name="export_csv")
]