import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum,Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Sum,Count,OuterRef,Exists,Q,F,Avg


from admin_site.models import CompanyDropdownsMaster
from admin_site.decorators import company_created,company_is_active
from admin_site.templatetags.admin_template_tags import get_capital_util,change_capital_util

from company.models import *
from product.models import *
decorators = [never_cache, company_created(),company_is_active()]


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

# @method_decorator(decorators,name='dispatch')
def certification_chart(request):
    labels=[]
    data=[]
    queryset = Company.objects.values('certification__name').annotate(Count('id')).order_by('certification').exclude(main_category='FBPIDI')
    for certification in queryset:
        labels.append(certification['certification__name'])
        data.append(certification['id__count'])
    return JsonResponse({'labels':labels,'data':data})

def company_subsector_chart(request):
    labels=[]
    data=[]
    queryset = Company.objects.values('category__category_name').annotate(Count('id')).order_by('category').exclude(main_category='FBPIDI')
    for category in queryset:
        labels.append(category['category__category_name']+"("+str(category['id__count'])+")")
        data.append(category['id__count'])
    return JsonResponse({'labels':labels,'data':data})


def management_tool_chart(request):
    labels=[]
    data=[]
    queryset = Company.objects.values('management_tools__name').annotate(Count('id')).order_by('management_tools').exclude(main_category='FBPIDI')
    for tools in queryset:
        labels.append(tools['management_tools__name'])
        data.append(tools['id__count'])
    return JsonResponse({'labels':labels,'data':data})  

def ownership_form_chart(self,*args,**kwargs):
    labels = []
    data = []
    queryset = Company.objects.values('ownership_form').annotate(Count('id')).order_by('ownership_form').exclude(main_category='FBPIDI')
    for ownership in queryset:
        labels.append(CompanyDropdownsMaster.objects.get(id=ownership['ownership_form']).name)
        data.append(ownership['id__count'])
    return JsonResponse({'labels':labels,'data':data})

