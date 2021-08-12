from django.db import models
from django.db.models.base import ModelState
from django.db.models.expressions import OrderBy
from django.http import request
from django.shortcuts import redirect
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    amount=models.FloatField()
    date=models.DateField(default=now)
    description=models.TextField()
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)
    category=models.CharField(max_length=255)

    def __str__(self):
        return self.category


class Category(models.Model):
    name=models.CharField(max_length=255)

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name
