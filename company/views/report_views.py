
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
        # capital utilization = (Sum(total_prodn_thisyrs)/Sum(actual_produn_capacity*260))*100
        # Sectors,Sub-Sectors and Products
        capital_util_data = []
        pp_today=0
        pp_last=0
        pp_prev = 0
        context = {}         
        companies = None
        if self.kwargs['option'] == 'by_sector':
            if self.kwargs['sector'] == "all":
                companies = Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals'])
                context['sub_sectors'] = Category.objects.all()
            else:
                companies = Company.objects.filter(main_category=self.kwargs['sector'])
                context['sub_sectors'] = Category.objects.filter(category_type=self.kwargs['sector'])
            context['title'] = self.kwargs['sector'] 
            context['sector'] = self.kwargs['sector'] 
        elif self.kwargs['option'] == 'by_sub_sector':
            companies = Company.objects.filter(category=self.kwargs['sector'])
            context['sub_sectors'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['sector']).category_type)
            context['title'] = Category.objects.get(id=self.kwargs['sector']).category_name
            context['sector'] = Category.objects.get(id=self.kwargs['sector']).category_type 
            context['products'] = SubCategory.objects.filter(category_name=self.kwargs['sector'])
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sector']).category_name
        elif self.kwargs['option'] == 'by_product':
            product = SubCategory.objects.get(id=self.kwargs['sector'])
            companies = Company.objects.filter(category=product.category_name)
            context['sub_sectors'] = Category.objects.filter(category_type=product.category_name.category_type)
            context['title'] = product.sub_category_name
            context['sector'] =  product.category_name.category_type 
            context['products'] = SubCategory.objects.filter(category_name=product.category_name)
            context['sub_sector'] =  product.category_name.category_name
        if companies == None:
            context['flag'] = "capital_utilization"
            context['title'] = self.kwargs['sector'] 
            messages.warning(self.request,"Please Fix Your Request,There is issue in the request")
            return render(self.request,"admin/company/report_page.html",context)
        else:
            for company in companies:
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

                # if company.main_category == "Food":
                if total_apc == 0:
                    capital_util_data.append({'company':company.name,'data':(float((pp_today)/1))*100})
                else:
                    capital_util_data.append({'company':company.name,'data':(float((pp_today)/total_apc))*100})
            context['capital_util_data'] = capital_util_data
            context['flag'] = "capital_utilization"
            
            return render(self.request,"admin/company/report_page.html",context)

class ChangeInCapitalUtilization(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        # capital utilization = (Sum(total_prodn_3-total_prodn_1yrs)/Sum(actual_produn_capacity*260))*100
        # Sectors,Sub-Sectors and Products
        change_capital_util_data = []
        pp_today=0
        pp_prev = 0
        context = {}         
        companies = None
        if self.kwargs['option'] == 'by_sector':
            if self.kwargs['sector'] == "all":
                companies = Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals'])
                context['sub_sectors'] = Category.objects.all()
            else:
                companies = Company.objects.filter(main_category=self.kwargs['sector'])
                context['sub_sectors'] = Category.objects.filter(category_type=self.kwargs['sector'])
            context['title'] = self.kwargs['sector'] 
            context['sector'] = self.kwargs['sector'] 
        elif self.kwargs['option'] == 'by_sub_sector':
            companies = Company.objects.filter(category=self.kwargs['sector'])
            context['sub_sectors'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['sector']).category_type)
            context['title'] = Category.objects.get(id=self.kwargs['sector']).category_name
            context['sector'] = Category.objects.get(id=self.kwargs['sector']).category_type 
            context['products'] = SubCategory.objects.filter(category_name=self.kwargs['sector'])
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sector']).category_name
        elif self.kwargs['option'] == 'by_product':
            product = SubCategory.objects.get(id=self.kwargs['sector'])
            companies = Company.objects.filter(category=product.category_name)
            context['sub_sectors'] = Category.objects.filter(category_type=product.category_name.category_type)
            context['title'] = product.sub_category_name
            context['sector'] =  product.category_name.category_type 
            context['products'] = SubCategory.objects.filter(category_name=product.category_name)
            context['sub_sector'] =  product.category_name.category_name

        if companies == None:
            context['flag'] = "change_capital_utilization"
            context['title'] = self.kwargs['sector'] 
            messages.warning(self.request,"Please Fixe Your Request,There is issue in the request")
            return render(self.request,"admin/company/report_page.html",context)
        else:
            for company in companies:
                production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=this_year)
                production_performance_this_pre = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=this_year-1)
                for p in production_performance_this_year:
                    pp_today += p.production_amount
                
                for p in production_performance_this_pre:
                    pp_prev += p.production_amount

                total_apc = 0
                for pco in ProductionCapacity.objects.filter(company=company):
                    total_apc += (pco.actual_prdn_capacity*260)

                if total_apc == 0:
                    change_capital_util_data.append({'company':company.name,'data':float((pp_prev-pp_today)/1)})
                else:
                    change_capital_util_data.append({'company':company.name,'data':float((pp_prev-pp_today)/total_apc)})
            context['change_capital_util_data'] = change_capital_util_data
            context['flag'] = "change_capital_utilization"
            
            return render(self.request,"admin/company/report_page.html",context)