def main_category_chart(request):
    labels = []
    data = []
    
    queryset = Company.objects.values('main_category').annotate(Count('id')).order_by('main_category').exclude(main_category='FBPIDI')
    for entry in queryset:
        labels.append(entry['main_category'])
        data.append(entry['id__count'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def working_hour_chart(request):
    labels = []
    data = []
    queryset = Company.objects.values('working_hours__name').annotate(Count('id')).order_by('working_hours').exclude(main_category='FBPIDI')
    for working_hour in queryset:
        labels.append(working_hour['working_hours__name']+" hours")
        data.append(working_hour['id__count'])
    return JsonResponse({
        'labels':labels,'data':data
    })
             
def inv_cap_chart(request):
    companies = Company.objects.all().exclude(main_category="FBPIDI")
    labels = []
    data = []
    for company in companies:
        if InvestmentCapital.objects.filter(company=company).exists():
            queryset =  InvestmentCapital.objects.filter(company=company).values('company__name').annotate(
                machinery = Sum('machinery_cost'),
                building = Sum('building_cost'),
                working = Sum('working_capital')
            )
            for invcap in queryset:
                labels.append(invcap['company__name'])
                data.append(invcap['machinery']+invcap['working']+invcap['building'])
    return JsonResponse({'labels':labels,'data':data})

def production_capacity_chart(request):
    labels = []
    data = []    
    queryset = ProductionCapacity.objects.values('product__sub_category_name','product__uom').annotate(
        total_prdn_capacity=Sum('install_prdn_capacity')*260).order_by('product')     
    for pdata in queryset:
        labels.append(pdata['product__sub_category_name'])
        data.append(pdata['total_prdn_capacity'])
    return JsonResponse({
        'labels':labels,'data':data
    })
def capital_util_chart(request):
    labels = []
    data=[]
    companies_with_data = Company.objects.filter(Exists( ProductionAndSalesPerformance.objects.filter(company=OuterRef('pk'))),
                                                    Exists(ProductionCapacity.objects.filter(company=OuterRef('pk')))
                                                    ).exclude(main_category="FBPIDI")
    for company in companies_with_data:
        production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=get_current_year()).values('product','product__sub_category_name','company__name').annotate(all_data=Sum('production_amount'))
        production_capacity_this_year = ProductionCapacity.objects.filter(company=company,year=get_current_year())
        
        for (performance,capacity) in zip(production_performance_this_year,production_capacity_this_year):
            if performance['product'] == capacity.product.id:
                labels.append(performance['product__sub_category_name'])
                data.append(get_capital_util(performance['all_data'],capacity.actual_prdn_capacity))
    return JsonResponse({
        'labels':labels,'data':data
    })
def change_capital_util_chart(request):
    labels = []
    data = []
    companies_with_data = Company.objects.filter(Exists( ProductionAndSalesPerformance.objects.filter(company=OuterRef('pk'))),
                                                    Exists(ProductionCapacity.objects.filter(company=OuterRef('pk')))
                                                    ).exclude(main_category="FBPIDI")
    for company in companies_with_data:
        production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=get_current_year()).values('product','product__sub_category_name','product__uom','company__name').annotate(all_data=Sum('production_amount'))
        production_performance_last_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=get_current_year()-1).values('product','product__sub_category_name','product__uom','company__name').annotate(all_data=Sum('production_amount'))
        production_capacity_this_year = ProductionCapacity.objects.filter(company=company,year=get_current_year())

        if production_performance_last_year.exists():
            for (performance_this,performance_last,capacity) in zip(production_performance_this_year,production_performance_last_year,production_capacity_this_year):
                if performance_this['product'] == capacity.product.id or performance_last['product'] == capacity.product.id:
                    labels.append(company.name+"-"+performance_this['product__sub_category_name'])
                    data.append(change_capital_util(performance_this['all_data'],performance_last['all_data'],capacity.actual_prdn_capacity))
        else:
            for (performance_this,capacity) in zip(production_performance_this_year,production_capacity_this_year):
                if performance_this['product'] == capacity.product.id:
                    labels.append(company.name+"-"+performance_this['product__sub_category_name'])
                    data.append(change_capital_util(performance_this['all_data'],0,capacity.actual_prdn_capacity))
    return JsonResponse({
        'labels':labels,'data':data
    })

def extraction_rate_chart(request):
    labels = []
    data = []
    queryset = ProductionCapacity.objects.values('product__sub_category_name','product__uom').annotate(avg_extraction_rate=Avg('extraction_rate')).order_by('product')
    for pdata in queryset:
        labels.append(pdata['product__sub_category_name'])
        data.append(pdata['avg_extraction_rate'])
    return JsonResponse({'labels':labels,'data':data})


def gvp_chart(request):
    labels = []
    gvp_this_year = []
    gvp_last_year = []
    gvp_prev_year = []
    companies_with_data = Company.objects.filter(Exists( ProductionAndSalesPerformance.objects.filter(company=OuterRef('pk')))).exclude(main_category='FBPIDI')
    for company in companies_with_data:
        perform_data = ProductionAndSalesPerformance.objects.filter(
                company=company).values('company__name','product__sub_category_name').annotate(
                    total_this_year=Sum('sales_value',filter=Q(activity_year=get_current_year())),
                    total_last_year=Sum('sales_value',filter=Q(activity_year=get_current_year()-1)),
                    total_prev_year=Sum('sales_value',filter=Q(activity_year=get_current_year()-2))
                )
        for gvp_index in perform_data:
            this_year = 0
            last_year = 0
            prev_year = 0
            if gvp_index['total_this_year'] != None:
                this_year = gvp_index['total_this_year']
            if gvp_index['total_last_year'] != None:
                last_year = gvp_index['total_last_year']
            if gvp_index['total_prev_year'] != None:
                prev_year = gvp_index['total_prev_year']

            labels.append(company.name+"-"+gvp_index['product__sub_category_name'])
            gvp_this_year.append(this_year)
            gvp_last_year.append(last_year)
            gvp_prev_year.append(prev_year)
    return JsonResponse({'labels':labels,'this_year':gvp_this_year,'last_year':gvp_last_year,'prev_year':gvp_prev_year,'year':get_current_year()})
