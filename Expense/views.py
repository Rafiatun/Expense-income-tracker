from django.core.checks import messages
from Expense.models import Category
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse,HttpResponse
from userpreferences.models import Userpreference
import datetime
import csv

def search_expense(request):
    if request.method=="POST":
        search_string=json.loads(request.body).get('searchText')
        expenses=Expense.objects.filter(
            amount__istartswith=search_string ,user=request.user) | Expense.objects.filter(
            date__istartswith=search_string ,user=request.user) | Expense.objects.filter(
            description__icontains=search_string ,user=request.user) | Expense.objects.filter(
            category__icontains=search_string ,user=request.user)


        data=expenses.values()
        return JsonResponse(list(data),safe=False)


@login_required(login_url='login')
def home(request):
    categories=Category.objects.all()
    expense=Expense.objects.filter(user=request.user)
    paginator=Paginator(expense,3)
    page_num=request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_num)
    currency = Userpreference.objects.get(user=request.user).currency
    context={
        'expense': expense,
        'page_obj':page_obj,
        'c':currency
     
    }

    return render(request , 'index.html',context)

@login_required(login_url='login')
def add_expense(request):
    categories=Category.objects.all()
    
    context={
        'categories': categories,
        'values': request.POST }

    if request.method == 'GET':
        return render(request, 'add_expense.html', context)

    if request.method=="POST":
        amount=request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request , 'add_expense.html',context)

        description=request.POST['description']
        date=request.POST['date_expense']
        category=request.POST['Category']

        if not description:
            messages.error(request,'Description is Required')
            return render(request , 'add_expense.html',context)
    
        Expense.objects.create(user=request.user,amount=amount,description=description,category=category,date=date)
        messages.success(request,"Expense saved successfully")
        return redirect('home')

def expense_edit(request,id):
    expense=Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context={
        'expense':expense,
        'categories': categories,
        'values': expense
    }

    if request.method == "GET":      
        return render(request,'expense_edit.html',context)
    if request.method == "POST":
        amount=request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'expense_edit.html',context)

        description=request.POST['description']
        date=request.POST['date_expense']
        category=request.POST['Category']

        if not description:
            messages.error(request,'Description is Required')
            return render(request,'expense_edit.html',context)
        
        
        Expense.objects.create(user=request.user,amount=amount,description=description,category=category,date=date)
        expense.user=request.user
        expense.amount=amount
        expense.description=description
        expense.category=category
        expense.date=date
        expense.save()


        messages.success(request,"Expense saved successfully")
        return redirect('home')



def expense_delete(request,id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,"Deleted")
    return redirect('home')


def expense_category_summary(request):
    today_date=datetime.date.today()
    six_mon_ago=today_date - datetime.timedelta(days=30*6)
    expenses=Expense.objects.filter(user=request.user,
        date__gte=six_mon_ago,date__lte=today_date)

    final_rep= {}

    def get_category(expenses):
        return expenses.category

    category_list=list(set(map(get_category,expenses)))

    def get_cat_amount(category):
        amount=0
        filtered_by_category=expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            final_rep[y]=get_cat_amount(y)

    return JsonResponse({'expense_category_data': final_rep},safe=False)


def stats_view(request):
    return render(request,'stats.html')

def export_csv(request):
    response=HttpResponse(content_type="text/csv")
    response['Content-disposition']='attachment;filename=Expenses'+str(datetime.datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount','Category','Description','Date'])
    expenses=Expense.objects.filter(user=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.category,expense.description,expense.date])

    return response
