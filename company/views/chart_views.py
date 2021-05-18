import datetime
import random
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


def get_chart_color():
    random_number = random.randint(0,16777215)
    hex_number =format(random_number,'x')
    hex_number = '#'+hex_number
    return hex_number

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
    colors = []
    queryset = Company.objects.values('certification__name').annotate(Count('id')).order_by('certification').exclude(main_category='FBPIDI')
    for certification in queryset:
        if certification['certification__name'] != None:
            labels.append(str(certification['certification__name'])+"("+str(certification['id__count'])+")")
            data.append(certification['id__count'])
            colors.append(get_chart_color())
    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def company_subsector_chart(request):
    labels=[]
    data=[]
    colors = []
    queryset = Company.objects.values('category__category_name').annotate(Count('id')).order_by('category').exclude(main_category='FBPIDI')
    for category in queryset:
        if category['category__category_name'] != None:
            labels.append(category['category__category_name']+"("+str(category['id__count'])+")")
            data.append(category['id__count'])
        colors.append(get_chart_color())
    return JsonResponse({'labels':labels,'data':data,'colors':colors})


def management_tool_chart(request):
    labels=[]
    data=[]
    colors = []
    queryset = Company.objects.values('management_tools__name').annotate(Count('id')).order_by('management_tools').exclude(main_category='FBPIDI')
    for tools in queryset:
        if tools['management_tools__name'] != None:
            labels.append(tools['management_tools__name'])
            data.append(tools['id__count'])
            colors.append(get_chart_color())
    return JsonResponse({'labels':labels,'data':data,'colors':colors})  

def ownership_form_chart(self,*args,**kwargs):
    labels = []
    data = []
    colors = []
    queryset = Company.objects.values('ownership_form').annotate(Count('id')).order_by('ownership_form').exclude(main_category='FBPIDI')
    for ownership in queryset:
        if ownership['ownership_form'] != None:
            labels.append(str(CompanyDropdownsMaster.objects.get(id=ownership['ownership_form']).name)+" ("+str(ownership['id__count'])+")")
            data.append(ownership['id__count'])
            colors.append(get_chart_color())

    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def main_category_chart(request):
    labels = []
    data = []
    colors = []
    queryset = Company.objects.values('main_category').annotate(Count('id')).order_by('main_category').exclude(main_category='FBPIDI')
    for entry in queryset:
        labels.append(entry['main_category'])
        data.append(entry['id__count'])
        colors.append(get_chart_color())
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'colors':colors
    })

def working_hour_chart(request):
    labels = []
    data = []
    colors = []
    queryset = Company.objects.values('working_hours__name').annotate(Count('id')).order_by('working_hours').exclude(main_category='FBPIDI')
    for working_hour in queryset:
        if working_hour['working_hours__name'] != None:
            labels.append(working_hour['working_hours__name']+" hours")
            data.append(working_hour['id__count'])
            colors.append(get_chart_color())
    return JsonResponse({
        'labels':labels,'data':data,'colors':colors
    })
             
def inv_cap_chart(request):
    companies = Company.objects.all().exclude(main_category="FBPIDI")
    labels = []
    data = []
    colors = []
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
                colors.append(get_chart_color())
    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def production_capacity_chart(request):
    labels = []
    data = []    
    colors = []
    queryset = ProductionCapacity.objects.values('product__sub_category_name','product__uom').annotate(
        total_prdn_capacity=Sum('install_prdn_capacity')*260).order_by('product')     
    for pdata in queryset:
        labels.append(pdata['product__sub_category_name'])
        data.append(pdata['total_prdn_capacity'])
        colors.append(get_chart_color())
    return JsonResponse({
        'labels':labels,'data':data,'colors':colors
    })
def capital_util_chart(request):
    labels = []
    data=[]
    colors = []
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
                colors.append(get_chart_color())
    return JsonResponse({
        'labels':labels,'data':data,'colors':colors
    })
def change_capital_util_chart(request):
    labels = []
    data = []
    colors = []
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
                    colors.append(get_chart_color())
        else:
            for (performance_this,capacity) in zip(production_performance_this_year,production_capacity_this_year):
                if performance_this['product'] == capacity.product.id:
                    labels.append(str(company.name)+"-"+performance_this['product__sub_category_name'])
                    data.append(change_capital_util(performance_this['all_data'],0,capacity.actual_prdn_capacity))
                    colors.append(get_chart_color())
    return JsonResponse({
        'labels':labels,'data':data,'colors':colors
    })

