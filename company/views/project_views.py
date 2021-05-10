import datetime
import json
import csv

from django.db import IntegrityError
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.contrib import messages
from django.views.generic import CreateView,UpdateView,ListView,View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.core import serializers

from company.models import *
from accounts.models import CompanyAdmin,UserProfile
from product.models import Product
from admin_site.views.dropdowns import image_cropper
from admin_site.views.views import record_activity
from admin_site.decorators import company_created,company_is_active


from company.forms import *

decorators = [never_cache, company_created(),company_is_active()]
@method_decorator(decorators,name='dispatch')
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

@method_decorator(decorators,name='dispatch')
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
        record_activity(self.request.user,"InvestmentProject","Investment project data created",project.id)
        messages.success(self.request,'Investment Project Created,Please Complete The Following!')
        return redirect("admin:create_project_detail",pk=project.id)

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return render(self.request,"admin/company/create_project_form.html",{'form':form})

@method_decorator(decorators,name='dispatch')
class CreateInvestmentProject(LoginRequiredMixin,CreateView):
    model = InvestmentProject
    form_class = InvestmentProjectForm_ForSuperAdmin
    template_name = "admin/company/create_project_form_admin.html"

    def form_valid(self,form):
        project = form.save(commit=False)
        project.created_by = self.request.user
        project.save()
        record_activity(self.request.user,"InvestmentProject","Investment project data Created",project.id)
        image_cropper(form.cleaned_data.get('x'),form.cleaned_data.get('y'),
                    form.cleaned_data.get('width'),form.cleaned_data.get('height'),
                    project.image,400,400)
        messages.success(self.request,'Investment Project Created,Please Complete The Following!')
        return redirect("admin:create_project_detail_admin",pk=project.id)
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return render(self.request,"admin/company/create_project_form_admin.html",{'form':form})

    def form_invalid(self, form):
        print("form is invalide", form.errors)
        messages.warning(self.request,"Form is invalid! Check your input again!")
        return redirect("admin:create_project")


@method_decorator(decorators,name='dispatch')
class CreateInvestmentProjectDetail(LoginRequiredMixin,UpdateView):
    model=InvestmentProject
    form_class=InvestmentProjectDetailForm
    template_name = "admin/company/create_project_detail.html"

    def get_form_kwargs(self,*args,**kwargs):
        kwargs = super(CreateInvestmentProjectDetail,self).get_form_kwargs()
        kwargs.update({'sector': InvestmentProject.objects.get(id=self.kwargs['pk']).sector})
        return kwargs
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['inv_capital_form'] = InvestmentCapitalForm
        context['employees_form'] = EmployeesFormProject
        context['job_created_form'] = JobCreatedFormProject
        context['edication_form'] = EducationStatusFormProject
        context['usage_form'] = LandUsageForm
        context['pstate_form'] = ProjectStatusForm
        context['product_form'] = ProjectProductForm
        context['address_form'] = CompanyAddressForm
        return context

    
    def form_valid(self,form):
        project=form.save(commit=False)
        project.product_type.set(form.cleaned_data.get('product_type'))
        project.last_updated_by=self.request.user
        project.last_updated_date = timezone.now()
        project.save()
        messages.success(self.request,"Project Detail Added Succesfully")
        return redirect("admin:project_list")
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_project_detail",pk=self.kwargs['pk'])

@method_decorator(decorators,name='dispatch')
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
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['inv_capital_form'] = InvestmentCapitalForm
        context['employees_form'] = EmployeesFormProject
        context['job_created_form'] = JobCreatedFormProject
        context['edication_form'] = EducationStatusFormProject
        context['usage_form'] = LandUsageForm
        context['pstate_form'] = ProjectStatusForm
        context['product_form'] = ProjectProductForm
        context['address_form'] = CompanyAddressForm
        return context
    
    def form_valid(self,form):
        project=form.save(commit=False)
        project.product_type.set(form.cleaned_data.get('product_type'))
        project.last_updated_by=self.request.user
        project.last_updated_date = timezone.now()
        project.save()
        image_cropper(form.cleaned_data.get('x'),form.cleaned_data.get('y'),
                    form.cleaned_data.get('width'),form.cleaned_data.get('height'),
                    project.image,400,400)
        messages.success(self.request,"Project Detail Added Succesfully")
        return redirect("admin:project_list")

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:create_project_detail_admin",pk=self.kwargs['pk'])


