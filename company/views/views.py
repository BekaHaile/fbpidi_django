import datetime
import json
import csv

from django.db import IntegrityError
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
from accounts.models import CompanyAdmin,UserProfile
from product.models import Order,OrderProduct,Product

from company.forms import *
from collaborations.models import *
from chat.models import  ChatMessages

class CreateMyCompanyProfile(LoginRequiredMixin,CreateView):
    model=Company
    form_class = CompanyProfileForm
    template_name = "admin/company/create_company_form.html"

    def get(self,*args,**kwargs):
        if self.request.user.is_company_admin:
            if self.request.user.get_company() != None:
                return redirect("admin:index")
            else:
                return super().get(*args,**kwargs)
        elif self.request.user.is_superuser:
            if self.request.user.get_company() != None:
                return redirect("admin:index")
            else:
                return redirect("admin:create_fbpidi_company")
        else:
            return redirect("admin:index")


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self,form):
        company = form.save(commit=False)
        company.contact_person = self.request.user
        company.craeted_by = self.request.user
        company.save()
        messages.success(self.request,"Company Profile Created")
        return redirect("admin:create_mycompany_detail",pk=company.id)


class CreateCompanyProfile(LoginRequiredMixin,CreateView):
    model = Company
    form_class = CompanyProfileForm_Superadmin
    template_name = "admin/company/create_company_form_1.html"

    def form_valid(self,form):
        company = form.save(commit=False)
        company.created_by = self.request.user
        company.save()
        messages.success(self.request,"Company Profile Created")
        return redirect("admin:create_company_detail",pk=company.id)

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_company_profile")