def extraction_rate_chart(request):
    labels = []
    data = []
    colors = []
    queryset = ProductionCapacity.objects.values('product__sub_category_name','product__uom').annotate(avg_extraction_rate=Avg('extraction_rate')).order_by('product')
    for pdata in queryset:
        labels.append(pdata['product__sub_category_name'])
        data.append(pdata['avg_extraction_rate'])
        colors.append(get_chart_color())
    return JsonResponse({'labels':labels,'data':data,'colors':colors})


def gvp_chart(request):
    labels = []
    colors = []
    colors1 = []
    colors2 = []
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
            colors.append(get_chart_color())
            colors1.append(get_chart_color())
            colors2.append(get_chart_color())
    return JsonResponse({'labels':labels,'this_year':gvp_this_year,
                        'last_year':gvp_last_year,'prev_year':gvp_prev_year,'year':get_current_year(),
                        'colors':colors,'colors1':colors1,'colors2':colors2})
def num_emp_chart(request):
    labels = []
    data = []
    colors = []
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
        colors.append(get_chart_color())
        if company.main_category == "Food":
            food_total += total
        if company.main_category == "Beverage":
            bev_total += total
        if company.main_category == "Pharmaceuticals":
            pharm_total += total
    labels = ['Food Sector','Beverage Sector','Phrmaceutical Sector']
    data = [0,food_total,bev_total,pharm_total]
    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def num_fem_emp_chart(request):
    labels = []
    data = []
    colors = []
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
        colors.append(get_chart_color())
    labels = ['Food Sector','Beverage Sector','Phrmaceutical Sector']
    data = [food_total,bev_total,pharm_total]
    return JsonResponse({'labels':labels,'data':data,'colors':colors})


def num_for_emp_chart(request):
    labels = []
    data = []
    colors = []
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
        colors.append(get_chart_color())
    labels = ['Food Sector','Beverage Sector','Phrmaceutical Sector']
    data = [food_total,bev_total,pharm_total]
    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def num_jobs_chart(request):
    labels = []
    data = []
    total = 0
    colors = []
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
        colors.append(get_chart_color())
    labels = ['Food Sector','Beverage Sector','Phrmaceutical Sector']
    data = [food_total,bev_total,pharm_total]
    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def num_edu_level_chart(request):
    labels = []
    colors = []
    data_male = []
    data_female = []
    queryset = EducationalStatus.objects.filter(year_edu=get_current_year()).values('education_type').annotate(Sum('male'),Sum('female')).order_by('education_type')
    total = 0
    for edu_data in queryset:
        labels.append(edu_data['education_type'])
        data_female.append(edu_data['female__sum'])
        data_male.append(edu_data['male__sum'])
        colors.append(get_chart_color())
    return JsonResponse({'labels':labels,'data_male':data_male,'data_female':data_female,'colors':colors})

def num_fem_inpsn_chart(request):
    queryset = FemalesInPosition.objects.filter(year_fem=get_current_year())
    in_med = 0
    in_high = 0
    colors = []
    women_in_pson_level = []
    for women_data in queryset:
        in_high += int(women_data.high_position)
        in_med += int(women_data.med_position)
        colors.append(get_chart_color())
    return JsonResponse({
        'labels':['Med Level Positions','Higher Level Positions'],
        'data':[in_med,in_high],'colors':colors
    })

def input_avl_chart(request):
    labels  =[]
    data = []
    supply = 0
    demand = 0
    av_inp = 0
    colors = []
    for product in SubCategory.objects.all():
        inp_dem_sups = InputDemandSupply.objects.filter(product=product,year=get_current_year()).values('product').annotate(
            demand=Sum('demand'),supply = Sum('supply')
        ).order_by('product')
        if inp_dem_sups.exists():
            for aup in inp_dem_sups:
                demand += aup['demand']
                supply += aup['supply']
                
            if demand == 0:
                av_inp=float(supply/1)
            else:
                av_inp=float(supply/demand)
        labels.append(product.sub_category_name)
        data.append(round(av_inp,2))
        colors.append(get_chart_color())
    
    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def input_share_chart(request):
    labels  =[]
    data = []
    colors = []
    local_share = 0
    for product in SubCategory.objects.all():
        ann_inp_need = AnnualInputNeed.objects.filter(product=product)
        if ann_inp_need.exists():
            for aup in ann_inp_need:
                local_share += aup.local_input
        labels.append(product.sub_category_name)
        data.append(local_share)
        colors.append(get_chart_color())
    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def energy_source_chart(request):
    labels  =[]
    data = []
    colors = []
    queryset = Company.objects.values('source_of_energy__name').annotate(Count('id')).order_by('source_of_energy').exclude(main_category='FBPIDI')
    for energy_source in queryset:
        if energy_source['source_of_energy__name'] != None:
            labels.append(energy_source['source_of_energy__name'])
            data.append(energy_source['id__count'])
            colors.append(get_chart_color())
    return JsonResponse({'labels':labels,'data':data,'colors':colors})

