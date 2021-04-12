
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

def get_subsector(request,sector):
    return JsonResponse({
        'sub_sectors':json.loads(serializers.serialize('json',Category.objects.filter(category_type=sector),ensure_ascii=False))
        })

def get_products(request,sub_sector):
    return JsonResponse({
        'products':json.loads(serializers.serialize('json',SubCategory.objects.filter(category_name=sub_sector),ensure_ascii=False))
        })

class AllReportPage(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context={}
        total_inv_cap_data = []
        ownership_data = []
        education_status_data = []
        companies = Company.objects.all().exclude(main_category='FBPIDI')
        # investment capital
        for company in companies:
            if InvestmentCapital.objects.filter(company=company).exists():
                queryset =  InvestmentCapital.objects.filter(company=company).values('company__name').annotate(
                    machinery = Sum('machinery_cost'),
                    building = Sum('building_cost'),
                    working = Sum('working_capital')
                )
                for invcap in queryset:
                    total_inv_cap_data.append({
                        'company':invcap['company__name'],
                        'total_inv_cap':invcap['machinery']+invcap['working']+invcap['building'],
                        'machinery':invcap['machinery'],
                        'building':invcap['building'],
                        'working':invcap['working'],
                        'sector':company.main_category
                    })
        # form of ownership
        queryset = companies.values('ownership_form').annotate(Count('id')).order_by('ownership_form').exclude(main_category='FBPIDI')
        total_ownership = 0
        for ownership in queryset:
            total_ownership += int(ownership['id__count'])
            ownership_data.append({'label':CompanyDropdownsMaster.objects.get(id=ownership['ownership_form']),
                                    'data':ownership['id__count']})

        # Educational status data
        for company in companies:
            queryset_edu = EducationalStatus.objects.filter(
                company=company,year_edu=get_current_year()).values('education_type').annotate(
                     Sum('male'),Sum('female'),total_edu=Sum('male')+Sum('female') ).order_by('education_type')

            for edu_data in queryset_edu:
                # total_edu += int(edu_data['female__sum']+edu_data['male__sum'])
                education_status_data.append({'company':company.name,'sector':company.main_category,'label':edu_data['education_type'],
                                        'data':int(edu_data['female__sum']+edu_data['male__sum'])})

        context['education_status_data'] = education_status_data
        context['total_ownership'] = total_ownership
        context['ownership_data'] = ownership_data
        context['inv_cap_data'] = total_inv_cap_data
        context['regions']= RegionMaster.objects.all()
        context['sub_sectors']= Category.objects.all()
        context['products'] = SubCategory.objects.all()
        return render(self.request,"admin/report/all_report_page.html",context)
    
    def post(self,*args,**kwargs):
        template_name = "admin/report/all_report_page.html"
        context = {}
        company = Company.objects.all().exclude(main_category='FBPIDI')

        if self.request.POST['region'] != "":
            company = company.filter(company_address__region=self.request.POST['region'])

        if self.request.POST['sector'] != "":
            company = company.filter(main_category=self.request.POST['sector'])
        
        if self.request.POST['sub_sector'] != "":
            company = company.filter(category=self.request.POST['sub_sector'])
        
        if self.request.POST['product'] != "":
            company = company.filter(company_brand__product_type=self.request.POST['product'])
        
        return render(self.request,template_name,context)

 