class AverageExtractionRate(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        products = None
        average_extraction_data = []
        context = {}
        if self.kwargs['product'] == "all":
            products = SubCategory.objects.all()
            context['title']= "All Products"
        else:
            products = SubCategory.objects.filter(id=self.kwargs['product'])
            context['title']= SubCategory.objects.get(id=self.kwargs['product']).sub_category_name
        extn_rate = 0
        index = 1
        for product in products:
            pcapacity = ProductionCapacity.objects.filter(product=product)
            for pcd in pcapacity:
                extn_rate+=pcd.extraction_rate
                index += 1
            average_extraction_data.append({'product':product.sub_category_name,'data':extn_rate/pcapacity.count(),})
        context['extn_data']=average_extraction_data
        context['flag'] = "extraction_data"
        context['products'] = SubCategory.objects.all()
        return render(self.request,"admin/company/report_page.html",context)


class GrossValueOfProduction(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        # Gross value of production = (Sum(total_prodn_thisyrs)/Sum(actual_produn_capacity*260))*100
        # Sectors,Sub-Sectors and Products
        gvp_data = []
        pp_today=0
        pp_last=0
        pp_prev = 0
        context = {}         
        companies = None
        if self.kwargs['option'] == 'by_sector':
            if self.kwargs['sector'] == "all":
                companies = Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals'])
                context['sub_sectors'] = Category.objects.all()
            else:
                companies = Company.objects.filter(main_category=self.kwargs['sector'])
                context['sub_sectors'] = Category.objects.filter(category_type=self.kwargs['sector'])
                context['title'] = self.kwargs['sector'] 
                context['sector'] = self.kwargs['sector']
        elif self.kwargs['option'] == 'by_sub_sector':
            companies = Company.objects.filter(category=self.kwargs['sector'])
            context['sub_sectors'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['sector']).category_type)
            context['title'] = Category.objects.get(id=self.kwargs['sector']).category_name
            context['sector'] = Category.objects.get(id=self.kwargs['sector']).category_type 
            context['products'] = SubCategory.objects.filter(category_name=self.kwargs['sector'])
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sector']).category_name
        elif self.kwargs['option'] == 'by_product':
            product = SubCategory.objects.get(id=self.kwargs['sector'])
            companies = Company.objects.filter(category=product.category_name)
            context['sub_sectors'] = Category.objects.filter(category_type=product.category_name.category_type)
            context['title'] = product.sub_category_name
            context['sector'] =  product.category_name.category_type 
            context['products'] = SubCategory.objects.filter(category_name=product.category_name)
            context['sub_sector'] =  product.category_name.category_name

        if companies == None:
            context['flag'] = "gross_vp_data"
            context['title'] = self.kwargs['sector'] 
            messages.warning(self.request,"Please Fixe Your Request,There is issue in the request")
            return render(self.request,"admin/company/report_page.html",context)
        else:
            for company in companies:
                production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=this_year)
                production_performance_this_last = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=this_year-1)
                production_performance_this_pre = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=this_year-2)
                for p in production_performance_this_year:
                    pp_today += p.sales_value
                
                for p in production_performance_this_last:
                    pp_last += p.sales_value

                for p in production_performance_this_pre:
                    pp_prev += p.sales_value
                gvp_data.append({'company':company.name,'data':float(pp_today+pp_last+pp_prev),'gvp_data':{
                    'this_yr':pp_today,'last_yr':pp_last,'prev_yr':pp_prev
                } })

            context['gvp_data'] = gvp_data
            context['flag'] = "gross_vp_data"
            context['years'] = {'this_year':this_year,'last_year':this_year-1,'prev_year':this_year-2}
            
            return render(self.request,"admin/company/report_page.html",context)


