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
from product.models import Order,OrderProduct,Product

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
        messages.success(self.request,'Investment Project Created,Please Complete The Following!')
        return redirect("admin:create_project_detail",pk=project.id)


@method_decorator(decorators,name='dispatch')
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


@method_decorator(decorators,name='dispatch')
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
    
    def form_valid(self,form):
        project=form.save(commit=False)
        project.product_type.set(form.cleaned_data.get('product_type'))
        project.last_updated_by=self.request.user
        project.last_updated_date = timezone.now()
        project.save()
        messages.success(self.request,"Project Detail Added Succesfully")
        return redirect("admin:project_list")

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
        context['usage_form'] = LandUsageForm
        context['pstate_form'] = ProjectStatusForm
        context['product_form'] = ProjectProductForm
        context['inv_capital_form'] = InvestmentCapitalForm
        context['land_aquisition'] = LandAquisitionForm
        try:
            context['land_usage_data'] = LandUsage.objects.get(project=self.kwargs['pk'])
        except LandUsage.DoesNotExist:
            context['land_usage_data']=None
        
        try:
            context['land_aqsn_data'] = LandAquisition.objects.get(project=self.kwargs['pk'])
        except LandAquisition.DoesNotExist:
            context['land_aqsn_data']=None
        
        try:
            context['inv_cap_data'] = InvestmentCapital.objects.get(project=self.kwargs['pk'])
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
        lu = form.save(commit=False)
        lu.project = InvestmentProject.objects.get(id=self.kwargs['project'])
        lu.save()
        return redirect("admin:update_project",pk=self.kwargs['project'])


@method_decorator(decorators,name='dispatch')
class UpdateLandUsage(LoginRequiredMixin,UpdateView):
    model=LandUsage
    form_class = LandUsageForm

    def form_valid(self,form):
        form.save()
        return redirect("admin:update_project",pk=LandUsage.objects.get(id=self.kwargs['pk']).project.id)

@method_decorator(decorators,name='dispatch')
class CreateProductQty(LoginRequiredMixin,CreateView):
    model=ProjectProductQuantity
    form_class = ProjectProductForm

    def form_valid(self,form):
        pp = form.save(commit=False)
        pp.project = InvestmentProject.objects.get(id=self.kwargs['project'])
        pp.save()
        return redirect("admin:update_project",pk=self.kwargs['project'])

@method_decorator(decorators,name='dispatch')
class UpdateProductQty(LoginRequiredMixin,UpdateView):
    model=ProjectProductQuantity
    form_class = ProjectProductForm

    def form_valid(self,form):
        form.save()
        return redirect("admin:update_project",pk=ProjectProductQuantity.objects.get(id=self.kwargs['pk']).project.id)


@method_decorator(decorators,name='dispatch')
class CreateProjectState(LoginRequiredMixin,CreateView):
    model=ProjectState
    form_class = ProjectStatusForm

    def form_valid(self,form):
        ps = form.save(commit=False)
        ps.project = InvestmentProject.objects.get(id=self.kwargs['project'])
        ps.save()
        return redirect("admin:update_project",pk=self.kwargs['project'])

@method_decorator(decorators,name='dispatch')
class UpdateProjectState(LoginRequiredMixin,UpdateView):
    model=ProjectState
    form_class = ProjectStatusForm


    def form_valid(self,form):
        form.save()
        return redirect("admin:update_project",pk=ProjectState.objects.get(id=self.kwargs['pk']).project.id)

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_project")


@method_decorator(decorators,name='dispatch')
class CreateInvestmentCapitalForProject(LoginRequiredMixin,CreateView):
    model = InvestmentCapital
    form_class = InvestmentCapitalForm
    

    def form_valid(self,form):
        try:
            project_invcap = form.save(commit=False)
            project_invcap.project = InvestmentProject.objects.get(id=self.kwargs['project'])
            project_invcap.save()
            messages.success(self.request,"Investment Capital Added")
            return redirect("admin:update_project",pk=self.kwargs['project'])
        except InvestmentProject.DoesNotExist:
            return redirect("admin:error_404")
            
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_project",pk=self.kwargs['project'])

@method_decorator(decorators,name='dispatch')
class UpdateInvestmentCapitalForProject(LoginRequiredMixin,UpdateView):
    model = InvestmentCapital
    form_class = InvestmentCapitalForm

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Investment Capital Data Updated")
        return redirect("admin:update_project",pk=InvestmentCapital.objects.get(id=self.kwargs['pk']).project.id)

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_project",pk=InvestmentCapital.objects.get(id=self.kwargs['pk']).project.id)

@method_decorator(decorators,name='dispatch')
class CreateLandAcqsn(LoginRequiredMixin,CreateView):
    model=LandAquisition
    form_class = LandAquisitionForm

    def form_valid(self,form):
        la = form.save(commit=False)
        la.project = InvestmentProject.objects.get(id=self.kwargs['project'])
        la.save()
        messages.success(self.request,"Land Acquisition data added")
        return redirect("admin:update_project",pk=self.kwargs['project'])

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_project",pk=self.kwargs['project'])

@method_decorator(decorators,name='dispatch')
class UpdateLandAcqsn(LoginRequiredMixin,UpdateView):
    model=LandAquisition
    form_class = LandAquisitionForm

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Land Acquisition Data Updated")
        return redirect("admin:update_project",pk=LandAquisition.objects.get(id=self.kwargs['pk']).project.id)
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:update_project",pk=LandAquisition.objects.get(id=self.kwargs['pk']).project.id)