class CreateMyCompanyDetail(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = MyCompanyDetailForm
    template_name = "admin/company/create_company_detail.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateMyCompanyDetail,self).get_form_kwargs()
        kwargs.update({'main_type': Company.objects.get(id=self.kwargs['pk']).main_category})
        return kwargs


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
        company.management_tools.set(form.cleaned_data.get('management_tools'))
        company.source_of_energy.set(form.cleaned_data.get('source_of_energy'))
        company.support_required.set(form.cleaned_data.get('support_required'))
        company.lab_test_analysis.set(form.cleaned_data.get('lab_test_analysis'))
        company.lab_equipment.set(form.cleaned_data.get('lab_equipment'))
        company.certification.set(form.cleaned_data.get('certification'))
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.save()
        messages.success(self.request,"Company Detail Information Added")
        return redirect("admin:update_company_info",pk=self.kwargs['pk'])
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_mycompany_detail",pk=self.kwargs['pk'])

class CreateCompanyDetail(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = MyCompanyDetailForm
    template_name = "admin/company/create_company_detail_1.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateCompanyDetail,self).get_form_kwargs()
        kwargs.update({'main_type': Company.objects.get(id=self.kwargs['pk']).main_category})
        return kwargs


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
        company.management_tools.set(form.cleaned_data.get('management_tools'))
        company.source_of_energy.set(form.cleaned_data.get('source_of_energy'))
        company.support_required.set(form.cleaned_data.get('support_required'))
        company.lab_test_analysis.set(form.cleaned_data.get('lab_test_analysis'))
        company.lab_equipment.set(form.cleaned_data.get('lab_equipment'))
        company.certification.set(form.cleaned_data.get('certification'))
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.save()
        messages.success(self.request,"Company Detail Information Added")
        return redirect("admin:companies")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_company_detail",pk=self.kwargs['pk'])

class ViewMyCompanyProfile(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = 'admin/company/company_detail.html'

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(ViewMyCompanyProfile,self).get_form_kwargs()
        kwargs.update({'main_type': Company.objects.get(id=self.kwargs['pk']).main_category})
        return kwargs

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
        context['title'] = Company.objects.get(id=self.kwargs['pk']).name
        return context

    def form_valid(self,form):
        company = form.save(commit=False)
        company.category.set(form.cleaned_data.get('category'))
        company.management_tools.set(form.cleaned_data.get('management_tools'))
        company.source_of_energy.set(form.cleaned_data.get('source_of_energy'))
        company.support_required.set(form.cleaned_data.get('support_required'))
        company.lab_test_analysis.set(form.cleaned_data.get('lab_test_analysis'))
        company.lab_equipment.set(form.cleaned_data.get('lab_equipment'))
        company.certification.set(form.cleaned_data.get('certification'))
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.save()
        messages.success(self.request,"Company Detail Information Updated")
        if self.request.user.is_superuser:
            return redirect("admin:company_detail",pk=self.kwargs['pk'])
        else:
            return redirect("admin:update_company_info",pk=self.kwargs['pk'])

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        if self.request.user.is_superuser:
            return redirect("admin:company_detail",pk=self.kwargs['pk'])
        else:
            return redirect("admin:update_company_info",pk=self.kwargs['pk'])
    
class CompaniesView(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies.html"
    paginate_by = 8


    def get_queryset(self):
        return Company.objects.all().exclude(main_category="FBPIDI")

class CompaniesDetailView(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "admin/company/company_profile_detail.html"
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = CompanyRatingForm
        context['address_form'] = CompanyAddressForm
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
        context['title'] = Company.objects.get(id=self.kwargs['pk']).name
        return context

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CompaniesDetailView,self).get_form_kwargs()
        kwargs.update({'main_type': Company.objects.get(id=self.kwargs['pk']).main_category})
        return kwargs

class RateCompany(LoginRequiredMixin,UpdateView):
    model=Company
    form_class = CompanyRatingForm

    def form_valid(self,form):
        rating = form.save(commit=False)
        rating.last_updated_by=self.request.user
        rating.last_updated_date = timezone.now()
        rating.save()
        return redirect("admin:company_detail", pk=self.kwargs['pk'])


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


class CreateInvestmentCapital(LoginRequiredMixin,CreateView):
    model = InvestmentCapital
    form_class = InvestmentCapitalForm
    

    def form_valid(self,form):
        try:
            if InvestmentCapital.objects.filter(year=form.cleaned_data.get("year_inv"),company=Company.objects.get(id=self.kwargs['company'])).exists():
                return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
            else:
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

# Company Data Creation Views
class CreatePowerConsumption(LoginRequiredMixin,CreateView):
    model = PowerConsumption
    form_class = PowerConsumptionForm

    def form_valid(self,form):
        try:
            if PowerConsumption.objects.filter(day=form.cleaned_data.get("day"),company=Company.objects.get(id=self.kwargs['company'])).exists():
                return JsonResponse({'error': True, 'message': 'Data For this Date Already Exists'})
            else:
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
                if Employees.objects.filter(year=form.cleaned_data.get("year_emp"),employment_type=form.cleaned_data.get('employment_type'), company=Company.objects.get(id=self.kwargs['company'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
                else:
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
                if JobOpportunities.objects.filter(year=form.cleaned_data.get("year_job"),job_type=form.cleaned_data.get('job_type'),company=Company.objects.get(id=self.kwargs['company'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
                else:
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
                if EducationalStatus.objects.filter(year=form.cleaned_data.get("year_edu"),education_type=form.cleaned_data.get('education_type'),company=Company.objects.get(id=self.kwargs['company'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
                else:
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
                if FemalesInPosition.objects.filter(year=form.cleaned_data.get("year_fem"),company=Company.objects.get(id=self.kwargs['company'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
                else:
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
                if SourceAmountIputs.objects.filter(year=form.cleaned_data.get("year_src"),company=Company.objects.get(id=self.kwargs['company'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
                else:
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
                if MarketDestination.objects.filter(year=form.cleaned_data.get("year_destn"),company=Company.objects.get(id=self.kwargs['company'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
                else:
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
                if MarketTarget.objects.filter(year=form.cleaned_data.get("year_target"),company=Company.objects.get(id=self.kwargs['company'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
                else:
                    target = form.save(commit=False)
                    target.year = form.cleaned_data.get("year_target")
                    target.company = Company.objects.get(id=self.kwargs['company'])
                    target.save()
                    return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Year Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Company Does Not Exist'})
            except MarketTarget.DoesNotExist:
                return JsonResponse({'error': True, 'message': 'Data For this Year Already Exists'})
        else:
            return JsonResponse({'error': True, 'message': form.errors})

class CheckYearField(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        company = Company.objects.get(id=self.kwargs['company'])
        if self.kwargs['model'] == "investment":
            
            try:
                investment=InvestmentCapital.objects.get(company=company,year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data': json.loads(serializers.serialize('json',[investment],ensure_ascii=False))[0] })
            except InvestmentCapital.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "employee":
            try:
                employee = Employees.objects.get(company=company,year=self.kwargs['year'],employment_type=self.request.POST['emp_type']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[employee],ensure_ascii=False))[0]})
            except Employees.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "jobs_created":
            try:
                jobs = JobOpportunities.objects.get(company=company,year=self.kwargs['year'],job_type=self.request.POST['job_type']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[jobs],ensure_ascii=False))[0]})
            except JobOpportunities.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "education":
            try:
                education = EducationalStatus.objects.get(company=company,year=self.kwargs['year'],education_type=self.request.POST['edu_type']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[education],ensure_ascii=False))[0]})
            except EducationalStatus.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "female_emp":
            try:
                female_emp = FemalesInPosition.objects.get(company=company,year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[female_emp],ensure_ascii=False))[0]})
            except FemalesInPosition.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "src_amnt":
            try:
                src_amnt = SourceAmountIputs.objects.get(company=company,year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[src_amnt],ensure_ascii=False))[0]})
            except SourceAmountIputs.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "power_consumption":
            try:
                power_consumed = PowerConsumption.objects.get(company=company,day=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Date Exists",
                                    'data':json.loads(serializers.serialize('json',[power_consumed],ensure_ascii=False))[0]})
            except PowerConsumption.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are Good to Go"})
        elif self.kwargs['model'] == "destination":
            try:
                destination = MarketDestination.objects.get(company=company,year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[destination],ensure_ascii=False))[0]})
            except MarketDestination.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "target":
            try:
                target = MarketTarget.objects.get(company=company,year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[target],ensure_ascii=False))[0]})
            except MarketTarget.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})

# Company Yearly data Update Views
class UpdateInvestmentCapital(LoginRequiredMixin,UpdateView):
    model = InvestmentCapital
    form_class = InvestmentCapitalForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "inv_capital" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Investment Capital Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=InvestmentCapital.objects.get(id=self.kwargs['pk']).company.id)

class UpdateEmployees(LoginRequiredMixin,UpdateView):
    model = Employees
    form_class = EmployeesForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "employeees" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Employees Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=Employees.objects.get(id=self.kwargs['pk']).company.id)

class UpdateCertificate(LoginRequiredMixin,UpdateView):
    model = Certificates
    form_class = CertificateForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "certificate" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Certificate Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=Certificates.objects.get(id=self.kwargs['pk']).company.id)


