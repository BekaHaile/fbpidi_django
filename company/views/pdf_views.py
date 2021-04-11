
import datetime
from django.http import HttpResponse
from django.views.generic import View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.db.models import *

from company.render import render_to_pdf 
from company.models import *
from product.models import *

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

class GenerateAllCompanyPdf(View):
    def get(self, request, *args, **kwargs):
        company_by_sector = Company.objects.all().exclude(main_category="FBPIDI").values('main_category').annotate(Count('id')).order_by('main_category')
        # company_by_region_sector = 
        context = {
            'company_by_sector':company_by_sector,
        }
        pdf = render_to_pdf('admin/report/all_report_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %("IIMS-Yearly-Report")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
          



class GenerateCompanyToPDF(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        context = {}
        company = Company.objects.get(id=self.request.POST['pk'])
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
 