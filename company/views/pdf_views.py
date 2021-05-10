
import datetime
from django.http import HttpResponse
from django.views.generic import View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.template.loader import get_template
from django.db.models import *
from admin_site.decorators import company_created,company_is_active

from company.render import render_to_pdf 
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

@method_decorator(decorators,name='get')
class GenerateAllCompanyPdf(View):
    def get(self, request, *args, **kwargs):
        context = {}
        total_inv_cap_data = []
        ownership_data = []
        education_status_data = []
        current_year= get_current_year()
        if self.kwargs['year'] != 'all':
            current_year = self.kwargs['year']

        companies = Company.objects.all().exclude(main_category='FBPIDI').order_by('id')
        products = SubCategory.objects.all()
        if self.kwargs['region'] != "all":
            companies = companies.filter(company_address__region=self.kwargs['region'])
            context['region'] = RegionMaster.objects.get(id=self.kwargs['region']).name
        if self.kwargs['sector'] != "all":
            companies = companies.filter(main_category=self.kwargs['sector'])
            products = products.filter(category_name__category_type=self.kwargs['sector'])
            context['sector'] = self.kwargs['sector']
        if self.kwargs['sub_sector'] != "all":
            companies = companies.filter(category=self.kwargs['sub_sector'])
            products = products.filter(category_name=self.kwargs['sub_sector'])
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sub_sector']).category_name
        if self.kwargs['product'] != "all":
            companies = companies.filter(company_brand__product_type=self.kwargs['product'])
            products = products.filter(id=self.kwargs['product'])
            context['product'] = SubCategory.objects.get(id=self.kwargs['product']).sub_category_name
        
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
        queryset = companies.values('ownership_form__name').annotate(Count('id')).order_by('ownership_form') 
        total_ownership = 0
        for ownership in queryset:
            if ownership['ownership_form__name'] != None:
                total_ownership += int(ownership['id__count'])
                ownership_data.append({'label':ownership['ownership_form__name'],
                                    'data':ownership['id__count']})

        # Educational status data
        total_edu = 0
        for company in companies:
            queryset_edu = EducationalStatus.objects.filter(
                company=company,year_edu=current_year).values('education_type').annotate(
                     Sum('male'),Sum('female'),total_edu=Sum('male')+Sum('female') ).order_by('education_type')
            
            fem_edu = 0
            male_edu = 0
            for edu_data in queryset_edu:
                fem_edu += edu_data['female__sum']
                male_edu += edu_data['male__sum']
                # total_edu += int(+)
                education_status_data.append({'company':company.name,'sector':company.main_category,'label':edu_data['education_type'],
                                        'data':int(edu_data['female__sum']+edu_data['male__sum'])})
            total_edu = fem_edu+male_edu
        queryset_cert = companies.values('certification__name').annotate(Count('id')).order_by('certification') 
        certification_data = []
        total_certification = 0
        if queryset_cert:
            for certification in queryset_cert:
                if certification['certification__name'] != None:
                    total_certification+= int(certification['id__count'])
                    certification_data.append({'label':certification['certification__name'],
                                        'data':certification['id__count']})
        
        queryset_mgmt = companies.values('management_tools__name').annotate(Count('id')).order_by('management_tools') 
        management_tool_data = []
        total_managment = 0
        if queryset_mgmt:
            for management_tool in queryset_mgmt:
                if management_tool['management_tools__name'] != None:
                    total_managment+= int(management_tool['id__count'])
                    management_tool_data.append({'label':management_tool['management_tools__name'],
                                        'data':management_tool['id__count']})
        queryset_energy = companies.values('source_of_energy__name').annotate(Count('id')).order_by('source_of_energy') 
        total_energy = 0
        energy_source_data = []
        if queryset_energy:
            for energy_source in queryset_energy:
                if energy_source['source_of_energy__name'] != None:
                    total_energy+= int(energy_source['id__count'])
                    energy_source_data.append({'label':energy_source['source_of_energy__name'],
                                        'data':energy_source['id__count']})
        women_in_pson_level = []
        total_fem_posn = 0
        if companies:
            for company in companies:
                queryset_female_posn = FemalesInPosition.objects.filter(
                        company=company,year_fem=current_year).values('company__name').annotate(
                            high_position=Sum('high_position'),med_position=Sum('med_position')
                        )
                in_med = 0
                in_high = 0
                
                for women_data in queryset_female_posn:
                    in_high = int(women_data['high_position'])
                    in_med = int(women_data['med_position'])
                total_fem_posn = int(in_high+in_med)

                women_in_pson_level.append({'company':company.name,'sector':company.main_category,'label':'Med Level Positions','data':in_med})
                women_in_pson_level.append({'company':company.name,'sector':company.main_category,'label':'Higher Level Positions','data':in_high})
        queryset_wh = companies.values('working_hours__name').annotate(Count('id')).order_by('working_hours').exclude(main_category='FBPIDI')
        working_hour_data = []
        total_wh = 0
        if queryset_wh:
            for working_hour in queryset_wh:
                if working_hour['working_hours__name'] != None:
                    total_wh += int(working_hour['id__count'])
                    working_hour_data.append({'label':working_hour['working_hours__name'],
                                            'data':working_hour['id__count']})
        prodn_data = []
        if companies:
            for company in companies:
                pdata = ProductionCapacity.objects.filter(company=company,year=current_year).values('product__sub_category_name','product__uom__name').annotate(total_prdn_capacity=Sum('install_prdn_capacity')*260,total_actual=Sum('actual_prdn_capacity')*260).order_by('product')
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
        if companies:
            for company in companies:
                inp_dem_sups = InputDemandSupply.objects.filter(company=company,year=current_year).values('product__sub_category_name','input_unit__name').annotate(
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
        if companies:
            for company in companies:
                ann_inp_need = AnnualInputNeed.objects.filter(company=company,year=current_year).values(
                                                'company__name','company__main_category','input_name',
                                                'product__sub_category_name','input_unit__name').annotate(
                                                    local_share = Sum('local_input',output=models.FloatField())).order_by('product')
                if ann_inp_need:
                    for inp_share in ann_inp_need:
                        local_share_data.append({'company':inp_share['company__name'],'product':inp_share['product__sub_category_name'],
                                        'unit':inp_share['input_unit__name'],'input':inp_share['input_name'],'data':inp_share['local_share']})
        companies_with_data = companies.filter(Exists( ProductionAndSalesPerformance.objects.filter(company=OuterRef('pk'))),
                                                        Exists(ProductionCapacity.objects.filter(company=OuterRef('pk')))
                                                        )
        capital_util_data = []
        if companies_with_data:
            for company in companies_with_data:
                production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=current_year).values('product','product__sub_category_name','company__name').annotate(all_data=Sum('production_amount'))
                production_capacity_this_year = ProductionCapacity.objects.filter(company=company,year=current_year)
                
                for (performance,capacity) in zip(production_performance_this_year,production_capacity_this_year):
                    if performance['product'] == capacity.product.id:
                        capital_util_data.append({
                            'company':company.name,'sector':company.main_category,'product':performance['product__sub_category_name'],'production_amount':performance['all_data'],
                            'actual_production':capacity.actual_prdn_capacity
                        })
        change_capital_util_data = []
        if companies_with_data:
            for company in companies_with_data:
                production_performance_this_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=current_year).values('product','product__sub_category_name','product__uom','company__name').annotate(all_data=Sum('production_amount'))
                production_performance_last_year = ProductionAndSalesPerformance.objects.filter(company=company,activity_year=int(current_year)-1).values('product','product__sub_category_name','product__uom','company__name').annotate(all_data=Sum('production_amount'))
                production_capacity_this_year = ProductionCapacity.objects.filter(company=company,year=current_year)

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
        if companies:
            for company in companies:
                padata = ProductionCapacity.objects.filter(company=company,year=current_year).values('product__sub_category_name','product__uom__name').annotate(avg_extraction_rate=Avg('extraction_rate')).order_by('product')
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
        prodn_total = 0
        price_total = 0

        if products:
            for product in products:
                pup = 0
                spp = ProductionAndSalesPerformance.objects.filter(product=product,activity_year=current_year).values('product').annotate(
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

        if companies_with_data:
            for company in companies_with_data:
                perform_data = ProductionAndSalesPerformance.objects.filter(
                        company=company).values('company__name','product__sub_category_name').annotate(
                            total_this_year=Sum('sales_value',filter=Q(activity_year=current_year)),
                            total_last_year=Sum('sales_value',filter=Q(activity_year=int(current_year)-1)),
                            total_prev_year=Sum('sales_value',filter=Q(activity_year=int(current_year)-2))
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
            jobs_created_temp = JobOpportunities.objects.filter(company=company,job_type__icontains="Temporary",year_job=current_year)
            jobs_created_permanent = JobOpportunities.objects.filter(company=company,job_type__icontains="Permanent",year_job=current_year)
            
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
        context['filter_data'] = [
                                { 
                                    'data':companies.exclude(Q(conducted_research='')|Q(conducted_research=None)), 
                                    'label':"Number of Industries Who Conducted Research"
                                },
                                {
                                    'data':companies.exclude(Q(outsourced_test_param='')|Q(outsourced_test_param=None)),
                                    'label':"Number of Industries Who OutSourced Test Parameter"
                                },
                                {
                                    'data':companies.exclude(Q(new_product_developed='')|Q(new_product_developed=None)),
                                    'label':"Number of Industries Who Developed New Product"
                                },
                                {
                                    'data':companies.exclude(Q(expansion_plan='')|Q(expansion_plan=None)),
                                    'label':"Number of Industries Who has Expansion Plan"
                                },
                                {
                                    'data':companies.exclude(Q(waste_trtmnt_system='')|Q(waste_trtmnt_system=None)),
                                    'label':"Number of Industries Who have Waste Treatment & disposal System"
                                },
                                {
                                    'data':companies.exclude(e_commerce=True),
                                    'label':"Number of Industries Who Use Ecomerce"
                                },
                                {
                                    'data':companies.exclude(active_database=True),
                                    'label':"Number of Industries Who has Active Database"
                                },
                                {
                                    'data':companies.exclude(efluent_treatment_plant=True),
                                    'label':"Number of Industries Who has Efluent Treatment Plant"
                                },
                                {
                                    'data':companies.exclude(env_mgmt_plan=True),
                                    'label':"Number of Industries Who has Environmental Management Plan"
                                },
                                {
                                    'data':companies.exclude(env_focal_person=True),
                                    'label':"Number of Industries Who has Environmental Focal person"
                                },
                                {
                                    'data':companies.exclude(safety_profesional=True),
                                    'label':"Number of Industries Who has Saftey Professional"
                                },
                                {
                                    'data':companies.exclude(Q(gas_carb_emision='')|Q(gas_carb_emision=None)),
                                    'label':"Number of Industries Who Measure Their Gas Carbon Emission"
                                },
                                {
                                    'data':companies.exclude(Q(comunity_compliant='')|Q(comunity_compliant=None)),
                                    'label':"Number of Industries Who  have Compliant with local Community"
                                },
                                {
                                    'data':companies.exclude(Q(lab_test_analysis=None)|Q(lab_equipment=None)),
                                    'label':"Number of Industries Who have Quality Control Laboratory"
                                } ,{
                                    'data':companies.exclude(Q(trade_license='')|Q(trade_license=None)),
                                    'label':"Number of Industries Who valid Trade license"
                                },{
                                    'data':companies.filter(Exists(Certificates.objects.filter(company=OuterRef('pk')))),
                                    'label':"Number of Industries Having Valid Certificate of Competency"
                                } 
                ]
        context['established_year_data'] = [
                    {'data':companies.filter(established_yr__lte='2000').count(),'label':"Before 2000 E.C"},
                    {'data':companies.filter(established_yr__lte='2005',established_yr__gte='2001').count(),'label':"2001 - 2005 E.C"},
                    {'data':companies.filter(established_yr__lte='2010',established_yr__gte='2006').count(),'label':"2006- 2010 E.C"},
                    {'data':companies.filter(established_yr__gte='2011').count(),'label':"After 2011 E.C"},
                ]
        context['total_count'] = companies.count()
        context['company_list'] = companies
        context['job_created_data'] = job_created_data 
        context['for_emp_data'] = for_emp_data
        context['total_emp_data'] = emp_data_total
        context['gvp_data'] = gvp_data
        context['years'] = {'this_year':int(current_year),'last_year':int(current_year)-1,'prev_year':int(current_year)-2}        
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
                                        'data':companies.filter(market_destination__export__gt=0,market_destination__year_destn=current_year).count()},
                                        {'label':"Local/Domestic",
                                        'data':companies.filter(market_destination__domestic__gt=0,market_destination__year_destn=current_year).count()}
                                    ]
        context['target_data'] = [{'label':"Further Processing Factors",
                                        'data':companies.filter(market_target__further_proc_power__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                    {'label':"Final Consumers",
                                        'data':companies.filter(market_target__final_consumer__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                    {'label':"Restaurant & Hotels",
                                    'data':companies.filter(market_target__restaurant_and_hotels__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                    {'label':"Institutions",
                                    'data':companies.filter(market_target__institutions__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                    {'label':"EPSA",
                                    'data':companies.filter(market_target__epsa__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                    {'label':"Hospitals",
                                    'data':companies.filter(market_target__hospitals__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                    {'label':"Agents",
                                    'data':companies.filter(market_target__agents__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                    {'label':"Wholesaler/Distributor",
                                    'data':companies.filter(market_target__wholesaler_distributor__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                    {'label':"Retailor",
                                    'data':companies.filter(market_target__retailer__gt=0,market_target__year_target=current_year).distinct('id').count()},
                                 
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
        context['current_year'] = current_year
        pdf = render_to_pdf('admin/report/all_report_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %("IIMS-Companies-Report")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
          


@method_decorator(decorators,name='dispatch')
class GenerateCompanyToPDF(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        context = {}
        company = Company.objects.get(id=self.kwargs['pk'])
        inv_cap =  InvestmentCapital.objects.filter(company=company).annotate(
                        machinery = Sum('machinery_cost'),
                        building = Sum('building_cost'),
                        working = Sum('working_capital')
                    )
        today = datetime.datetime.today()
        this_year = today.year
        ethio_year = (this_year-8)
        production_capacity = ProductionCapacity.objects.filter(company=company,year=get_current_year())
        input_need = AnnualInputNeed.objects.filter(company=company,year=get_current_year())
        
        sales_performance = ProductionAndSalesPerformance.objects.filter(company=company).values('product__uom__name','product__sub_category_name').annotate(
                            sales_this_year=Sum('sales_value',filter=Q(activity_year=get_current_year())),
                            sales_last_year=Sum('sales_value',filter=Q(activity_year=get_current_year()-1)),
                            sales_prev_year=Sum('sales_value',filter=Q(activity_year=get_current_year()-2)),

                            amnt_this_year=Sum('sales_amount',filter=Q(activity_year=get_current_year())),
                            amnt_last_year=Sum('sales_amount',filter=Q(activity_year=get_current_year()-1)),
                            amnt_prev_year=Sum('sales_amount',filter=Q(activity_year=get_current_year()-2)),
                           
                            prdn_this_year=Sum('production_amount',filter=Q(activity_year=get_current_year())),
                            prdn_last_year=Sum('production_amount',filter=Q(activity_year=get_current_year()-1)),
                            prdn_prev_year=Sum('production_amount',filter=Q(activity_year=get_current_year()-2))
                        )
        demand_supply = InputDemandSupply.objects.filter(company=company).values('input_type','input_unit__name','product__sub_category_name').annotate(
                            demand_this_year=Sum('demand',filter=Q(year=get_current_year())),
                            demand_last_year=Sum('demand',filter=Q(year=get_current_year()-1)),
                            demand_prev_year=Sum('demand',filter=Q(year=get_current_year()-2)),

                            supply_this_year=Sum('supply',filter=Q(year=get_current_year())),
                            supply_last_year=Sum('supply',filter=Q(year=get_current_year()-1)),
                            supply_prev_year=Sum('supply',filter=Q(year=get_current_year()-2)),
                        )
        employees = Employees.objects.filter(company=company,year_emp=get_current_year()).aggregate(
            male_temp = Sum('male',filter=Q(employment_type__icontains="Temporary")),
            female_temp=Sum('female',filter=Q(employment_type__icontains="Temporary")),
            male_perm = Sum('male',filter=Q(employment_type__icontains="Permanent")),
            female_perm=Sum('female',filter=Q(employment_type__icontains="Permanent")),
            male_foreign = Sum('male',filter=Q(employment_type__icontains="Foreign")),
            female_foreign=Sum('female',filter=Q(employment_type__icontains="Foreign")),
            )
        jobs_created = JobOpportunities.objects.filter(company=company,year_job=get_current_year()).aggregate(
            male_temp = Sum('male',filter=Q(job_type__icontains="Temporary")),
            female_temp=Sum('female',filter=Q(job_type__icontains="Temporary")),
            male_perm = Sum('male',filter=Q(job_type__icontains="Permanent")),
            female_perm=Sum('female',filter=Q(job_type__icontains="Permanent")),
            )
        edu_status = EducationalStatus.objects.filter(company=company,year_edu=get_current_year()).values('education_type').annotate(Sum('male'),Sum('female')).order_by('education_type')
        num_sex_in_psn = FemalesInPosition.objects.filter(company=company,year_fem=get_current_year()).aggregate(
                    female_in_high = Sum('high_position'),
                    female_in_med = Sum('med_position'),
                    male_in_high = Sum('high_position_male'),
                    male_in_med = Sum('med_position_male')
            )
        
        src_amnt_input = None
        market_destin = None
        market_target = None
        power_c = None
        try:
            src_amnt_input = SourceAmountIputs.objects.get(company=company,year_src=get_current_year())
            market_destin = MarketDestination.objects.get(company=company,year_destn=get_current_year())
            market_target = MarketTarget.objects.get(company=company,year_target=get_current_year())
            power_c = PowerConsumption.objects.get(company=company,year_pc=get_current_year())
        except SourceAmountIputs.DoesNotExist:
            src_amnt_input = None
        except MarketTarget.DoesNotExist:
            market_target = None
        except MarketDestination.DoesNotExist:
            market_destin = None
        except PowerConsumption.DoesNotExist:
            power_c = None

        context = {
                'company':company,
                'production_capacity':production_capacity,
                'inv_capital':inv_cap,
                'anual_input_need':input_need,
                'sales_perfornamce':sales_performance,
                'demand_supply':demand_supply,
                'employees':employees,
                'jobs_created':jobs_created,
                'edu_status':edu_status,
                'num_sex_posn':num_sex_in_psn,
                'src_amnt':src_amnt_input,
                'market_destin':market_destin,
                'market_target':market_target,
                'power_c':power_c,
                'years':{'this_yr':get_current_year(),'last_yr':get_current_year()-1,'prev_yr':get_current_year()-2}
            }

        pdf = render_to_pdf('admin/report/company_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %(company.name.upper())
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

@method_decorator(decorators,name='dispatch')
class GenerateProjectPdf(View):
    def get(self, request, *args, **kwargs):
        context = {}
        projects = InvestmentProject.objects.all()
        if self.kwargs['region'] != "all":
            projects = projects.filter(project_address__region=self.kwargs['region'])
            context['region'] = RegionMaster.objects.get(id=self.kwargs['region']).name
        if self.kwargs['sector'] != "all":
            projects = projects.filter(sector=self.kwargs['sector'])
            context['sector'] = self.kwargs['sector']
        if self.kwargs['sub_sector'] != "all":
            projects = projects.filter(product_type=self.kwargs['sub_sector'])
            context['sub_sector'] = Category.objects.get(id=self.kwargs['sub_sector']).category_name
        # form of ownership
        queryset = projects.values('ownership_form__name').annotate(Count('id')).order_by('ownership_form') 
        total_ownership = 0
        ownership_data = []
        for ownership in queryset:
            if ownership['ownership_form__name'] != None:
                total_ownership += int(ownership['id__count'])
                ownership_data.append({'label':ownership['ownership_form__name'],
                                    'data':ownership['id__count']})
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
        queryset_classificaion = projects.values('project_classification__name').annotate(Count('id')).order_by('project_classification') 
        total_classification = 0
        classification_data = []
        for ownership in queryset_classificaion:
            if ownership['project_classification__name'] != None:
                total_classification += int(ownership['id__count'])
                classification_data.append({'label':ownership['project_classification__name'],
                                    'data':ownership['id__count']})
        prodn_data = []
        for project in projects:
            pdata = ProjectProductQuantity.objects.filter(project=project).values(
                'product_tobe_produced','expected_normal_capacity')
            for p in pdata:
                prodn_data.append({
                    'project':project.project_name,
                    'sector':project.sector,
                    'product':p['product_tobe_produced'],
                    'nominal_capacity':p['expected_normal_capacity']
                })
        emp_data_total = []
        total_perm_emp = 0
        total_temp_emp=0
        for project in projects:
            employees_perm = Employees.objects.filter(projct=project,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(projct=project,employment_type__icontains="Temporary")
            
            for ep in employees_perm:
                total_perm_emp = (ep.male+ep.female)
            
            for et in employees_temp:
                total_temp_emp = (et.male+et.female)
            
            total = total_perm_emp+total_temp_emp
            emp_data_total.append({'project':project.project_name,'sector':project.sector,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        total_for_emp_m=0
        total_for_emp_f=0
        for_emp_data = []
        for project in projects:
            employees_foreign = Employees.objects.filter(projct=project,employment_type__icontains="Foreign")
            if employees_foreign.exists():
                for ef in employees_foreign:
                    total_for_emp_m += (ef.male)
                    total_for_emp_f += (ef.female)

                total = total_for_emp_m+total_for_emp_f
                for_emp_data.append({'project':project.project_name,'sector':project.sector,'data':total,'for_male':total_for_emp_m,'for_female':total_for_emp_f})
        job_created_data = []
        for project in projects:
            jobs_created_temp = JobOpportunities.objects.filter(project=project,job_type__icontains="Temporary",year_job=get_current_year())
            jobs_created_permanent = JobOpportunities.objects.filter(project=project,job_type__icontains="Permanent",year_job=get_current_year())
            if jobs_created_temp.exists() or jobs_created_permanent.exists():
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

                job_created_data.append({'project':project.project_name,'sector':project.sector,'data':{
                    'temporary_male':temp_male,'temporary_female':temp_female,
                    'permanent_male':permanent_male,'permanent_female':permanent_female
                }})
        femal_emp_data = []
        for project in projects:
            employees_perm = Employees.objects.filter(projct=project,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(projct=project,employment_type__icontains="Temporary")
            if employees_perm.exists() or employees_temp.exists():
                for ep in employees_perm:
                    total_perm_emp = (ep.female)
                
                for et in employees_temp:
                    total_temp_emp = (et.female)
                
                total = total_perm_emp+total_temp_emp
                femal_emp_data.append({'project':project.project_name,'sector':project.sector,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        education_status_data = []
        total_edu = 0
        for project in projects:
            queryset_edu = EducationalStatus.objects.filter(
                project=project,year_edu=get_current_year()).values('education_type').annotate(
                     Sum('male'),Sum('female'),total_edu=Sum('male')+Sum('female') ).order_by('education_type')
            fem_edu = 0
            male_edu = 0
            if queryset_edu.exists():
                for edu_data in queryset_edu:
                    fem_edu += edu_data['female__sum']
                    male_edu += edu_data['male__sum']
                    # total_edu += int(+)
                    education_status_data.append({'project':project.project_name,'sector':project.sector,'label':edu_data['education_type'],
                                        'data':int(edu_data['female__sum']+edu_data['male__sum'])})
            total_edu = fem_edu+male_edu
        context['filter_data'] = [
                                { 
                                    'data':projects.exclude(Q(target_market='')|Q(target_market=None)), 
                                    'label':"Number of investment projects with export plan "
                                },
                                { 
                                    'data':projects.filter(Q(target_market='')|Q(target_market=None)), 
                                    'label':"Number of investment projects wholly sell their product locally"
                                },
                                {
                                    'data':projects.exclude(Q(env_impac_ass_doc='')|Q(env_impac_ass_doc=None)),
                                    'label':"Number of investment projects that have Environmental impact assessment document"
                                },
                                ]
        
        context['total_edu'] = total_edu
        context['education_status_data'] = education_status_data
        context['total_fem_emp_data'] = femal_emp_data
        context['total_emp_data'] = emp_data_total
        context['job_created_data'] = job_created_data
        context['for_emp_data'] = for_emp_data
        context['nominal_data'] = prodn_data
        context['classification_data'] = classification_data
        context['total_class'] = total_classification
        context['inv_cap_data'] = total_inv_cap_data
        context['ownership_data'] = ownership_data
        context['total_ownership'] = total_ownership
        context['projects'] = projects
        pdf = render_to_pdf('admin/report/all_project_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %("Investment Project")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



@method_decorator(decorators,name='dispatch')
class GenerateProjectToPDF(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        context = {}
        project = InvestmentProject.objects.get(id=self.kwargs['pk'])
        inv_cap =  InvestmentCapital.objects.filter(project=project).annotate(
                        machinery = Sum('machinery_cost'),
                        building = Sum('building_cost'),
                        working = Sum('working_capital')
                    )
        employees = Employees.objects.filter(projct=project).aggregate(
            male_temp = Sum('male',filter=Q(employment_type__icontains="Temporary")),
            female_temp=Sum('female',filter=Q(employment_type__icontains="Temporary")),
            male_perm = Sum('male',filter=Q(employment_type__icontains="Permanent")),
            female_perm=Sum('female',filter=Q(employment_type__icontains="Permanent")),
            male_foreign = Sum('male',filter=Q(employment_type__icontains="Foreign")),
            female_foreign=Sum('female',filter=Q(employment_type__icontains="Foreign")),
            )
        jobs_created = JobOpportunities.objects.filter(project=project).aggregate(
            male_temp = Sum('male',filter=Q(job_type__icontains="Temporary")),
            female_temp=Sum('female',filter=Q(job_type__icontains="Temporary")),
            male_perm = Sum('male',filter=Q(job_type__icontains="Permanent")),
            female_perm=Sum('female',filter=Q(job_type__icontains="Permanent")),
            )
        edu_status = EducationalStatus.objects.filter(project=project).values('education_type').annotate(Sum('male'),Sum('female')).order_by('education_type')
        
        context = {
                'project':project,
                'inv_capital':inv_cap,
                'employees':employees,
                'jobs_created':jobs_created,
                'edu_status':edu_status,
            }

        pdf = render_to_pdf('admin/report/project_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %(project.project_name.upper())
            content = "inline; filename='%s'" %(filename)
            download = self.request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