class UpdateJobsCreated(LoginRequiredMixin,UpdateView):
    model = JobOpportunities
    form_class = JobCreatedForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "job_oportunity" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Jobs Created Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=JobOpportunities.objects.get(id=self.kwargs['pk']).company.id)

class UpdateEducationStatus(LoginRequiredMixin,UpdateView):
    model = EducationalStatus
    form_class = EducationStatusForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "education" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Education Status Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=EducationalStatus.objects.get(id=self.kwargs['pk']).company.id)

class UpdateFemalesInPosn(LoginRequiredMixin,UpdateView):
    model = FemalesInPosition
    form_class = FemalesInPositionForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "females_in_posn" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Females in Position Level Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=FemalesInPosition.objects.get(id=self.kwargs['pk']).company.id)

class UpdateSrcAmntInputs(LoginRequiredMixin,UpdateView):
    model = SourceAmountIputs
    form_class = SourceAmountIputsForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "src_amnt_inpts" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Source & Ammount of inputs Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=SourceAmountIputs.objects.get(id=self.kwargs['pk']).company.id)

class UpdatePowerConsumption(LoginRequiredMixin,UpdateView):
    model = PowerConsumption
    form_class = PowerConsumptionForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "power_consumption" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Power Consumption Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=PowerConsumption.objects.get(id=self.kwargs['pk']).company.id)

