import datetime
import json
from django.db import IntegrityError
from django.forms.models import model_to_dict
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

from company.models import *
from accounts.models import CompanyAdmin,User
from product.models import Order,OrderProduct

from company.forms import *
from chat.models import ChatGroup, ChatMessage

class CreateMyCompanyProfile(LoginRequiredMixin,CreateView):
    model=Company
    form_class = CompanyProfileForm
    template_name = "admin/company/create_company_form.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self,form):
        company = form.save(commit=False)
        company.geo_location = form.cleaned_data.get('location')
        company.ownership_form = form.cleaned_data.get('ownership')
        company.contact_person = self.request.user
        company.craeted_by = self.request.user
        company.save()
        messages.success(self.request,"Company Profile Created")
        return redirect("admin:create_company_detail",pk=company.id)


class CreateCompanyProfile(LoginRequiredMixin,CreateView):
    model = Company
    form_class = CompanyProfileForm_Superadmin
    template_name = "admin/company/create_company_form_1.html"

    def form_valid(self,form):
        company = form.save(commit=False)
        company.ownership_form = form.cleaned_data.get("ownership")
        company.created_by = self.request.user
        company.save()
        messages.success(self.request,"Company Profile Created")
        return redirect("admin:create_company_detail",pk=company.id)

    def form_invalid(self,form):
        print(form.errors)

class CreateCompanyAddress(LoginRequiredMixin,CreateView):
    model = CompanyAddress
    form_class = CompanyAddressForm

    def form_valid(self,form):
        address = form.save(commit=False)
        address.company = Company.objects.get(id=self.kwargs['company'])
        address.save()
        return JsonResponse({'error':False,'message':'Company Address Saved Successfully'})

class UpdateCompanyAddress(LoginRequiredMixin,UpdateView):
    model = CompanyAddress
    form_class = CompanyAddressForm

    def form_valid(self,form):
        form.save()
        return JsonResponse({'error':False,'message':'Company Address Updated Successfully'})


