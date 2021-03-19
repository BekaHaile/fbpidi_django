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
from product.models import Order,OrderProduct,Product

from company.forms import *
from collaborations.models import *
from chat.models import ChatGroup, ChatMessage, ChatMessages

class CreateMyCompanyProfile(LoginRequiredMixin,CreateView):
    model=Company
    form_class = CompanyProfileForm
    template_name = "admin/company/create_company_form.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
    def get(self,*args,**kwargs):
        if self.request.user.get_company() != None:
            messages.warning(self.request,"You Have A Company Profile")
            return redirect("admin:index")
        else:
            return redirect("admin:create_company_profile")

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
        print(form.errors)
        return redirect("admin:index")


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
        company.certification.set(form.cleaned_data.get('certification'))
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.save()
        messages.success(self.request,"Company Detail Information Added")
        return redirect("admin:update_company_info",pk=self.kwargs['pk'])

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
        company.certification.set(form.cleaned_data.get('certification'))
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.save()
        messages.success(self.request,"Company Detail Information Added")
        return redirect("admin:companies")

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
        return context

    def form_valid(self,form):
        company = form.save(commit=False)
        company.category.set(form.cleaned_data.get('category'))
        company.management_tools.set(form.cleaned_data.get('management_tools'))
        company.certification.set(form.cleaned_data.get('certification'))
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.save()
        messages.success(self.request,"Company Detail Information Updated")
        return redirect("admin:update_company_info",pk=self.kwargs['pk'])

    
class CompaniesView(LoginRequiredMixin,ListView):
    model = Company
    template_name = "admin/company/companies.html"

class CompaniesDetailView(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = "admin/company/company_profile_detail.html"
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_form'] = CompanyRatingForm
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
        company = Company.objects.get(id=self.kwargs['company'])
        if self.kwargs['model'] == "investment":
            
            try:
                # json.dumps(model_to_dict(investment))
                investment=InvestmentCapital.objects.get(company=company,year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data': json.loads(serializers.serialize('json',[investment],ensure_ascii=False))[0] })
            except InvestmentCapital.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "employee":
            try:
                employee = Employees.objects.get(company=company,year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[employee],ensure_ascii=False))[0]})
            except Employees.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "jobs_created":
            try:
                jobs = JobOpportunities.objects.get(company=company,year=self.kwargs['year']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[jobs],ensure_ascii=False))[0]})
            except JobOpportunities.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "education":
            try:
                education = EducationalStatus.objects.get(company=company,year=self.kwargs['year']) 
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
                )})
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


class AdminCompanyEventList(LoginRequiredMixin, ListView):
    model = CompanyEvent
    template_name = "admin/collaborations/admin_companyevent_list.html"
    context_object_name = "events"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CompanyEventForm.objects.all()
        else: 
            return CompanyEvent.objects.filter(company =  self.request.user.get_company())

class CreateCompanyEvent(LoginRequiredMixin, CreateView):
        model = CompanyEvent
        form_class = CompanyEventForm
        template_name = "admin/collaborations/create_events.html"

        def form_valid(self,form):
            event = form.save(commit=False)
            if event.start_date.date() > timezone.now().date():
                event.status = "Upcoming"
            elif event.start_date.date() == timezone.now().date():
                 event.status = 'Open'
            else:
                event.status = 'Closed' 
            event.company = self.request.user.get_company()
            event.created_by = self.request.user               
            event.save()
            messages.success(self.request,"Event Created Successfully")
            return redirect('admin:admin_companyevent_list')

        def form_invalid(self,form):
            messages.warning(self.request,form.errors)
            return redirect('admin:create_companyevent')


# class EditCompanyEvent(LoginRequiredMixin, UpdateView):
#         model = CompanyEvent
#         form_class = CompanyEventForm
#         template_name = "admin/collaborations/create_events.html"

#         # def get_context_data(self,**kwargs):
#         #     context = super().get_context_data(**kwargs)
#         #     context['edit'] = True
           

#         def form_valid(self,form):
#             event = form.save(commit=False)
#             event.title.set (self.request.POST['title'])
#             event.title_am.set(self.request.POST['title_am'])
#             event.description.set(self.request.POST['description'])
#             event.description_am.set( self.request.POST['description_am'])
#             event.start_date.set( change_to_datetime(self.request.POST['start_date']))
#             event.end_date.set(change_to_datetime(self.request.POST['end_date']))
#             if event.start_date.date() > timezone.now().date():
#                 event.status.set("Upcoming")
#             elif event.start_date.date() == timezone.now().date():
#                  event.status.set('Open')
#             else:
#                 event.status.set( 'Closed' )
#             if self.request.FILES:
#                 event.image.set(self.request.FILES['image'])
#             event.last_updated_by = self.request.user
#             event.last_updated_date = timezone.now()
#             event.save() 
#             messages.success(self.request,"Event Edited Successfully")
#             return redirect("admin:admin_companyevent_list")


#         def form_invalid(self,form):
#             messages.warning(self.request,form.errors)
#             return redirect("admin:admin_companyevent_list")

def change_to_datetime(calender_date):
    str_date = datetime.datetime.strptime(calender_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    return datetime.datetime.strptime(str_date,'%Y-%m-%d' )

class EditCompanyEvent(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        return render(self.request, "admin/collaborations/create_events.html",{'edit':True,'event':CompanyEvent.objects.get(id = self.kwargs['pk'])})

    def post(self,*args,**kwargs):
        form = CompanyEventForm(self.request.POST,self.request.FILES)
        event = CompanyEvent.objects.get(id=self.kwargs['pk']) 
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
            return redirect('admin:admin_companyevent_list')
        else:
            messages.warning(self.request,form.errors)
            return redirect('admin:admin_companyevent_list')

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
        context = {'company':fbpidi,'events':events,'event_form':event_form, 'banks':banks, 'company_bank_accounts': company_bank_accounts,'chat_list':get_grouped_chats(self.request.user), 'account_form':account_form}
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
            return Company.objects.all()


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