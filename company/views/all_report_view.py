
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
        companies = Company.objects.all().exclude(main_category='FBPIDI').order_by('id')
        products = SubCategory.objects.all()
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
        queryset = companies.values('ownership_form').annotate(Count('id')).order_by('ownership_form') 
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
            total_edu = 0
            fem_edu = 0
            male_edu = 0
            for edu_data in queryset_edu:
                fem_edu += edu_data['female__sum']
                male_edu += edu_data['male__sum']
                # total_edu += int(+)
                education_status_data.append({'company':company.name,'sector':company.main_category,'label':edu_data['education_type'],
                                        'data':int(edu_data['female__sum']+edu_data['male__sum'])})
        total_edu = fem_edu+male_edu
        queryset_cert = companies.values('certification').annotate(Count('id')).order_by('certification') 
        certification_data = []
        total_certification = 0
        for certification in queryset_cert:
            total_certification+= int(certification['id__count'])
            certification_data.append({'label':CompanyDropdownsMaster.objects.get(id=certification['certification']).name,
                                    'data':certification['id__count']})
        
        queryset_mgmt = companies.values('management_tools').annotate(Count('id')).order_by('management_tools') 
        management_tool_data = []
        total_managment = 0
        for management_tool in queryset_mgmt:
            total_managment+= int(management_tool['id__count'])
            management_tool_data.append({'label':CompanyDropdownsMaster.objects.get(id=management_tool['management_tools']).name,
                                    'data':management_tool['id__count']})
        queryset_energy = companies.values('source_of_energy').annotate(Count('id')).order_by('source_of_energy') 
        total_energy = 0
        energy_source_data = []
        for energy_source in queryset_energy:
            if energy_source['source_of_energy'] != None:
                total_energy+= int(energy_source['id__count'])
                energy_source_data.append({'label':CompanyDropdownsMaster.objects.get(id=energy_source['source_of_energy']).name,
                                    'data':energy_source['id__count']})
        women_in_pson_level = []
        for company in companies:
            queryset_female_posn = FemalesInPosition.objects.filter(
                    company=company,year_fem=get_current_year()).values('company__name').annotate(
                        high_position=Sum('high_position'),med_position=Sum('med_position')
                    )
            in_med = 0
            in_high = 0
            total_fem_posn = 0
            for women_data in queryset_female_posn:
                in_high = int(women_data['high_position'])
                in_med = int(women_data['med_position'])
            total_fem_posn = int(in_high+in_med)

            women_in_pson_level.append({'company':company.name,'sector':company.main_category,'label':'Med Level Positions','data':in_med})
            women_in_pson_level.append({'company':company.name,'sector':company.main_category,'label':'Higher Level Positions','data':in_high})
        queryset_wh = companies.values('working_hours').annotate(Count('id')).order_by('working_hours').exclude(main_category='FBPIDI')
        working_hour_data = []
        total_wh = 0
        for working_hour in queryset_wh:
            total_wh += int(working_hour['id__count'])
            working_hour_data.append({'label':CompanyDropdownsMaster.objects.get(id=working_hour['working_hours']),
                                    'data':working_hour['id__count']})
        prodn_data = []
        for company in companies:
            pdata = ProductionCapacity.objects.filter(company=company,year=get_current_year()).values('product__sub_category_name','product__uom__name').annotate(total_prdn_capacity=Sum('install_prdn_capacity')*260,total_actual=Sum('actual_prdn_capacity')*260).order_by('product')
            for p in pdata:
                prodn_data.append({
                    'company':company,
                    'sector':company.main_category,
                    'product':p['product__sub_category_name'],
                    'uom':p['product__uom__name'],
                    'total_prdn_capacity':p['total_prdn_capacity'],
                    'total_actual':p['total_actual']
                })
        total_avi_data = []
        demand = 0
        supply = 0
        product = ""
        unit = ""
        for company in companies:
            inp_dem_sups = InputDemandSupply.objects.filter(company=company,year=get_current_year()).values('product__sub_category_name','input_unit__name').annotate(
                demand=Sum('demand'),supply = Sum('supply')
            )
            if inp_dem_sups.exists():
                for aup in inp_dem_sups:
                    demand += aup['demand']
                    supply += aup['supply']
                    product = aup['product__sub_category_name']
                    unit = aup['input_unit__name']
                if demand == 0:
                    av_inp=float(supply/1)
                else:
                    av_inp=float(supply/demand)
                
                total_avi_data.append({'company':company.name,
                                    'product':product,
                                    'unit':unit,
                                    'data':av_inp*100})
        local_share_data = []
        for company in companies:
            ann_inp_need = AnnualInputNeed.objects.filter(company=company,year=get_current_year()).values(
                                            'company__name','company__main_category','input_name',
                                            'product__sub_category_name','input_unit__name').annotate(
                                                local_share = Sum('local_input',output=models.FloatField())).order_by('product')
            for inp_share in ann_inp_need:
                local_share_data.append({'company':inp_share['company__name'],'product':inp_share['product__sub_category_name'],
                                'unit':inp_share['input_unit__name'],'input':inp_share['input_name'],'data':inp_share['local_share']})
        companies_with_data = companies.filter(Exists( ProductionAndSalesPerformance.objects.filter(company=OuterRef('pk'))),
                                                    Exists(ProductionCapacity.objects.filter(company=OuterRef('pk')))
                                                    )
        capital_util_data = []
        for company in companies_with_data:
            production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=get_current_year()).values('product','product__sub_category_name','company__name').annotate(all_data=Sum('production_amount'))
            production_capacity_this_year = ProductionCapacity.objects.filter(company=company,year=get_current_year())
            
            for (performance,capacity) in zip(production_performance_this_year,production_capacity_this_year):
                if performance['product'] == capacity.product.id:
                    capital_util_data.append({
                        'company':company.name,'sector':company.main_category,'product':performance['product__sub_category_name'],'production_amount':performance['all_data'],
                        'actual_production':capacity.actual_prdn_capacity
                    })
        change_capital_util_data = []
        for company in companies_with_data:
            production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=get_current_year()).values('product','product__sub_category_name','product__uom','company__name').annotate(all_data=Sum('production_amount'))
            production_performance_last_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=get_current_year()-1).values('product','product__sub_category_name','product__uom','company__name').annotate(all_data=Sum('production_amount'))
            production_capacity_this_year = ProductionCapacity.objects.filter(company=company,year=get_current_year())

            if production_performance_last_year.exists():
                for (performance_this,performance_last,capacity) in zip(production_performance_this_year,production_performance_last_year,production_capacity_this_year):
                    if performance_this['product'] == capacity.product.id or performance_last['product'] == capacity.product.id:
                        change_capital_util_data.append({
                            'company':company.name,
                            'sector':company.main_category,
                            'product':performance_this['product__sub_category_name'],
                            'unit':performance_this['product__uom'],
                            'pa_this':performance_this['all_data'],
                            'pa_last':performance_last['all_data'],
                            'apc':capacity.actual_prdn_capacity
                        })
            else:
                for (performance_this,capacity) in zip(production_performance_this_year,production_capacity_this_year):
                    if performance_this['product'] == capacity.product.id:
                        change_capital_util_data.append({
                            'company':company.name,
                            'sector':company.main_category,
                            'product':performance_this['product__sub_category_name'],
                            'unit':performance_this['product__uom'],
                            'pa_this':performance_this['all_data'],
                            'pa_last':0,
                            'apc':capacity.actual_prdn_capacity
                        })
        extraction_rate = []
        for company in companies:
            padata = ProductionCapacity.objects.filter(company=company,year=get_current_year()).values('product__sub_category_name','product__uom__name').annotate(avg_extraction_rate=Avg('extraction_rate')).order_by('product')
            for p in padata:
                extraction_rate.append(
                    {
                        'company':company.name,'sector':company.main_category,
                        'product':p['product__sub_category_name'],
                        'extraction_rate':p['avg_extraction_rate'],
                        'unit':p['product__uom__name']
                    }
                )
        average_price_data = []
        for product in products:
            pup = 0
            spp = ProductionAndSalesPerformance.objects.filter(product=product,activity_year=get_current_year()).values('product').annotate(
                total_sales_amnt=Sum('sales_amount'),total_sales=Sum('sales_value'))

            if spp.exists():
                for aup in spp:
                    price_total = aup['total_sales']
                    prodn_total = aup['total_sales_amnt']
            if prodn_total == 0:
                pup = float(price_total/1)
            else:
                pup = float(price_total/prodn_total)

            average_price_data.append({'product':product.sub_category_name,'data':pup})
        gvp_data = []
        for company in companies_with_data:
            perform_data = ProductionAndSalesPerformance.objects.filter(
                    company=company).values('company__name','product__sub_category_name').annotate(
                        total_this_year=Sum('sales_value',filter=Q(activity_year=get_current_year())),
                        total_last_year=Sum('sales_value',filter=Q(activity_year=get_current_year()-1)),
                        total_prev_year=Sum('sales_value',filter=Q(activity_year=get_current_year()-2))
                    )
            for gvp_index in perform_data:
                gvp_data.append({
                    'company':company.name,
                    'product':gvp_index['product__sub_category_name'],
                    'this_yr':gvp_index['total_this_year'],
                    'last_yr':gvp_index['total_last_year'],
                    'pref_yr':gvp_index['total_prev_year'],
                })
        emp_data_total = []
        total_perm_emp = 0
        total_temp_emp=0
        for company in companies:
            employees_perm = Employees.objects.filter(company=company,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(company=company,employment_type__icontains="Temporary")
            
            for ep in employees_perm:
                total_perm_emp = (ep.male+ep.female)
            
            for et in employees_temp:
                total_temp_emp = (et.male+et.female)
            
            total = total_perm_emp+total_temp_emp
            emp_data_total.append({'company':company.name,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        total_for_emp_m=0
        total_for_emp_f=0
        for_emp_data = []
        for company in companies:
            employees_foreign = Employees.objects.filter(company=company,employment_type__icontains="Foreign")
                        
            for ef in employees_foreign:
                total_for_emp_m += (ef.male)
                total_for_emp_f += (ef.female)

            total = total_for_emp_m+total_for_emp_f
            for_emp_data.append({'company':company.name,'data':total,'for_male':total_for_emp_m,'for_female':total_for_emp_f})
        job_created_data = []
        for company in companies:
            jobs_created_temp = JobOpportunities.objects.filter(company=company,job_type__icontains="Temporary",year_job=get_current_year())
            jobs_created_permanent = JobOpportunities.objects.filter(company=company,job_type__icontains="Permanent",year_job=get_current_year())
            
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
        context['for_emp_data'] = for_emp_data
        context['total_emp_data'] = emp_data_total
        context['gvp_data'] = gvp_data
        context['years'] = {'this_year':get_current_year(),'last_year':get_current_year()-1,'prev_year':get_current_year()-2}        
        context['price_data']=average_price_data
        context['extraction_rate'] = extraction_rate
        context['change_capital_util_data'] = change_capital_util_data
        context['capital_util_data'] = capital_util_data
        context['input_share']=local_share_data
        context['avalilable_input']=total_avi_data
        context['produn_data']=prodn_data
        context['total_wh'] = total_wh
        context['working_hour_data'] = working_hour_data
        context['total_fem_posn'] = total_fem_posn
        context['women_in_pson_level'] = women_in_pson_level
        context['destination_data'] = [{'label':"Exporting ",
                                        'data':companies.filter(market_destination__export__gt=0,market_destination__year_destn=get_current_year()).count()},
                                        {'label':"Local/Domestic",
                                        'data':companies.filter(market_destination__domestic__gt=0,market_destination__year_destn=get_current_year()).count()}
                                    ]
        context['target_data'] = [{'label':"Further Processing Factors",
                                        'data':companies.filter(market_target__further_proc_power__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                    {'label':"Final Consumers",
                                        'data':companies.filter(market_target__final_consumer__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                    {'label':"Restaurant & Hotels",
                                    'data':companies.filter(market_target__restaurant_and_hotels__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                    {'label':"Institutions",
                                    'data':companies.filter(market_target__institutions__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                    {'label':"EPSA",
                                    'data':companies.filter(market_target__epsa__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                    {'label':"Hospitals",
                                    'data':companies.filter(market_target__hospitals__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                    {'label':"Agents",
                                    'data':companies.filter(market_target__agents__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                    {'label':"Wholesaler/Distributor",
                                    'data':companies.filter(market_target__wholesaler_distributor__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                    {'label':"Retailor",
                                    'data':companies.filter(market_target__retailer__gt=0,market_target__year_target=get_current_year()).distinct('id').count()},
                                 
                                ]
        context['total_energy'] = total_energy
        context['energy_source_data'] = energy_source_data
        context['total_managment'] = total_managment
        context['management_tool_data'] = management_tool_data
        context['total_certification'] = total_certification
        context['certification_data'] = certification_data
        context['total_edu'] = total_edu
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

 