@method_decorator(decorators,name='dispatch')
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
        context['inv_capital_form'] = InvestmentCapitalForm
        context['employees_form'] = EmployeesFormProject
        context['job_created_form'] = JobCreatedFormProject
        context['edication_form'] = EducationStatusFormProject
        context['usage_form'] = LandUsageForm
        context['pstate_form'] = ProjectStatusForm
        context['product_form'] = ProjectProductForm
        context['address_form'] = CompanyAddressForm
        try:
            context['land_usage_data'] = LandUsage.objects.get(project=self.kwargs['pk'])
        except LandUsage.DoesNotExist:
            context['land_usage_data']=None
        
        try:
            context['inv_cap_data'] = InvestmentCapital.objects.filter(project=self.kwargs['pk']).latest('-timestamp')
        except InvestmentCapital.DoesNotExist:
            context['inv_cap_data']=None
        
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
        record_activity(self.request.user,"InvestmentProject","Investment project data Updated",project.id)
        image_cropper(form.cleaned_data.get('x'),form.cleaned_data.get('y'),
                    form.cleaned_data.get('width'),form.cleaned_data.get('height'),
                    project.image,400,400)
        messages.success(self.request,"Project Detail Added Succesfully")
        return redirect("admin:project_list")

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_project",pk=self.kwargs['pk'])

@method_decorator(decorators,name='dispatch')
class CreateLandUsage(LoginRequiredMixin,CreateView):
    model=LandUsage
    form_class = LandUsageForm

    def form_valid(self,form):
        try:
            lu = form.save(commit=False)
            lu.project = InvestmentProject.objects.get(id=self.kwargs['project'])
            lu.save()
            record_activity(self.request.user,"LandUsage","Land Usage data Created",lu.id)
            return JsonResponse({'error':False,'message':'Land Usage Created Successfully!!!'})
        except InvestmentProject.DoesNotExist:
            return JsonResponse({'error':True,'message':'Investment Project Doesn\'t Exist'})
        except IntegrityError as e:
            return JsonResponse({'error':True,'message':'Data Already Exists'})
    
    def form_invalid(self,form):
        return JsonResponse({'error':True,'message':form.errors})


@method_decorator(decorators,name='dispatch')
class UpdateLandUsage(LoginRequiredMixin,UpdateView):
    model=LandUsage
    form_class = LandUsageForm

    def form_valid(self,form):
        lu = form.save()
        record_activity(self.request.user,"LandUsage","Land Usage data Updated",lu.id)
        return redirect("admin:update_project",pk=LandUsage.objects.get(id=self.kwargs['pk']).project.id)
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_land_use",pk=self.kwargs['pk'])

@method_decorator(decorators,name='dispatch')
class CreateProductQty(LoginRequiredMixin,CreateView):
    model=ProjectProductQuantity
    form_class = ProjectProductForm

    def form_valid(self,form):
        try:
            pp = form.save(commit=False)
            pp.project = InvestmentProject.objects.get(id=self.kwargs['project'])
            pp.save()
            record_activity(self.request.user,"ProjectProductQuantity","Product Quantity data Updated",pp.id)
            return JsonResponse({'error':False,'message':'Product Quantity Created Successfully!!!'})
        except InvestmentProject.DoesNotExist:
            return JsonResponse({'error':True,'message':'Investment Project Doesn\'t Exist'})
    
    def form_invalid(self,form):
        return JsonResponse({'error':True,'message':form.errors})

@method_decorator(decorators,name='dispatch')
class UpdateProductQty(LoginRequiredMixin,UpdateView):
    model=ProjectProductQuantity
    form_class = ProjectProductForm
    template_name = "admin/company/project_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "product_quantity" 
        return context

    def form_valid(self,form):
        pp=form.save()
        record_activity(self.request.user,"ProjectProductQuantity","Product Quantity data Updated",pp.id)
        return redirect("admin:update_project",pk=ProjectProductQuantity.objects.get(id=self.kwargs['pk']).project.id)
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_product_qty",pk=self.kwargs['pk'])


@method_decorator(decorators,name='dispatch')
class CreateProjectState(LoginRequiredMixin,CreateView):
    model=ProjectState
    form_class = ProjectStatusForm

    def form_valid(self,form):
        try:
            ps = form.save(commit=False)
            ps.project = InvestmentProject.objects.get(id=self.kwargs['project'])
            ps.save()
            record_activity(self.request.user,"ProjectState","Project State data Created",ps.id)
            return JsonResponse({'error':False,'message':'Project Status Created Successfully!!!'})
        except InvestmentProject.DoesNotExist:
            return JsonResponse({'error':True,'message':'Investment Project Doesn\'t Exist'})
        except IntegrityError as e:
            return JsonResponse({'error':True,'message':'Data Already Exists'})

    def form_invalid(self,form):
        return JsonResponse({'error':True,'message':form.errors})

