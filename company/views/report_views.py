
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
from django.db.models import Q
from django.utils import timezone
from django.core import serializers
from django.db.models import Sum,Count


from company.models import *
from product.models import *
from accounts.models import CompanyAdmin,UserProfile

from company.forms import *

today = datetime.datetime.today()
this_year = today.year


class ReportPage(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        return render(self.request,"admin/pages/report.html")
 


class CapitalUtilizationReportSector(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        # capital utilization = (Sum(total_prodn_3yrs)/Sum(actual_produn_capacity*260))*100
        # Sectors,Sub-Sectors and Products
        food_company_list = []
        bev_company_list = []
        pharm_company_list = []
        pp_today=0
        pp_last=0
        pp_prev = 0
        context = {}         
        for company in Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals']):
            production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=this_year)
            production_performance_this_last = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=this_year-1)
            production_performance_this_pre = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=this_year-2)
            for p in production_performance_this_year:
                pp_today += p.production_amount
            
            for p in production_performance_this_last:
                pp_last += p.production_amount

            for p in production_performance_this_pre:
                pp_prev += p.production_amount

            total_apc = 0
            for pco in ProductionCapacity.objects.filter(company=company):
                total_apc += (pco.actual_prdn_capacity*260)

            if company.main_category == "Food":
                if total_apc == 0:
                    food_company_list.append({'company':company.name,'data':(float((pp_today+pp_last+pp_prev)/1))*100})
                else:
                    food_company_list.append({'company':company.name,'data':(float((pp_today+pp_last+pp_prev)/total_apc))*100})
            elif company.main_category == "Beverage":
                if total_apc == 0:
                    bev_company_list.append({'company':company.name,'data':(float((pp_today+pp_last+pp_prev)/1))*100})
                else:
                    bev_company_list.append({'company':company.name,'data':(float((pp_today+pp_last+pp_prev)/total_apc))*100})
            elif company.main_category == "Pharmaceuticals":
                if total_apc == 0:
                    pharm_company_list.append({'company':company.name,'data':(float((pp_today+pp_last+pp_prev)/1))*100})
                else:
                    pharm_company_list.append({'company':company.name,'data':(float((pp_today+pp_last+pp_prev)/total_apc))*100})
        context['food_data'] = food_company_list
        context['bev_data'] = bev_company_list
        context['pharm_data'] = pharm_company_list
        context['flag'] = "capital_utilization"
        return render(self.request,"admin/company/report_page.html",context)

class InvestmentCapitalReportView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        template_name="admin/company/report_page.html"
        context = {}
        total_food_inv_cap = 0
        total_bev_inv_cap = 0
        total_pharm_inv_cap = 0
        for company in Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals']):
            if company.main_category == "Food":
                for invcap in InvestmentCapital.objects.filter(company=company):
                    total_food_inv_cap +=invcap.get_inv_cap()
            elif company.main_category == "Beverage":
                for invcap in InvestmentCapital.objects.filter(company=company):
                    total_bev_inv_cap +=invcap.get_inv_cap()
            elif company.main_category == "Pharmaceuticals":
                for invcap in InvestmentCapital.objects.filter(company=company):
                    total_pharm_inv_cap +=invcap.get_inv_cap()
        context['food_inv_cap'] = total_food_inv_cap
        context['bev_inv_cap'] = total_bev_inv_cap
        context['pharm_inv_cap'] = total_pharm_inv_cap
        context['flag'] = 'inv_cap'
        return render(self.request,template_name,context)


class ProductionCapacityView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        template_name="admin/company/report_page.html"
        context = {}
        labels=[]
        data=[]
        labels2 = []
        data2 = []

        queryset = ProductionCapacity.objects.values('product').annotate(Sum('install_prdn_capacity')).order_by('product')
        for entry in queryset:
            labels.append(SubCategory.objects.get(id=entry['product']).sub_category_name)
            data.append(entry['install_prdn_capacity__sum'])
        
        queryset2 = ProductionCapacity.objects.values('product').annotate(Sum('actual_prdn_capacity')).order_by('product')
        for entry in queryset2:
            labels2.append(SubCategory.objects.get(id=entry['product']).sub_category_name)
            data2.append(entry['actual_prdn_capacity__sum'])

        context['data'] = data
        context['labels'] = labels
        context['data_a'] = data2
        context['labels_a'] = labels2
        context['flag'] = 'production_cap'
        return render(self.request,template_name,context)