def market_target_chart(request):
    company = Company.objects.all().exclude(main_category='FBPIDI').order_by('id')
    return JsonResponse({
        'labels':["Further Processing Factors","Final Consumers","Restaurant & Hotels","Institutions","EPSA",
                  "Hospitals","Agents","Wholesaler/Distributor","Retailor",],
        'data':[company.filter(market_target__further_proc_power__gt=0).distinct('id').count(),
                company.filter(market_target__final_consumer__gt=0).distinct('id').count(),
                company.filter(market_target__restaurant_and_hotels__gt=0).distinct('id').count(),
                company.filter(market_target__institutions__gt=0).distinct('id').count(),
                company.filter(market_target__epsa__gt=0).distinct('id').count(),
                company.filter(market_target__hospitals__gt=0).distinct('id').count(),
                company.filter(market_target__agents__gt=0).distinct('id').count(),
                company.filter(market_target__wholesaler_distributor__gt=0).distinct('id').count(),
                company.filter(market_target__retailer__gt=0).distinct('id').count()
                ],
        'colors':[get_chart_color(),get_chart_color(),get_chart_color(),get_chart_color(),get_chart_color(),get_chart_color(),
                get_chart_color(),get_chart_color(),get_chart_color()]
    })

def market_destin_chart(request):
    company = Company.objects.all().exclude(main_category='FBPIDI')
    return JsonResponse({
        'labels':["Exporting ","Local/Domestic",],
        'data':[company.filter(market_destination__export__gt=0,market_destination__year_destn=get_current_year()).count(),
                company.filter(market_destination__domestic__gt=0,market_destination__year_destn=get_current_year()).count()],
        'colors':[get_chart_color(),get_chart_color()]
    })


def inquiry_product_chart(request):
    labels  =[]
    data = []
    colors = []
    try:
        company = request.user.get_company()
        categories = [c.id for c  in company.category.all()]
        
        q = Q( Q( product__company = request.user.get_company().id) | 
                Q( category__in = categories))
        queryset =  ProductInquiry.objects.filter(q).values('product__name').annotate(
            inqury=Count('id')
        ).order_by('product')
        for inq in queryset:
            labels.append(inq['product__name'])
            data.append(inq['inqury'])
            colors.append(get_chart_color())
        return JsonResponse({'labels':labels,'data':data,'colors':colors})
    except Exception as e:
        return JsonResponse({'data':[],'labels':[],'colors':[]})


def daily_inquiry_chart(request):
    today = datetime.datetime.today()
    yesterday = today-datetime.timedelta(days=1)
    thirdday = today-datetime.timedelta(days=2)
    frothday = today-datetime.timedelta(days=3)
    fifthday = today-datetime.timedelta(days=4)
    sixthday = today-datetime.timedelta(days=5)
    sevenday = today-datetime.timedelta(days=6)
    labels  =[]
    data = []
    colors = []
    try:
        company = request.user.get_company()
        categories = [c.id for c  in company.category.all()]
        
        q = Q( Q( product__company = request.user.get_company().id) | 
                Q( category__in = categories))

        today_data =  ProductInquiry.objects.filter(q,Q(created_date__date=today))
        lastday_data =  ProductInquiry.objects.filter(q, Q(created_date__date=yesterday))
        thirdday_data =  ProductInquiry.objects.filter(q,Q(created_date__date=thirdday) )
        forthday_data =  ProductInquiry.objects.filter(q,Q(created_date__date=frothday) )
        fifthday_data =  ProductInquiry.objects.filter(q, Q(created_date__date=fifthday))
        sixday_data =  ProductInquiry.objects.filter(q, Q(created_date__date=sixthday))
        sevenday_data = ProductInquiry.objects.filter(q, Q(created_date__date=sevenday))

        labels=[
            sevenday.strftime("%A"),sixthday.strftime("%A"),fifthday.strftime("%A"),frothday.strftime("%A"),
            thirdday.strftime("%A"),yesterday.strftime("%A"),today.strftime("%A")
        ]
        data = [
            sevenday_data.count(),sixday_data.count(),fifthday_data.count(),forthday_data.count(),
            thirdday_data.count(),lastday_data.count(),today_data.count()
        ]
        for i in range(0,8):
            colors.append(get_chart_color())
        return JsonResponse({'labels':labels,'data':data,'colors':colors})
    except Exception as e:
        return JsonResponse({'data':[],'labels':[],'colors':colors})


