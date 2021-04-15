
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


class ProjectReport(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        projects = InvestmentProject.objects.all()
        # form of ownership
        queryset = projects.values('ownership_form').annotate(Count('id')).order_by('ownership_form') 
        total_ownership = 0
        ownership_data = []
        for ownership in queryset:
            total_ownership += int(ownership['id__count'])
            try:
                ownership_data.append({'label':CompanyDropdownsMaster.objects.get(id=ownership['ownership_form']),
                                    'data':ownership['id__count']})
            except CompanyDropdownsMaster.DoesNotExist:
                ownership_data= []
        total_inv_cap_data = []
        for project in projects:
            if InvestmentCapital.objects.filter(project=project).exists():
                queryset =  InvestmentCapital.objects.filter(project=project).values('project__project_name').annotate(
                    machinery = Sum('machinery_cost'),
                    building = Sum('building_cost'),
                    working = Sum('working_capital')
                )
                for invcap in queryset:
                    total_inv_cap_data.append({
                        'project':invcap['project__project_name'],
                        'total_inv_cap':invcap['machinery']+invcap['working']+invcap['building'],
                        'machinery':invcap['machinery'],
                        'building':invcap['building'],
                        'working':invcap['working'],
                        'sector':project.sector
                    })
        queryset_classificaion = projects.values('project_classification').annotate(Count('id')).order_by('project_classification') 
        total_classification = 0
        classification_data = []
        for ownership in queryset_classificaion:
            total_classification += int(ownership['id__count'])
            try:
                classification_data.append({'label':ProjectDropDownsMaster.objects.get(id=ownership['project_classification']),
                                    'data':ownership['id__count']})
            except ProjectDropDownsMaster.DoesNotExist:
                classification_data= []

        context['classification_data'] = classification_data
        context['total_class'] = total_classification
        context['inv_cap_data'] = total_inv_cap_data
        context['ownership_data'] = ownership_data
        context['total_ownership'] = total_ownership
        context['projects'] = projects
        return render(self.request,"admin/report/all_report_project.html",context)