@method_decorator(decorators,name='dispatch')
class UpdateProjectState(LoginRequiredMixin,UpdateView):
    model=ProjectState
    form_class = ProjectStatusForm
    template_name = "admin/company/project_data_update.html"

    def form_valid(self,form):
        ps = form.save()
        record_activity(self.request.user,"ProjectState","Project State data Updated",ps.id)
        return redirect("admin:update_project",pk=ProjectState.objects.get(id=self.kwargs['pk']).project.id)

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_project_state",pk=self.kwargs['pk'])


@method_decorator(decorators,name='dispatch')
class CreateInvestmentCapitalForProject(LoginRequiredMixin,CreateView):
    model = InvestmentCapital
    form_class = InvestmentCapitalForm
    

    def form_valid(self,form):
        try:
            project_invcap = form.save(commit=False)
            project_invcap.project = InvestmentProject.objects.get(id=self.kwargs['project'])
            project_invcap.save()
            record_activity(self.request.user,"InvestmentCapital","Investment capital data Created",project_invcap.id)
            return JsonResponse({'error':False,'message':'Investment Capital Data Added'})
        except InvestmentProject.DoesNotExist:
            return JsonResponse({'error':True,'message':'Investment Project Doesn\'t Exist'})
            
    def form_invalid(self,form):
        return JsonResponse({'error':True,'message':form.errors})