class AverageUnitPrice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        products = None
        average_price_data = []
        context = {}
        if self.kwargs['product'] == "all":
            products = SubCategory.objects.all()
            context['title']= "All Products"
        else:
            products = SubCategory.objects.filter(id=self.kwargs['product'])
            context['title']= SubCategory.objects.get(id=self.kwargs['product']).sub_category_name
        price_total = 0
        prodn_total = 0
        for product in products:
            pup = 0
            spp = ProductionAndSalesPerformance.objects.filter(product=product,activity_year=this_year)
            if spp.exists():
                for aup in spp:
                    price_total = aup.sales_value
                    prodn_total = aup.sales_amount
                
                if prodn_total == 0:
                    pup = float(price_total/1)
                else:
                    pup = float(price_total/prodn_total)

            average_price_data.append({'product':product.sub_category_name,'data':pup})
        context['price_data']=average_price_data
        context['flag'] = "unit_price_data"
        context['products'] = SubCategory.objects.all()
        print(context)
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
        products = None
        context = {}         
        if self.kwargs['product'] == "all":
            products = SubCategory.objects.all()
            context['title']= "All Products"
        else:
            products = SubCategory.objects.filter(id=self.kwargs['product'])
            context['title']= SubCategory.objects.get(id=self.kwargs['product']).sub_category_name

        total_data = []
        prodn_total = 0
        actual_total = 0
        for product in products:
            for aup in ProductionCapacity.objects.filter(product=product):
                prodn_total+=float(aup.install_prdn_capacity*260)
                actual_total+=float(aup.actual_prdn_capacity*260)

            total_data.append({'product':product.sub_category_name,'total_data':{'installed':prodn_total,'actual':actual_total},'data':prodn_total+actual_total})
        context['produn_data']=total_data
        context['products'] = SubCategory.objects.all()
        context['flag'] = 'production_cap'
        return render(self.request,"admin/company/report_page.html",context)
  