class UpdateMarketTarget(LoginRequiredMixin,UpdateView):
    model = MarketTarget
    form_class = MarketTargetForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "market_target" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Market Target Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=MarketTarget.objects.get(id=self.kwargs['pk']).company.id)

class UpdateMarketDestination(LoginRequiredMixin,UpdateView):
    model = MarketDestination
    form_class = MarketDestinationForm
    template_name = "admin/company/company_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "market_destination" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        messages.success(self.request,"Market Destination Data Updated")
        return redirect("admin:update_company_info",pk=data.company.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_company_info",pk=MarketDestination.objects.get(id=self.kwargs['pk']).company.id)

class ListInvestmentProject(LoginRequiredMixin,ListView):
    model = InvestmentProject
    template_name = "admin/company/project_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return InvestmentProject.objects.all()
        elif self.request.user.is_company_admin:
            return InvestmentProject.objects.filter(company=Company.objects.get(contact_person=self.request.user))
        elif self.request.user.is_company_staff:
            return InvestmentProject.objects.filter(company=CompanyStaff.objects.get(user=self.request.user).company)


class CreateMyInvestmentProject(LoginRequiredMixin,CreateView):
    model = InvestmentProject
    form_class = InvestmentProjectForm
    template_name = "admin/company/create_project_form.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateMyInvestmentProject,self).get_form_kwargs()
        kwargs.update({'contact_person': UserProfile.objects.filter(created_by=self.request.user)})
        return kwargs


    def form_valid(self,form):
        project = form.save(commit=False)
        company = None
        if self.request.user.is_company_admin:
            company = Company.objects.get(contact_person=self.request.user)
        elif self.request.user.is_company_staff:
            company = CompanyStaff.objects.get(user=self.request.user).company
        
        project.company = company
        project.created_by = self.request.user
        project.save()
        messages.success(self.request,'Investment Project Created,Please Complete The Following!')
        return redirect("admin:create_project_detail",pk=project.id)



class CreateInvestmentProject(LoginRequiredMixin,CreateView):
    model = InvestmentProject
    form_class = InvestmentProjectForm_ForSuperAdmin
    template_name = "admin/company/create_project_form_admin.html"

    def form_valid(self,form):
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.save()
        messages.success(self.request,'Investment Project Created,Please Complete The Following!')
        return redirect("admin:create_project_detail_admin",pk=project.id)

class CreateInvestmentProjectDetail(LoginRequiredMixin,UpdateView):
    model=InvestmentProject
    form_class=InvestmentProjectDetailForm
    template_name = "admin/company/create_project_detail.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateInvestmentProjectDetail,self).get_form_kwargs()
        kwargs.update({'sector': InvestmentProject.objects.get(id=self.kwargs['pk']).sector})
        return kwargs
    
    def form_valid(self,form):
        project=form.save(commit=False)
        project.product_type.set(form.cleaned_data.get('product_type'))
        project.last_updated_by=self.request.user
        project.last_updated_date = timezone.now()
        project.save()
        messages.success(self.request,"Project Detail Added Succesfully")
        return redirect("admin:project_list")

class CreateInvestmentProjectDetail_Admin(LoginRequiredMixin,UpdateView):
    model=InvestmentProject
    form_class=InvestmentProjectDetailForm_Admin
    template_name = "admin/company/create_project_detail_admin.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateInvestmentProjectDetail_Admin,self).get_form_kwargs()
        kwargs.update({'sector': InvestmentProject.objects.get(id=self.kwargs['pk']).sector})
        kwargs.update({'contact_person': UserProfile.objects.filter(created_by=
                InvestmentProject.objects.get(id=self.kwargs['pk']).company.contact_person
                )| UserProfile.objects.filter(id=
                InvestmentProject.objects.get(id=self.kwargs['pk']).company.contact_person.id
                ) })
        return kwargs
    
    def form_valid(self,form):
        project=form.save(commit=False)
        project.product_type.set(form.cleaned_data.get('product_type'))
        project.last_updated_by=self.request.user
        project.last_updated_date = timezone.now()
        project.save()
        messages.success(self.request,"Project Detail Added Succesfully")
        return redirect("admin:project_list")

class UpdateInvestmentProject(LoginRequiredMixin,UpdateView):
    model=InvestmentProject
    form_class = ProjectUpdateForm
    template_name = "admin/company/update_project_form.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(UpdateInvestmentProject,self).get_form_kwargs()
        kwargs.update({'sector': InvestmentProject.objects.get(id=self.kwargs['pk']).sector})
        kwargs.update({'contact_person': UserProfile.objects.filter(created_by=
                InvestmentProject.objects.get(id=self.kwargs['pk']).company.contact_person
                )})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['usage_form'] = LandUsageForm
        context['pstate_form'] = ProjectStatusForm
        context['product_form'] = ProjectProductForm
        try:
            context['land_usage_data'] = LandUsage.objects.get(project=self.kwargs['pk'])
        except LandUsage.DoesNotExist:
            context['land_usage_data']=None
        
        try:
            context['project_state'] = ProjectState.objects.get(project=self.kwargs['pk'])
        except ProjectState.DoesNotExist:
            context['project_state'] = None
        return context

    def form_valid(self,form):
        project=form.save(commit=False)
        project.product_type.set(form.cleaned_data.get('product_type'))
        project.last_updated_by=self.request.user
        project.last_updated_date = timezone.now()
        project.save()
        messages.success(self.request,"Project Detail Added Succesfully")
        return redirect("admin:project_list")

class CreateLandUsage(LoginRequiredMixin,CreateView):
    model=LandUsage
    form_class = LandUsageForm

    def form_valid(self,form):
        lu = form.save(commit=False)
        lu.project = InvestmentProject.objects.get(id=self.kwargs['project'])
        lu.save()
        return redirect("admin:update_project",pk=self.kwargs['project'])

class UpdateLandUsage(LoginRequiredMixin,UpdateView):
    model=LandUsage
    form_class = LandUsageForm

    def form_valid(self,form):
        form.save()
        return redirect("admin:update_project",pk=LandUsage.objects.get(id=self.kwargs['pk']).project.id)

class CreateProductQty(LoginRequiredMixin,CreateView):
    model=ProjectProductQuantity
    form_class = ProjectProductForm

    def form_valid(self,form):
        pp = form.save(commit=False)
        pp.project = InvestmentProject.objects.get(id=self.kwargs['project'])
        pp.save()
        return redirect("admin:update_project",pk=self.kwargs['project'])


class UpdateProductQty(LoginRequiredMixin,UpdateView):
    model=ProjectProductQuantity
    form_class = ProjectProductForm

    def form_valid(self,form):
        form.save()
        return redirect("admin:update_project",pk=ProjectProductQuantity.objects.get(id=self.kwargs['pk']).project.id)

class CreateProjectState(LoginRequiredMixin,CreateView):
    model=ProjectState
    form_class = ProjectStatusForm

    def form_valid(self,form):
        ps = form.save(commit=False)
        ps.project = InvestmentProject.objects.get(id=self.kwargs['project'])
        ps.save()
        return redirect("admin:update_project",pk=self.kwargs['project'])


class UpdateProjectState(LoginRequiredMixin,UpdateView):
    model=ProjectState
    form_class = ProjectStatusForm


    def form_valid(self,form):
        form.save()
        return redirect("admin:update_project",pk=ProjectState.objects.get(id=self.kwargs['pk']).project.id)

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_project")

class CreateFbpidiCompanyProfile(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        context['form'] = InistituteForm
        if self.request.user.is_superuser:
            return render(self.request,"admin/company/company_form_fbpidi.html",context)
        else:
            return redirect("admin:index")

    def post(self,form):
        form = InistituteForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            fbpidi = form.save(commit=False)
            fbpidi.main_category = "FBPIDI"
            fbpidi.contact_person = self.request.user
            fbpidi.save()
            return redirect("admin:index")
        else:
            messages.warning(self.request,form.errors)
            return redirect("admin:create_fbpidi_company")


class ViewFbpidiCompany(LoginRequiredMixin,UpdateView):
    model=Company
    form_class = InistituteForm
    template_name="admin/company/company_profile_fbpidi.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['address_form'] = CompanyAddressForm
        try:
            context['address'] = CompanyAddress.objects.get(company=Company.objects.get(id=self.kwargs['pk']))
        except CompanyAddress.DoesNotExist:
            context['address'] = None
        return context

    def form_valid(self,form):
        fbpidi = form.save(commit=False)
        fbpidi.last_updated_by=self.request.user
        fbpidi.last_updated_date=timezone.now()
        fbpidi.save()
        messages.success(self.request,"Company Updated")
        return redirect("admin:view_fbpidi_company",pk=fbpidi.id)
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:view_fbpidi_company",self.kwargs['pk'])


class SliderImageList(LoginRequiredMixin,ListView):
    model=HomePageSlider
    template_name = "admin/company/slider_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return HomePageSlider.objects.all()
        else:
            return HomePageSlider.objects.filter(company=self.request.user.get_company())


class CreateSliderImage(LoginRequiredMixin,CreateView):
    model=HomePageSlider
    form_class = SliderImageForm
    template_name = "admin/company/slider_create_form.html"

    def form_valid(self,form):
        try:
            image = form.save(commit=False)
            image.company = Company.objects.get(id=self.kwargs['company'])
            image.created_by= self.request.user
            image.save()
            messages.success(self.request,"Image Uploaded Successfully")
            return redirect("admin:slider_list")
        except Exception as e:
            messages.warning(self.request,e)
            return redirect("admin:create_slider",company=self.kwargs['company'])    
            
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_slider",company=self.kwargs['company'])

class UpdateSliderImage(LoginRequiredMixin,UpdateView):
    model=HomePageSlider
    form_class = SliderImageForm
    template_name = "admin/company/slider_update_form.html"

    def form_valid(self,form):
        image = form.save(commit=False)
        image.last_updated_by=self.request.user
        image.last_updated_date = timezone.now()
        image.save()
        messages.success(self.request,"Image Updated Successfully")
        return redirect("admin:slider_list")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_slider",pk=self.kwargs['pk'])
 
#  Company Report Views




############## newly added, delete this commet after everything has worked right

class CompanyByMainCategory(ListView):
    model = Company
    template_name = "frontpages/company/company_list.html"
    paginate_by = 6
    
    def get_queryset(self):
        if self.kwargs['option'] == "Beverage":
            return Company.objects.filter(main_category="Beverage")
        elif self.kwargs['option'] == "Food":
            return Company.objects.filter(main_category="Food")
        elif self.kwargs['option'] == "Pharmaceuticals":
            return Company.objects.filter(main_category="Pharmaceuticals")
        elif self.kwargs['option'] == "all":
            return Company.objects.all().exclude(main_category="FBPIDI")

class ProjectList(ListView):
    model = InvestmentProject
    template_name = "frontpages/project/project_list.html"

class ProjectDetail(DetailView):
    model = InvestmentProject
    template_name = "frontpages/project/project_detail.html"

class CompanyHomePage(DetailView):
    model = Company
    template_name="frontpages/company/business-5.html"  

class CompanyAbout(DetailView):
    model=Company
    template_name="frontpages/company/about.html"


class CompanyContact(DetailView):
    model=Company
    template_name="frontpages/company/contact.html"

class CompanyProductList(DetailView):
    model= Company
    template_name = "frontpages/company/blog-grid-center.html"

class CompanyProjectList(DetailView):
    model= Company
    template_name = "frontpages/company/blog-grid-center.html"

class CompanyNewsList(ListView):
    model = News
    template_name = "frontpages/company/company_news.html"
    context_object_name = "news_list"

    def get_queryset(self):
        try:
            return News.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "#######3 the excptio is ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context