@method_decorator(decorators,name='dispatch')
class UpdateInvestmentCapitalForProject(LoginRequiredMixin,UpdateView):
    model = InvestmentCapital
    form_class = InvestmentCapitalForm
    template_name = "admin/company/project_data_update.html"

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['flag'] = "inv_capital"
        return context

    def form_valid(self,form):
        inv_cap = form.save()
        record_activity(self.request.user,"InvestmentCapital","Investment capital data Updated",inv_cap.id)
        messages.success(self.request,"Investment Capital Data Updated")
        return redirect("admin:update_project",pk=InvestmentCapital.objects.get(id=self.kwargs['pk']).project.id)

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_inv_cap_project",pk=self.kwargs['pk'])

 
@method_decorator(decorators,name='dispatch')
class CreateEmployeesProject(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = EmployeesFormProject(self.request.POST)
        if form.is_valid():
            try:
                if Employees.objects.filter(employment_type=form.cleaned_data.get('employment_type'), projct=InvestmentProject.objects.get(id=self.kwargs['project'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Category Already Exists'})
                else:
                    employee = form.save(commit=False)
                    employee.projct = InvestmentProject.objects.get(id=self.kwargs['project'])
                    employee.save()
                    record_activity(self.request.user,"Employees","Employees data Created",employee.id)
                    return JsonResponse({'error': False, 'message': form.cleaned_data.get('employment_type')+'Employees Data Uploaded Successfully for'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Employee Data For this Category Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Project Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors})  

@method_decorator(decorators,name='dispatch')
class CreateJobsCreatedProject(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = JobCreatedFormProject(self.request.POST)
        if form.is_valid():
            try:
                if JobOpportunities.objects.filter(job_type=form.cleaned_data.get('job_type'),project=InvestmentProject.objects.get(id=self.kwargs['project'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Category Already Exists'})
                else:
                    jobs = form.save(commit=False)
                    jobs.project = InvestmentProject.objects.get(id=self.kwargs['project'])
                    jobs.save()
                    record_activity(self.request.user,"JobOpportunities","Jobs Created data Created",jobs.id)
                    return JsonResponse({'error': False, 'message': form.cleaned_data.get('job_type')+' Job Oportunities Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Category Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Project Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors})     

@method_decorator(decorators,name='dispatch')
class CreateEducationStatusProject(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = EducationStatusFormProject(self.request.POST)
        if form.is_valid():
            try:
                if EducationalStatus.objects.filter(education_type=form.cleaned_data.get('education_type'),project=InvestmentProject.objects.get(id=self.kwargs['project'])).exists():
                    return JsonResponse({'error': True, 'message': 'Data For this Education Type Already Exists'})
                else:
                    education = form.save(commit=False)
                    education.project = InvestmentProject.objects.get(id=self.kwargs['project'])
                    education.save()
                    record_activity(self.request.user,"EducationalStatus","Educational Status data Created",education.id)
                    return JsonResponse({'error': False, 'message': form.cleaned_data.get('education_type')+' Educational Status Uploaded Successfully'})
            except IntegrityError as e:
                return JsonResponse({'error':True,'message':"Data For this Category Already Exists"})
            except Company.DoesNotExist:
                return JsonResponse({'error':True,'message':'Project Does Not Exist'})
        else:
            return JsonResponse({'error': True, 'message': form.errors}) 

@method_decorator(decorators,name='dispatch')
class UpdateEmployeesProject(LoginRequiredMixin,UpdateView):
    model = Employees
    form_class = EmployeesFormProject
    template_name = "admin/company/project_data_update.html"


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "employees" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        record_activity(self.request.user,"Employees","Employees data Updated",data.id)
        messages.success(self.request,"Employees Data Updated")
        return redirect("admin:update_project",pk=data.project.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_project",pk=Employees.objects.get(id=self.kwargs['pk']).projct.id)

@method_decorator(decorators,name='dispatch')
class UpdateJobsCreatedProject(LoginRequiredMixin,UpdateView):
    model = JobOpportunities
    form_class = JobCreatedFormProject
    template_name = "admin/company/project_data_update.html"


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "job_oportunity" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        record_activity(self.request.user,"JobOpportunities","Jobs Created data Updated",data.id)
        messages.success(self.request,"Jobs Created Data Updated")
        return redirect("admin:update_project",pk=data.project.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_project",pk=JobOpportunities.objects.get(id=self.kwargs['pk']).project.id)

@method_decorator(decorators,name='dispatch')
class UpdateEducationStatusProject(LoginRequiredMixin,UpdateView):
    model = EducationalStatus
    form_class = EducationStatusFormProject
    template_name = "admin/company/project_data_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "education" 
        return context
    
    def form_valid(self,form):
        data = form.save()
        record_activity(self.request.user,"EducationalStatus","Educational Status data Updated",data.id)
        messages.success(self.request,"Education Status Data Updated")
        return redirect("admin:update_project",pk=data.project.id)

    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_project",pk=EducationalStatus.objects.get(id=self.kwargs['pk']).project.id)

@method_decorator(decorators,name='dispatch')
class CreateProjectAddress(LoginRequiredMixin,CreateView):
    model = CompanyAddress
    form_class = CompanyAddressForm

    def form_valid(self,form):
        try:
            address = form.save(commit=False)
            address.project = InvestmentProject.objects.get(id=self.kwargs['project'])
            address.save()
            record_activity(self.request.user,"CompanyAddress","Project Address Created",address.id)
            return JsonResponse({'error':False,'message':'Investment Project Address Saved Successfully'})
        except IntegrityError as e:
            return JsonResponse({'error':True,'message':'Investment Project Address is Already Added'})
        

@method_decorator(decorators,name='dispatch')
class CheckYearFieldProject(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        project = InvestmentProject.objects.get(id=self.kwargs['project'])
        if self.kwargs['model'] == "employee":
            try:
                employee = Employees.objects.get(projct=project,employment_type=self.request.POST['emp_type']) 
                return JsonResponse({"error":True,"message":"Data For this Category Exists",
                                    'data':json.loads(serializers.serialize('json',[employee],ensure_ascii=False))[0]})
            except Employees.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "jobs_created":
            try:
                jobs = JobOpportunities.objects.get(project=project,job_type=self.request.POST['job_type']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[jobs],ensure_ascii=False))[0]})
            except JobOpportunities.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})
        elif self.kwargs['model'] == "education":
            try:
                education = EducationalStatus.objects.get(project=project,education_type=self.request.POST['edu_type']) 
                return JsonResponse({"error":True,"message":"Data For this Year Exists",
                                    'data':json.loads(serializers.serialize('json',[education],ensure_ascii=False))[0]})
            except EducationalStatus.DoesNotExist:
                return JsonResponse({"error":False,"message":"You are good to go"})

def mark_complete(request,pk):
    if request.method == 'GET':
        try:
            project = InvestmentProject.objects.get(id=pk)
            if project.project_complete == False:
                project.project_complete = True
                project.save()
                messages.success(request,"You Have marked Your Project Complete")
            else:
                project.project_complete = False
                project.save()
                messages.success(request,"You Have marked Your Project Incomplete")
            return redirect("admin:update_project",pk=pk)
        except InvestmentProject.DoesNotExist:
            return redirect('admin:error_404')