class CreateCompanyDetail(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyDetailForm
    template_name = "admin/company/create_company_detail.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['inv_capital_form'] = InvestmentCapitalForm
        context['certificate_form'] = CertificateForm
        context['employees_form'] = EmployeesForm
        context['job_created_form'] = JobCreatedForm
        context['edication_form'] = EducationStatusForm
        context['female_posn_form'] = FemalesInPositionForm
        context['src_amnt_input_form'] = SourceAmountIputsForm
        context['destination_form'] = MarketDestinationForm
        context['target_form'] = MarketTargetForm
        context['consumption_form'] = PowerConsumptionForm
        context['address_form'] = CompanyAddressForm
        return context

    def form_valid(self,form):
        company = form.save(commit=False)
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.working_hours = form.cleaned_data.get('working_hours')
        company.certification.set(form.cleaned_data.get('certification'))
        company.management_tools.set(form.cleaned_data.get('management_tools'))
        company.source_of_energy = form.cleaned_data.get('source_of_energy')
        company.support_required = form.cleaned_data.get('support_required')
        company.save()
        messages.success(self.request,"Company Detail Information Added")
        return redirect("admin:update_company_info",pk=self.kwargs['pk'])

class ViewMyCompanyProfile(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = 'admin/company/company_detail.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['inv_capital_form'] = InvestmentCapitalForm
        context['certificate_form'] = CertificateForm
        context['employees_form'] = EmployeesForm
        context['job_created_form'] = JobCreatedForm
        context['edication_form'] = EducationStatusForm
        context['female_posn_form'] = FemalesInPositionForm
        context['src_amnt_input_form'] = SourceAmountIputsForm
        context['destination_form'] = MarketDestinationForm
        context['target_form'] = MarketTargetForm
        context['consumption_form'] = PowerConsumptionForm
        context['address_form'] = CompanyAddressForm
        return context

    def form_valid(self,form):
        company = form.save(commit=False)
        company.category.set(form.cleaned_data.get('category')) 
        company.geo_location = form.cleaned_data.get('location')
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.save()
        messages.success(self.request,"Company Detail Information Updated")
        return redirect("admin:update_company_info",pk=self.kwargs['pk'])



class CreateInvestmentCapital(LoginRequiredMixin,CreateView):
    model = InvestmentCapital
    form_class = InvestmentCapitalForm

    def form_valid(self,form):
        try:
            company_inv_cap = form.save(commit=False)
            company_inv_cap.company = Company.objects.get(id=self.kwargs['company'])
            company_inv_cap.year = form.cleaned_data.get('year_inv')
            company_inv_cap.save()
            return JsonResponse({'error': False, 'message': "Sucessfully Added Investment Capital"})
        except Company.DoesNotExist:
            return JsonResponse({'error': True, 'message': "Company Does Not Exist"})
        except IntegrityError as e:
            return JsonResponse({'error': True, 'message': "Data For the selected year already exists"})
            
    def form_invalid(self,form):
        return JsonResponse({'error': True, 'message': form.errors}) 

class CreatePowerConsumption(LoginRequiredMixin,CreateView):
    model = PowerConsumption
    form_class = PowerConsumptionForm

    def form_valid(self,form):
        try:
            power_consm = form.save(commit=False)
            power_consm.company = Company.objects.get(id=self.kwargs['company'])
            power_consm.save()
            return JsonResponse({'error': False, 'message': "Sucessfully Added Power Consumption Data"})
        except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Day Already Exists"})
        except Company.DoesNotExist:
            return JsonResponse({'error': True, 'message': "Company Does Not Exist"})
            
    def form_invalid(self,form):
        return JsonResponse({'error': True, 'message': "Power consumption with this Day already exists."}) 


class CreateCertificates(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = CertificateForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.company = Company.objects.get(id=self.kwargs['company'])
            certificate.save()
            return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
        else:
            return JsonResponse({'error': True, 'message': form.errors}) 

class CreateEmployees(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = EmployeesForm(self.request.POST)
        if form.is_valid():
            try:
                employee = form.save(commit=False)
                employee.year = form.cleaned_data.get('year_emp')
                employee.company = Company.objects.get(id=self.kwargs['company'])
                employee.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Employee Data For this Year Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Company Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors})  

class CreateJobsCreatedYearly(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = JobCreatedForm(self.request.POST)
        if form.is_valid():
            try:
                jobs = form.save(commit=False)
                jobs.year = form.cleaned_data.get('year_job')
                jobs.company = Company.objects.get(id=self.kwargs['company'])
                jobs.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Year Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Company Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors})     

class CreateEducationStatus(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = EducationStatusForm(self.request.POST)
        if form.is_valid():
            try:
                education = form.save(commit=False)
                education.year = form.cleaned_data.get('year_edu')
                education.company = Company.objects.get(id=self.kwargs['company'])
                education.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Year Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Company Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors}) 

class CreateFemaleinPosition(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = FemalesInPositionForm(self.request.POST)
        if form.is_valid():
            try:
                femaleposn = form.save(commit=False)
                femaleposn.year = form.cleaned_data.get("year_fem")
                femaleposn.company = Company.objects.get(id=self.kwargs['company'])
                femaleposn.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Year Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Company Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors}) 

class CreateAnualSourceofInputs(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = SourceAmountIputsForm(self.request.POST)
        if form.is_valid():
            try:
                inputs = form.save(commit=False)
                inputs.year = form.cleaned_data.get("year_src")
                inputs.company = Company.objects.get(id=self.kwargs['company'])
                inputs.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Year Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Company Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors})


class CreateMarketDestination(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = MarketDestinationForm(self.request.POST)
        if form.is_valid():
            try:
                destination = form.save(commit=False)
                destination.year = form.cleaned_data.get("year_destn")
                destination.company = Company.objects.get(id=self.kwargs['company'])
                destination.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Year Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Company Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors})


class CreateMarketTarget(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = MarketTargetForm(self.request.POST)
        if form.is_valid():
            try:
                target = form.save(commit=False)
                target.year = form.cleaned_data.get("year_target")
                target.company = Company.objects.get(id=self.kwargs['company'])
                target.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Year Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Company Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors})

