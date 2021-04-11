
import json
import csv
import datetime

from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,ListView,View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core import serializers
from django.db.models import Sum,Count,OuterRef,Exists,Q,F,Avg

from company.models import *
from product.models import *
from accounts.models import CompanyAdmin,UserProfile

from company.forms import *

def get_current_year():
    current_year = 0
    gc_year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day

    if month <= 7 and day < 8 or month <= 7:
        current_year = gc_year-9
    else:
        current_year = gc_year - 8
    return current_year


class AllReportPage(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context={}
        context['regions']= RegionMaster.objects.all()
        context['sub_sectors']= Category.objects.all()
        context['products'] = SubCategory.objects.all()
        return render(self.request,"admin/report/all_report_page.html",context)

 