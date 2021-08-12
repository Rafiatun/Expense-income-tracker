from django.core.checks import messages
from Expense.models import Category, Expense
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import UserIncome,Source
from userpreferences.models import Userpreference
import datetime

def search_income(request):
    if request.method=="POST":
        search_string=json.loads(request.body).get('searchText')
        expenses=UserIncome.objects.filter(
            amount__istartswith=search_string ,user=request.user) | UserIncome.objects.filter(
            date__istartswith=search_string ,user=request.user) | UserIncome.objects.filter(
            description__icontains=search_string ,user=request.user) | UserIncome.objects.filter(
            source__icontains=search_string ,user=request.user)

        data=expenses.values()
        return JsonResponse(list(data),safe=False)


@login_required(login_url='login')
def home(request):
    income=UserIncome.objects.filter(user=request.user)
    paginator=Paginator(income,3)
    page_num=request.GET.get('page')
    source=Source.objects.all()
    page_obj=Paginator.get_page(paginator,page_num)
    currency = Userpreference.objects.get(user=request.user).currency
    context={
        'income': income,
        'page_obj':page_obj,
        'c':currency,
        'source': source
     
    }

    return render(request , 'income_index.html',context)

@login_required(login_url='login')
def add_income(request):
    source=Source.objects.all()
    
    context={
        'source': source,
        'values': request.POST }

    if request.method == 'GET':
        return render(request, 'add_income.html', context)

    if request.method=="POST":
        amount=request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request , 'add_income.html',context)

        description=request.POST['description']
        source=request.POST['source']
        date=request.POST['date_expense']
        

        if not description:
            messages.error(request,'Description is Required')
            return render(request , 'add_income.html',context)
    
        UserIncome.objects.create(user=request.user,amount=amount,description=description,source=source,date=date)
        messages.success(request,"Income added successfully")
        return redirect('income')


@login_required(login_url='login')
def income_edit(request,id):
    income=UserIncome.objects.get(pk=id)
    source = Source.objects.all()
    context={
        'income':income,
        'source': source,
        'values': income
    }

    if request.method == "GET":      
        return render(request,'income_edit.html',context)

    if request.method == "POST":
        amount=request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'income_edit.html',context)
            
        source=request.POST['Source']
        description=request.POST['description']
        date=request.POST['date_expense']
       

        if not description:
            messages.error(request,'Description is Required')
            return render(request,'income_edit.html',context)
        
        
        UserIncome.objects.create(user=request.user,amount=amount,source=source,description=description,date=date)
        income.amount=amount
        income.source=source
        income.description=description
        income.date=date
        income.save()


        messages.success(request,"Changed successfully")
        return redirect('income')



@login_required(login_url='login')
def income_delete(request,id):
    income=UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request,"Deleted")
    return redirect('income')