class CheckYearField(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        if self.kwargs['model'] == "investment":
            try:
                # json.dumps(model_to_dict(investment))
                investment=InvestmentCapital.objects.get(company=self.kwargs['company'],year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data': json.loads(serializers.serialize('json',[investment],ensure_ascii=False))[0] })
            except InvestmentCapital.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "employee":
            try:
                employee = Employees.objects.get(company=self.kwargs['company'],year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[employee],ensure_ascii=False))[0]})
            except Employees.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "jobs_created":
            try:
                jobs = JobOpportunities.objects.get(company=self.kwargs['company'],year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[jobs],ensure_ascii=False))[0]})
            except JobOpportunities.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "education":
            try:
                education = EducationalStatus.objects.get(company=self.kwargs['company'],year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[education],ensure_ascii=False))[0]})
            except EducationalStatus.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "female_emp":
            try:
                female_emp = FemalesInPosition.objects.get(company=self.kwargs['company'],year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[female_emp],ensure_ascii=False))[0]})
            except FemalesInPosition.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "src_amnt":
            try:
                src_amnt = SourceAmountIputs.objects.get(company=self.kwargs['company'],year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[src_amnt],ensure_ascii=False))[0]})
            except SourceAmountIputs.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "power_consumption":
            try:
                power_consumed = PowerConsumption.objects.get(company=self.kwargs['company'],day=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Date Exists",
                                    'data':json.loads(serializers.serialize('json',[power_consumed],ensure_ascii=False))[0]})
            except PowerConsumption.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are Good to Go"})
        elif self.kwargs['model'] == "destination":
            try:
                destination = MarketDestination.objects.get(company=self.kwargs['company'],year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[destination],ensure_ascii=False))[0]})
            except MarketDestination.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "target":
            try:
                target = MarketTarget.objects.get(company=self.kwargs['company'],year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[target],ensure_ascii=False))[0]})
            except MarketTarget.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})