class CompanyListForReport(LoginRequiredMixin,ListView):
    model=Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.all().exclude(main_category="FBPIDI")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership").order_by('-id')
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context

class FilterCompanyByMainCategory(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        try:
            if self.kwargs['sector'] == "all":
                return Company.objects.all().exclude(main_category="FBPIDI")
            else:
                return Company.objects.filter(main_category=self.kwargs['sector'])
        except Exception as e:
            return None

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(category_type=self.kwargs['sector'])
        context['sector'] = self.kwargs['sector']
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership")
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context


class FilterCompanyByEstablishedYear(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        try:
            if self.kwargs['option'] == "before_2000":
                return Company.objects.filter(established_yr__lte='2000').exclude(main_category="FBPIDI")
            elif self.kwargs['option'] == "before_2005":
                return Company.objects.filter(established_yr__lte='2005',established_yr__gte='2001').exclude(main_category="FBPIDI")
            elif self.kwargs['option'] == "before_2010":
                return Company.objects.filter(established_yr__lte='2010',established_yr__gte='2006').exclude(main_category="FBPIDI")
            elif self.kwargs['option'] == "after_2011":
                return Company.objects.filter(established_yr__gte='2011').exclude(main_category="FBPIDI")
        except Exception as e:
            return None

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership")
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context

class FilterCompanyCategory(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        try:
            if self.kwargs['category'] == 'Food' or self.kwargs['category'] == 'Beverage' or self.kwargs['category'] == 'Pharmaceuticals':
                return Company.objects.filter(main_category=self.kwargs['category'])
            else:
                return Company.objects.filter( category=Category.objects.get(id=self.kwargs['category']) ) 
        except Exception as e:
            return None
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.kwargs['category'] == 'Food' or self.kwargs['category'] == 'Beverage' or self.kwargs['category'] == 'Pharmaceuticals':
                context['categories'] = Category.objects.filter(category_type=self.kwargs['category'])
            else:
                context['categories'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['category']).category_type)
        except Exception as e:
            return None
        context['sector'] = Category.objects.get(id=self.kwargs['category']).category_type
        context['sub_sector'] = Category.objects.get(id=self.kwargs['category']).category_name
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership")
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context

class FilterByOwnership(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.filter(ownership_form=self.kwargs['ownership_form'])
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership")
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context

class FilterByExpansionPlan(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.all().exclude(expansion_plan__icontains="No")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership")
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context

class FilterByTradeLicense(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.all().exclude(trade_license__in=['',"None"])
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership")
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context

class FilterCertificate(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.filter(main_category__in=['Food','Beverage','Pharmaceuticals'])
                
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership")
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context

class FilterByWorkingHour(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.filter(working_hours=self.kwargs['working_hour'])
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['ownership'] = CompanyDropdownsMaster.objects.filter(chk_type ="Forms of Ownership")
        context['working_hour'] = CompanyDropdownsMaster.objects.filter(chk_type ="Working hours")
        return context


class NumberOfEmployees(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        total_perm_emp = 0
        total_temp_emp=0
        total_for_emp=0
        food_data=[]
        bev_data=[]
        pharm_data=[]
        for company in Company.objects.filter(main_category__in=['Food','Beverage','Pharmaceuticals']):
            employees_perm = Employees.objects.filter(company=company,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(company=company,employment_type__icontains="Temporary")
            employees_foreign = Employees.objects.filter(company=company,employment_type__icontains="Foreign")
            
            for ep in employees_perm:
                total_perm_emp += (ep.male+ep.female)
            
            for et in employees_temp:
                total_temp_emp += (et.male+et.female)
            
            for ef in employees_foreign:
                total_for_emp += (ef.male+ef.female)

            total = total_perm_emp+total_temp_emp+total_for_emp

            if company.main_category == "Food":
                food_data.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
            elif company.main_category == "Beverage":
                bev_data.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
            elif company.main_category == "Pharmaceuticals":
                pharm_data.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        context = {
            'food_data':food_data,'bev_data':bev_data,'pharm_data':pharm_data,
            'flag':"num_employees"
        }
        return render(self.request,'admin/company/report_page.html',context)

class NumberOfEmployeesFemale(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        total_perm_emp = 0
        total_temp_emp=0
        food_data=[]
        bev_data=[]
        pharm_data=[]
        for company in Company.objects.filter(main_category__in=['Food','Beverage','Pharmaceuticals']):
            employees_perm = Employees.objects.filter(company=company,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(company=company,employment_type__icontains="Temporary")
            
            for ep in employees_perm:
                total_perm_emp += (ep.female)
            
            for et in employees_temp:
                total_temp_emp += (et.female)
            
            total = total_perm_emp+total_temp_emp

            if company.main_category == "Food":
                food_data.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
            elif company.main_category == "Beverage":
                bev_data.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
            elif company.main_category == "Pharmaceuticals":
                pharm_data.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        context = {
            'food_data':food_data,'bev_data':bev_data,'pharm_data':pharm_data,
            'flag':"num_employees_female"
        }
        return render(self.request,'admin/company/report_page.html',context)


class NumberOfEmployeesForeign(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        total_for_emp_m=0
        total_for_emp_f=0
        food_data=[]
        bev_data=[]
        pharm_data=[]
        for company in Company.objects.filter(main_category__in=['Food','Beverage','Pharmaceuticals']):
            employees_foreign = Employees.objects.filter(company=company,employment_type__icontains="Foreign")
                        
            for ef in employees_foreign:
                total_for_emp_m += (ef.male)
                total_for_emp_f += (ef.female)

            total = total_for_emp_m+total_for_emp_f

            if company.main_category == "Food":
                food_data.append({'company':company.name,'data':total,'for_male':total_for_emp_m,'for_female':total_for_emp_f})
            elif company.main_category == "Beverage":
                bev_data.append({'company':company.name,'data':total,'for_male':total_for_emp_m,'for_female':total_for_emp_f})
            elif company.main_category == "Pharmaceuticals":
                pharm_data.append({'company':company.name,'data':total,'for_male':total_for_emp_m,'for_female':total_for_emp_f})
        context = {
            'food_data':food_data,'bev_data':bev_data,'pharm_data':pharm_data,
            'flag':"num_employees_foreign"
        }
        return render(self.request,'admin/company/report_page.html',context)

class ExportCSV(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            companies=""
            if self.kwargs['option'] == "main_category":
                if self.kwargs['category'] == "all":
                    companies = Company.objects.select_related().all().exclude(main_category="FBPIDI")
                else:
                    companies = Company.objects.select_related().filter(main_category=self.kwargs['category'])
            elif self.kwargs['option'] == "sub_category":
                companies = Company.objects.filter(
                    category=Category.objects.get(category_name=self.kwargs['category'])
                )
            response = HttpResponse(content_type='text/csv',charset="utf-8")  
            response['Content-Disposition'] = 'attachment; filename="COMPANY_DATA.csv"'  
            writer = csv.writer(response)
            writer.writerow(['name','Sector','Category','Products','Ownership Form','Established Year'])
            for company in companies:
                writer.writerow([
                    company.name,company.main_category,get_categories(company),company.company_product.all().count(),
                    company.ownership_form.name,company.established_yr
                ])
            return response             
        except Exception as e:
            messages.warning(self.request,e)
            return redirect("admin:company_list_report")

def get_categories(company):
    str_cat = ""
    for cat in company.category.all():
        str_cat+=cat.category_name+", "
    return str_cat