def num_emp_chart(request):
    labels = []
    data = []
    total_perm_emp = 0
    total_temp_emp = 0
    total = 0
    food_total = 0
    bev_total = 0
    pharm_total = 0
    for company in Company.objects.all().exclude(main_category='FBPIDI'):
        employees_perm = Employees.objects.filter(company=company,employment_type__icontains="Permanent")
        employees_temp = Employees.objects.filter(company=company,employment_type__icontains="Temporary")
        
        for ep in employees_perm:
            total_perm_emp = (ep.male+ep.female)
        
        for et in employees_temp:
            total_temp_emp = (et.male+et.female)
        total = total_perm_emp+total_temp_emp

        if company.main_category == "Food":
            food_total += total
        if company.main_category == "Beverage":
            bev_total += total
        if company.main_category == "Pharmaceuticals":
            pharm_total += total
    labels = ['Food Sector','Beverage Sector','Phrmaceutical Sector']
    data = [food_total,bev_total,pharm_total]
    return JsonResponse({'labels':labels,'data':data})

def num_fem_emp_chart(request):
    labels = []
    data = []
    total_perm_emp = 0
    total_temp_emp = 0
    total = 0
    food_total = 0
    bev_total = 0
    pharm_total = 0
    for company in Company.objects.all().exclude(main_category='FBPIDI'):
        employees_perm = Employees.objects.filter(company=company,employment_type__icontains="Permanent")
        employees_temp = Employees.objects.filter(company=company,employment_type__icontains="Temporary")
        
        for ep in employees_perm:
            total_perm_emp = (ep.female)
        
        for et in employees_temp:
            total_temp_emp = (et.female)
        
        total = total_perm_emp+total_temp_emp
        if company.main_category == "Food":
            food_total += total
        if company.main_category == "Beverage":
            bev_total += total
        if company.main_category == "Pharmaceuticals":
            pharm_total += total
    labels = ['Food Sector','Beverage Sector','Phrmaceutical Sector']
    data = [food_total,bev_total,pharm_total]
    return JsonResponse({'labels':labels,'data':data})


def num_for_emp_chart(request):
    labels = []
    data = []
    total_for_emp_m = 0
    total_for_emp_f = 0
    total = 0
    food_total = 0
    bev_total = 0
    pharm_total = 0
    for company in Company.objects.all().exclude(main_category='FBPIDI'):
        employees_foreign = Employees.objects.filter(company=company,employment_type__icontains="Foreign")         
        for ef in employees_foreign:
            total_for_emp_m += (ef.male)
            total_for_emp_f += (ef.female)

        total = total_for_emp_m+total_for_emp_f
        if company.main_category == "Food":
            food_total += total
        if company.main_category == "Beverage":
            bev_total += total
        if company.main_category == "Pharmaceuticals":
            pharm_total += total
    labels = ['Food Sector','Beverage Sector','Phrmaceutical Sector']
    data = [food_total,bev_total,pharm_total]
    return JsonResponse({'labels':labels,'data':data})

def num_jobs_chart(request):
    labels = []
    data = []
    total = 0
    food_total = 0
    bev_total = 0
    pharm_total = 0
    for company in Company.objects.all().exclude(main_category='FBPIDI'):
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
        total = permanent_female+permanent_male+temp_female+temp_male
        if company.main_category == "Food":
            food_total += total
        if company.main_category == "Beverage":
            bev_total += total
        if company.main_category == "Pharmaceuticals":
            pharm_total += total
    labels = ['Food Sector','Beverage Sector','Phrmaceutical Sector']
    data = [food_total,bev_total,pharm_total]
    return JsonResponse({'labels':labels,'data':data})