class CreateCompanyProfileAfterSignUp(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        form = CompanyForm()
        try:
            Company.objects.get(user=self.request.user)
            return redirect("admin:view_company_profile")
        except:
            return render(self.request,"admin/company/company_form_signup.html",{"form":form})

    def post(self, *args,**kwargs):
        form = CompanyForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.product_category = form.cleaned_data.get("product_category")
            company.user = self.request.user
            company.save()
            messages.success(self.request,"Company Profile Created")
            return redirect("admin:index")
        return render(self.request,"admin/company/company_form_signup.html",{'form':form})


class ViewCompanyProfile(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        company = None
        try:
            if self.request.user.is_company_admin:
                company = Company.objects.get(user=self.request.user)
            if self.request.user.is_company_staff:
                comp_staff = CompanyStaff.objects.get(user = self.request.user)
                company = Company.objects.get(id=comp_staff.company.id)
            sol_form = CompanySolutionForm()
            staff_users = CompanyStaff.objects.filter(company=company)
            solutions = CompanySolution.objects.filter(company=company)
            events = CompanyEvent.objects.filter(company=company)
            event_form = CompanyEventForm
            banks = Bank.objects.all()
            company_bank_accounts = CompanyBankAccount.objects.filter(company=company)
            account_form = CompanyBankAccountForm()

            context = {'company':company,'staff_users':staff_users,'solution_form':sol_form,'solutions':solutions,
                        'event_form':event_form,'events':events, 
                        'banks':banks, 'company_bank_accounts': company_bank_accounts, 'account_form':account_form}
            if "active_tab" in self.kwargs:#to activate a specific tab while opening the company profile, first used for message (inbox tab)
                context ['active_tab'] = self.kwargs['active_tab']
                   
            return render(self.request,'admin/company/company_profile_detail.html',context)
        except ObjectDoesNotExist:
            return redirect("admin:create_company_profile")
        
    def post(self,*args,**kwargs):
        try:
            company = Company.objects.get(id=self.kwargs['id'])
            # for company profile
            if self.request.POST['flag'] == "profile":
                company.company_name = self.request.POST['company_name']
                company.company_name_am = self.request.POST['company_name_am']
                company.location = self.request.POST['location']
                company.city = self.request.POST['city']
                company.phone_number = self.request.POST['phone_number']
                company.number_of_employees = self.request.POST['number_of_employees']
                company.certification = self.request.POST['certification']
                company.capital = self.request.POST['capital']
                company.established_year = self.request.POST['established_year']
                company.postal_code = self.request.POST['postal_code']
                company.detail = self.request.POST['detail']
                company.detail_am = self.request.POST['detail_am']
                company.color = self.request.POST['color']
                company.facebook_link = self.request.POST['facebook_link']
                company.twiter_link = self.request.POST['twiter_link']
                company.linkedin_link = self.request.POST['linkedin_link']
                company.google_link = self.request.POST['google_link']
                company.instagram_link = self.request.POST['instagram_link']
                company.pintrest_link = self.request.POST['pintrest_link']
                if self.request.FILES.get('company_logo') != None:
                    company.company_logo = self.request.FILES.get('company_logo')
                if self.request.FILES.get('company_intro') != None:
                    company.company_intro = self.request.FILES.get('company_intro')
            elif self.request.POST['flag'] == "trade":
                # for Company Trade capacity
                company.incoterms =  self.request.POST['incoterms']
                company.incoterms_am =  self.request.POST['incoterms_am']
                company.terms_of_payment =self.request.POST['terms_of_payment']
                company.average_lead_time =self.request.POST['average_lead_time']
                company.average_lead_time_am =self.request.POST['average_lead_time_am']
                print(self.request.POST['no_trading_staff'])
                if self.request.POST['no_trading_staff'] != None:
                    company.no_trading_staff = self.request.POST['no_trading_staff']
                if self.request.POST['export_yr'] != None:
                    company.export_yr = self.request.POST['export_yr']
                if self.request.POST['export_percentage'] != None:
                    company.export_percentage =self.request.POST['export_percentage']
                company.main_market =  self.request.POST['main_market']
                company.main_market_am = self.request.POST['main_market_am']
                company.nearest_port =  self.request.POST['nearest_port']
                company.nearest_port_am =self.request.POST['nearest_port_am']
            elif self.request.POST['flag'] == "production":
                # production capacity
                company.r_and_d_capacity =  self.request.POST['r_and_d_capacity']
                company.r_and_d_capacity_am =  self.request.POST['r_and_d_capacity_am']
                company.no_of_rnd_staff =    self.request.POST['no_of_rnd_staff']
                company.no_production_lines =    self.request.POST['no_production_lines']
                company.anual_op_value =    self.request.POST['anual_op_value']
                company.anual_op_main_products =   self.request.POST['anual_op_main_products']
                company.anual_op_main_products_am =   self.request.POST['anual_op_main_products_am']
            company.save()
            messages.success(self.request,"Company Updated")
            if self.request.user.is_superuser:
                return redirect("admin:company_detail",id=company.id)
            else:
                return redirect("admin:view_company_profile")
        except ObjectDoesNotExist:
            messages.warning(self.request,"Company Does Not Exist")
            if self.request.user.is_superuser:
                return redirect("admin:company_detail",id=company.id)
            else:
                return redirect("admin:view_company_profile")
    
class CompaniesView(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies.html"

class CompaniesDetailView(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "admin/company/company_profile_detail.html"

class CreateCompanySolution(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = CompanySolutionForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.company = Company.objects.get(id=self.kwargs['company_id'])
            solution.save()
            messages.success(self.request,"Services Created Successfully")
        messages.warning(self.request,form.errors)
        return redirect("admin:view_company_profile")


class CreateCompanyEvent(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = CompanyEventForm(self.request.POST,self.request.FILES)
        company = Company.objects.get(id=self.kwargs['company_id'])
        if form.is_valid():
            event = form.save(commit=False)
            if event.start_date.date() > timezone.now().date():
                event.status = "Upcoming"
            elif event.start_date.date() == timezone.now().date():
                 event.status = 'Open'
            else:
                event.status = 'Closed' 
            event.company = company
            event.created_by = self.request.user               
            event.save()
            messages.success(self.request,"Event Created Successfully")
            if company.company_type == "fbpidi":
                return redirect("admin:view_fbpidi_company")
            else:
                return redirect("admin:view_company_profile")
        else:
            messages.warning(self.request,form.errors)
            if company.company_type == "fbpidi":
                return redirect("admin:view_fbpidi_company")
            else:
                return redirect("admin:view_company_profile")


def change_to_datetime(calender_date):
    str_date = datetime.datetime.strptime(calender_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    return datetime.datetime.strptime(str_date,'%Y-%m-%d' )

class EditCompanyEvent(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = CompanyEventForm(self.request.POST,self.request.FILES)
        event = CompanyEvent.objects.get(id=self.kwargs['id']) 
        if form.is_valid():
            form.save(commit=False)
            event.title = self.request.POST['title']
            event.title_am = self.request.POST['title_am']
            event.description = self.request.POST['description']
            event.description_am = self.request.POST['description_am']
            event.start_date = change_to_datetime(self.request.POST['start_date'])
            event.end_date = change_to_datetime(self.request.POST['end_date'])
            if event.start_date.date() > timezone.now().date():
                event.status = "Upcoming"
            elif event.start_date.date() == timezone.now().date():
                 event.status = 'Open'
            else:
                event.status = 'Closed' 
            if self.request.FILES:
                event.image = self.request.FILES['image']
            event.last_updated_by = self.request.user
            event.last_updated_date = timezone.now()
            event.save() 
            messages.success(self.request,"Event Edited Successfully")
            return redirect("admin:view_fbpidi_company") if self.request.user.is_superuser else redirect("admin:view_company_profile")
            
        else:
            messages.warning(self.request,form.errors)
            return redirect("admin:view_fbpidi_company") if self.request.user.is_superuser else redirect("admin:view_company_profile")


class CreateFbpidiCompanyProfile(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = FbpidiCompanyForm()
        return render(self.request,"admin/company/company_form_fbpidi.html",{'form':form})

    def post(self,*args,**kwargs):
        form = FbpidiCompanyForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            fbpidi = form.save(commit=False)
            fbpidi.company_type = "fbpidi"
            fbpidi.company_type_am = "fbpidi"
            fbpidi.user=self.request.user
            fbpidi.save()
            return redirect('admin:index')
        else:
            return render(self.request,"admin/company/company_form_fbpidi.html",{'form':form})


class ViewFbpidiCompany(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        fbpidi = Company.objects.get(company_type="fbpidi")
        events = CompanyEvent.objects.all()
        event_form = CompanyEventForm
        banks = Bank.objects.all()
        company_bank_accounts = CompanyBankAccount.objects.filter(company=fbpidi)
        account_form = CompanyBankAccountForm()
        context = {'company':fbpidi,'events':events,'event_form':event_form, 'banks':banks, 'company_bank_accounts': company_bank_accounts, 'account_form':account_form}
        context['active_tab'] = 'inbox'
        # if 'active_tab' in self.kwargs:
            # print("########## Active tab is", self.kwargs['active_tab'])
            # context['active_tab'] = self.kwargs['active_tab']

        return render(self.request,"admin/company/company_profile_fbpidi.html",context)
    
    def post(self,*args,**kwargs):
        company = Company.objects.get(id=self.kwargs['id'])
        try:
            if self.request.POST['flag'] == "profile":
                company.company_name = self.request.POST['company_name']
                company.company_name_am = self.request.POST['company_name_am']
                company.location = self.request.POST['location']
                company.city = self.request.POST['city']
                company.phone_number = self.request.POST['phone_number']
                company.postal_code = self.request.POST['postal_code']
                company.established_year = self.request.POST['established_year']
                company.detail = self.request.POST['detail']
                company.detail_am = self.request.POST['detail_am']
            elif self.request.POST['flag'] == "aditional":
                company.facebook_link = self.request.POST['facebook_link']
                company.twiter_link = self.request.POST['twiter_link']
                company.linkedin_link = self.request.POST['linkedin_link']
                company.google_link = self.request.POST['google_link']
                company.instagram_link = self.request.POST['instagram_link']
                company.pintrest_link = self.request.POST['pintrest_link']
                if self.request.FILES.get('company_logo') != None:
                    company.company_logo = self.request.FILES.get('company_logo')
                if self.request.FILES.get('company_intro') != None:
                    company.company_intro = self.request.FILES.get('company_intro')
            company.save()
            messages.success(self.request,"Company Updated")
            return redirect("admin:view_fbpidi_company")
        except ObjectDoesNotExist:
            messages.warning(self.request,"Company Does Not Exist")
            return redirect("admin:view_fbpidi_company")


class CreateCompanyBankAccount(LoginRequiredMixin, View):
        def post(self, *ags, **kwargs):
            form  = CompanyBankAccountForm(self.request.POST)
            if form.is_valid:
                    account = form.save(commit=False)
                    company = Company.objects.get(id = self.kwargs['id'])
                    account.company = company
                    account.save()
                    messages.success(self.request, "New Bank Account Successfully Added!")
                    if company.company_type == "fbpidi":
                        return redirect("admin:view_fbpidi_company")
                    else:
                        return redirect("admin:view_company_profile")
            else:   
                messages.warning(self.request, "Error While Adding New Bank Account!")  
                company = Company.objects.get(id = self.kwargs['id'])
                if company.company_type == "fbpidi":
                        return redirect("admin:view_fbpidi_company")
                else:
                        return redirect("admin:view_company_profile")      


class EditCompanyBankAccount(LoginRequiredMixin, View):
       
        def post(self, *ags, **kwargs):
            form  = CompanyBankAccountForm(self.request.POST)
            if form.is_valid:     
                bank_account = CompanyBankAccount.objects.get(id = self.kwargs['id'])
                bank_account.bank = Bank.objects.get(id =self.request.POST['bank'])
                bank_account.account_number = self.request.POST['account_number']
                bank_account.save()
                messages.success(self.request, "Bank Account Successfully Edited!")
                
                if bank_account.company.company_type == "fbpidi":
                        return redirect("admin:view_fbpidi_company")
                else:
                        return redirect("admin:view_company_profile")      

            else:   
                messages.warning(self.request, "Error While Adding New Bank Account!")  
                company = Company.objects.get(id = self.kwargs['id'])
                if company.company_type == "fbpidi":
                        return redirect("admin:view_fbpidi_company")
                else:
                        return redirect("admin:view_company_profile")      


class DeleteCompanyBankAccount(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        message = ""
        redirect_url = ""
        if self.request.user.is_superuser:
            redirect_url = "admin:view_fbpidi_company"
        else:
            redirect_url = "admin:view_company_profile"

        if self.kwargs['id'] :
            bank_account = CompanyBankAccount.objects.filter(id = self.kwargs['id']  ).first()
            
            if bank_account:
                bank_account.delete()
                message = "Bank Account Deleted Successfully"
                messages.success(self.request,message)
                
                return redirect(redirect_url)
            else:
                messages.warning(self.request, "NO such tender was found!")
                return redirect(redirect_url)


        else:
            messages.warning(self.request, "Nothing selected!")
            return redirect(redirect_url)



############## newly added, delete this commet after everything has worked right

class MnfcCompanyByMainCategory(View):
    def get(self,*args,**kwargs):
        companies = Company.objects.all()
        company_list = []
        context = {}
        if self.kwargs['option'] == "Beverage":
            for company in companies:
                if company.product_category.category_name.category_type == "Beverage":
                    company_list.append(company)
        elif self.kwargs['option'] == "Food":
            for company in companies:
                if company.product_category.category_name.category_type == "Food":
                    company_list.append(company)
        elif self.kwargs['option'] == "Pharmaceuticals":
            for company in companies:
                if company.product_category.category_name.category_type == "Pharmaceuticals":
                    company_list.append(company)
        elif self.kwargs['option'] == "all":
            for company in companies:
                company_list.append(company)
        context['companies'] = company_list
        context['count'] = len(company_list)
        return render(self.request,"frontpages/company/company_list.html",context)

class SupCompanyByMainCategory(View):
    def get(self,*args,**kwargs):
        companies = Company.objects.all()
        company_list = []
        context = {}
        if self.kwargs['option'] == "Beverage":
            for company in companies:
                if company.product_category.category_name.category_type == "Beverage":
                    company_list.append(company)
        elif self.kwargs['option'] == "Food":
            for company in companies:
                if company.product_category.category_name.category_type == "Food":
                    company_list.append(company)
        elif self.kwargs['option'] == "Pharmaceuticals":
            for company in companies:
                if company.product_category.category_name.category_type == "Pharmaceuticals":
                    company_list.append(company)
        elif self.kwargs['option'] == "all":
            for company in companies:
                company_list.append(company)
        context['companies'] = company_list
        context['count'] = len(company_list)
        return render(self.request,"frontpages/company/company_list.html",context)