class InputAvailablity(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        products = None
        context = {}         
        if self.kwargs['product'] == "all":
            products = SubCategory.objects.all()
            context['title']= "All Products"
        else:
            products = SubCategory.objects.filter(id=self.kwargs['product'])
            context['title']= SubCategory.objects.get(id=self.kwargs['product']).sub_category_name

        total_data = []
        supply = 0
        demand = 0
        av_inp = 0
        for product in products:
            inp_dem_sups = InputDemandSupply.objects.filter(product=product)
            if inp_dem_sups.exists():
                for aup in inp_dem_sups:
                    demand += aup.demand
                    supply += aup.supply

                if demand == 0:
                    av_inp=float(supply/1)
                else:
                    av_inp=float(supply/demand)
                
                total_data.append({'product':product.sub_category_name,'data':av_inp*100,'unit':product.uom})
        context['avalilable_input']=total_data
        context['flag'] = "avalilable_input"
        context['products'] = SubCategory.objects.all()
        return render(self.request,"admin/company/report_page.html",context)

class ShareLocalInputs(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        products = None
        context = {}         
        if self.kwargs['product'] == "all":
            products = SubCategory.objects.all()
            context['title']= "All Products"
        else:
            products = SubCategory.objects.filter(id=self.kwargs['product'])
            context['title']= SubCategory.objects.get(id=self.kwargs['product']).sub_category_name

        total_data = []
        local_share = 0
        for product in products:
            ann_inp_need = AnnualInputNeed.objects.filter(product=product)
            if ann_inp_need.exists():
                for aup in ann_inp_need:
                    local_share += aup.local_input
                
                total_data.append({'product':product.sub_category_name,'data':local_share,'unit':product.uom})
        context['input_share']=total_data
        context['flag'] = "input_share"
        context['products'] = SubCategory.objects.all()
        return render(self.request,"admin/company/report_page.html",context)


class CompanyListForReport(LoginRequiredMixin,ListView):
    model=Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.all().exclude(main_category="FBPIDI")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
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
        return context

class OwnershipReport(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        ownership_data = []
        context = {}
        template_name = "admin/company/report_page.html"
        company = Company.objects.all().exclude(main_category="FBPIDI")
        queryset = Company.objects.values('ownership_form').annotate(Count('id')).order_by('ownership_form').exclude(main_category='FBPIDI')
        total = 0
        for ownership in queryset:
            total += int(ownership['id__count'])
            # label.append(CompanyDropdownsMaster.objects.get(id=ownership['ownership_form']))
            # data.append(ownership['id__count'])
            # percent.append(float(ownership['id__count']/queryset.count())*100)
            ownership_data.append({'label':CompanyDropdownsMaster.objects.get(id=ownership['ownership_form']),
                                    'data':ownership['id__count']})
        context['total'] = total
        context['ownership_data'] = ownership_data
        context['flag'] = 'ownership_data'
        return render(self.request,template_name,context)

class FilterByExpansionPlan(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.all().exclude(expansion_plan__icontains="No")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FilterByTradeLicense(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.all().exclude(trade_license__in=['',"None"])
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FilterCertificate(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies_for_report.html"

    def get_queryset(self):
        return Company.objects.filter(main_category__in=['Food','Beverage','Pharmaceuticals'])
                
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FilterByWorkingHour(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        working_hour_data = []
        context = {}
        template_name = "admin/company/report_page.html"
        queryset = Company.objects.values('working_hours').annotate(Count('id')).order_by('working_hours').exclude(main_category='FBPIDI')
        total = 0
        for working_hour in queryset:
            total += int(working_hour['id__count'])
            working_hour_data.append({'label':CompanyDropdownsMaster.objects.get(id=working_hour['working_hours']),
                                    'data':working_hour['id__count']})
        context['total'] = total
        context['working_hour_data'] = working_hour_data
        context['flag'] = 'working_hour_data'
        return render(self.request,template_name,context)
         

class NumberofIndustriesByOption(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        context['flag'] = "company_count"
        template_name = "admin/company/companies_for_report.html"
        if self.kwargs['option'] == 'research':
            context['data'] = Company.objects.all().exclude(conducted_research='').exclude(main_category='FBPIDI').count()
            context['label'] = "Number of Industries Who Conducted Research"
        elif self.kwargs['option'] == 'test_param':
            context['data'] = Company.objects.all().exclude(outsourced_test_param='').exclude(main_category='FBPIDI').count()
            context['label'] = "Number of Industries Who Out Sourced Test Parameter"
        elif self.kwargs['option'] == 'new_product':
            context['data'] =  Company.objects.all().exclude(new_product_developed='').exclude(main_category='FBPIDI').count()
            context['label'] = "Number of Industries Who Developed New Product"
        
        return render(self.request,template_name,context)



class NumberOfEmployees(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        total_perm_emp = 0
        total_temp_emp=0
        emp_data_total=[]
        companies = None
        context = {}
        if self.kwargs['option'] == 'by_sector':
            if self.kwargs['sector'] == "all":
                companies = Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals'])
                context['sub_sectors'] = Category.objects.all()
            else:
                companies = Company.objects.filter(main_category=self.kwargs['sector'])
                context['sub_sectors'] = Category.objects.filter(category_type=self.kwargs['sector'])
            context['title'] = self.kwargs['sector']
            context['sector'] = self.kwargs['sector'] 
        elif self.kwargs['option'] == 'by_sub_sector':
            companies = Company.objects.filter(category=self.kwargs['sector'])
            context['sub_sectors'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['sector']).category_type)
            context['title'] = Category.objects.get(id=self.kwargs['sector']).category_name
            context['sector'] = Category.objects.get(id=self.kwargs['sector']).category_type 
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sector']).category_name
        
        if companies == None:
            context['flag'] = "num_employees"
            context['title'] = self.kwargs['sector'] 
            messages.warning(self.request,"Please Fix Your Request,There is issue in the request")
            return render(self.request,"admin/company/report_page.html",context)
        else:
            for company in companies:
                employees_perm = Employees.objects.filter(company=company,employment_type__icontains="Permanent")
                employees_temp = Employees.objects.filter(company=company,employment_type__icontains="Temporary")
                
                for ep in employees_perm:
                    total_perm_emp += (ep.male+ep.female)
                
                for et in employees_temp:
                    total_temp_emp += (et.male+et.female)
                
                total = total_perm_emp+total_temp_emp
                emp_data_total.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
            context['total_emp_data'] = emp_data_total
            context['flag'] = "num_employees"
            return render(self.request,'admin/company/report_page.html',context)

class NumberOfEmployeesFemale(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        total_perm_emp = 0
        total_temp_emp=0
        femal_emp_data=[]
        companies = None
        context = {}
        if self.kwargs['option'] == 'by_sector':
            if self.kwargs['sector'] == "all":
                companies = Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals'])
                context['sub_sectors'] = Category.objects.all()
            else:
                companies = Company.objects.filter(main_category=self.kwargs['sector'])
                context['sub_sectors'] = Category.objects.filter(category_type=self.kwargs['sector'])
            context['title'] = self.kwargs['sector']
            context['sector'] = self.kwargs['sector'] 
        elif self.kwargs['option'] == 'by_sub_sector':
            companies = Company.objects.filter(category=self.kwargs['sector'])
            context['sub_sectors'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['sector']).category_type)
            context['title'] = Category.objects.get(id=self.kwargs['sector']).category_name
            context['sector'] = Category.objects.get(id=self.kwargs['sector']).category_type 
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sector']).category_name
        if companies == None:
            context['flag'] = "num_employees"
            context['title'] = self.kwargs['sector'] 
            messages.warning(self.request,"Please Fix Your Request,There is issue in the request")
            return render(self.request,"admin/company/report_page.html",context)
        else:
            for company in companies:
                employees_perm = Employees.objects.filter(company=company,employment_type__icontains="Permanent")
                employees_temp = Employees.objects.filter(company=company,employment_type__icontains="Temporary")
                
                for ep in employees_perm:
                    total_perm_emp += (ep.female)
                
                for et in employees_temp:
                    total_temp_emp += (et.female)
                
                total = total_perm_emp+total_temp_emp
                femal_emp_data.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
                
            context['total_emp_data'] = femal_emp_data
            context['flag'] = "num_employees_female"
            return render(self.request,'admin/company/report_page.html',context)


class NumberOfEmployeesForeign(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        total_for_emp_m=0
        total_for_emp_f=0
        for_emp_data=[]
        companies = None
        context = {}
        if self.kwargs['option'] == 'by_sector':
            if self.kwargs['sector'] == "all":
                companies = Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals'])
                context['sub_sectors'] = Category.objects.all()
            else:
                companies = Company.objects.filter(main_category=self.kwargs['sector'])
                context['sub_sectors'] = Category.objects.filter(category_type=self.kwargs['sector'])
            context['title'] = self.kwargs['sector']
            context['sector'] = self.kwargs['sector'] 
        elif self.kwargs['option'] == 'by_sub_sector':
            companies = Company.objects.filter(category=self.kwargs['sector'])
            context['sub_sectors'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['sector']).category_type)
            context['title'] = Category.objects.get(id=self.kwargs['sector']).category_name
            context['sector'] = Category.objects.get(id=self.kwargs['sector']).category_type 
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sector']).category_name
        if companies == None:
            context['flag'] = "num_employees_foreign"
            context['title'] = self.kwargs['sector'] 
            messages.warning(self.request,"Please Fix Your Request,There is issue in the request")
            return render(self.request,"admin/company/report_page.html",context)
        else:
            for company in companies:
                employees_foreign = Employees.objects.filter(company=company,employment_type__icontains="Foreign")
                            
                for ef in employees_foreign:
                    total_for_emp_m += (ef.male)
                    total_for_emp_f += (ef.female)

                total = total_for_emp_m+total_for_emp_f
                for_emp_data.append({'company':company.name,'data':total,'for_male':total_for_emp_m,'for_female':total_for_emp_f})
                 
            context['for_emp_data'] = for_emp_data
            context['flag'] = "num_employees_foreign"
            return render(self.request,'admin/company/report_page.html',context)

class NumberOfJobsCreatedBySubSector(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        job_created_data=[]
        companies = None
        context = {}
        if self.kwargs['option'] == 'by_sector':
            if self.kwargs['sector'] == "all":
                companies = Company.objects.filter(main_category__in=["Food",'Beverage','Pharmaceuticals'])
                context['sub_sectors'] = Category.objects.all()
            else:
                companies = Company.objects.filter(main_category=self.kwargs['sector'])
                context['sub_sectors'] = Category.objects.filter(category_type=self.kwargs['sector'])
            context['title'] = self.kwargs['sector']
            context['sector'] = self.kwargs['sector'] 
        elif self.kwargs['option'] == 'by_sub_sector':
            companies = Company.objects.filter(category=self.kwargs['sector'])
            context['sub_sectors'] = Category.objects.filter(category_type=Category.objects.get(id=self.kwargs['sector']).category_type)
            context['title'] = Category.objects.get(id=self.kwargs['sector']).category_name
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sector']).category_name
            context['sector'] = Category.objects.get(id=self.kwargs['sector']).category_type 
        if companies == None:
            context['flag'] = "num_jobs_created"
            context['title'] = self.kwargs['sector'] 
            messages.warning(self.request,"Please Fix Your Request,There is issue in the request")
            return render(self.request,"admin/company/report_page.html",context)
        else:
            for company in companies:
                jobs_created_temp = JobOpportunities.objects.filter(company=company,job_type__icontains="Temporary")
                jobs_created_permanent = JobOpportunities.objects.filter(company=company,job_type__icontains="Permanent")
               
                temp_male = 0
                temp_female = 0
                for temp in jobs_created_temp:
                    temp_female += temp.female
                    temp_male += temp.male

                permanent_male = 0
                permanent_female = 0
                for p in jobs_created_permanent:
                    permanent_male += p.male
                    permanent_female += p.female

                job_created_data.append({'company':company.name,'data':{
                    'temporary_male':temp_male,'temporary_female':temp_female,
                    'permanent_male':permanent_male,'permanent_female':permanent_female
                }})

            context['job_created_data'] = job_created_data 
            context['flag'] = "num_jobs_created"
            return render(self.request,'admin/company/report_page.html',context)

class EduLevelofEmployees(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        education_status_data = []
        context = {}
        template_name = "admin/company/report_page.html"
        queryset = EducationalStatus.objects.values('education_type').annotate(Sum('male'),Sum('female')).order_by('education_type')
        total = 0
        for edu_data in queryset:
            total += int(edu_data['female__sum']+edu_data['male__sum'])
            education_status_data.append({'label':edu_data['education_type'],
                                    'data':int(edu_data['female__sum']+edu_data['male__sum'])})
        print(total)
        context['total'] = total
        context['education_status_data'] = education_status_data
        context['flag'] = 'education_status_data'
        return render(self.request,template_name,context)
        template_name = "admin/company/companies_for_report.html"


class NumWomenInPosition(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        women_in_pson_level = []
        context = {}
        template_name = "admin/company/report_page.html"
        queryset = FemalesInPosition.objects.all()
        # (Sum('high_position'),Sum('med_position'))
        in_med = 0
        in_high = 0
        total = 0
        for women_data in queryset:
            in_high += int(women_data.high_position)
            in_med += int(women_data.med_position)
        total = int(in_high+in_med)
        women_in_pson_level.append({'label':'Med Level Positions','data':in_med})
        women_in_pson_level.append({'label':'Higher Level Positions','data':in_high})
        context['total'] = total
        context['women_in_pson_level'] = women_in_pson_level
        context['flag'] = 'women_in_pson_level'
        print(context)
        return render(self.request,template_name,context)

class CompanyCertificationData(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        certification_data = []
        context = {}
        template_name = "admin/company/report_page.html"
        company = Company.objects.all().exclude(main_category="FBPIDI")
        queryset = Company.objects.values('certification').annotate(Count('id')).order_by('certification').exclude(main_category='FBPIDI')
        #  [{'certification': 21, 'id__count': 1}, 
        #  {'certification': 20, 'id__count': 1}, 
        #  {'certification': 18, 'id__count': 1}, 
        #  {'certification': 16, 'id__count': 1}, 
        #  {'certification': 13, 'id__count': 1}]
        total = 0
        for certification in queryset:
            total+= int(certification['id__count'])
            certification_data.append({'label':CompanyDropdownsMaster.objects.get(id=certification['certification']).name,
                                    'data':certification['id__count']})
        context['total'] = total
        context['certification_data'] = certification_data
        context['flag'] = 'certification_data'
        return render(self.request,template_name,context)
        template_name = "admin/company/companies_for_report.html"

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