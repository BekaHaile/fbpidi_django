
from django.utils import timezone

from django.shortcuts import render,redirect
from django.views.generic import (View,CreateView,ListView,UpdateView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from admin_site.models import CompanyDropdownsMaster,ProjectDropDownsMaster,RegionMaster,UomMaster
from admin_site.forms import CompanyDropdownsMasterForm,ProjectDropdownsMasterForm,RegionMasterForm,UomMasterForm
from product.models import Dose,DosageForm
from product.forms import DoseForm,DosageFormForm
from collaborations.models import JobCategory,ResearchProjectCategory
from collaborations.forms import JobCategoryForm,ResearchProjectCategoryForm



class CreateCompanyDropdownsMaster(LoginRequiredMixin,CreateView):
    model = CompanyDropdownsMaster
    form_class = CompanyDropdownsMasterForm
    template_name = ""

    def form_valid(self,form):
        chkmst = form.save(commit=False)
        chkmst.created_by = self.request.user
        chkmst.save()
        messages.success(self.request,"Check List Added Successfully")
        return redirect("admin:settings")

class UpdateCompanyDropdownsMaster(LoginRequiredMixin,UpdateView):
    model = CompanyDropdownsMaster
    form_class = CompanyDropdownsMasterForm
    template_name = "admin/accounts/check_list_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "company_dropdown"
        return context

    def form_valid(self,form):
        chkmst = form.save(commit=False)
        chkmst.lastupdated_by = self.request.user
        chkmst.lastupdated_date = timezone.now()
        chkmst.save()
        messages.success(self.request,"Check List Updated Successfully")
        return redirect("admin:settings") 

class AllSettingsPage(LoginRequiredMixin,ListView):
    model = CompanyDropdownsMaster
    template_name = "admin/accounts/settings_list.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['chkform'] = CompanyDropdownsMasterForm()
        context['projectform'] = ProjectDropdownsMasterForm()
        context['pl_objects'] = ProjectDropDownsMaster.objects.all()
        context['dose_form'] = DoseForm()
        context['doses'] = Dose.objects.all()
        context['dosage_forms'] = DosageForm.objects.all()
        context['dosage_form_form'] = DosageFormForm()
        context['job_category_form'] = JobCategoryForm()
        context['job_categories'] = JobCategory.objects.all()
        context['research_categories'] = ResearchProjectCategory.objects.all()
        context['research_category_form'] = ResearchProjectCategoryForm()
        context['region_form'] = RegionMasterForm()
        context['region_list'] = RegionMaster.objects.all()
        context['uom_form'] = UomMasterForm()
        context['uom_list'] = UomMaster.objects.all()
        context['flag'] = "company_dropdown"
        context['title'] = "Settings"
        return context



class CreateProjectDropdownsMaster(LoginRequiredMixin,CreateView):
    model = ProjectDropDownsMaster
    form_class = ProjectDropdownsMasterForm
    template_name = ""

    def form_valid(self,form):
        chkmst = form.save(commit=False)
        chkmst.created_by = self.request.user
        chkmst.save()
        messages.success(self.request,"Dropdown Added Successfully")
        return redirect("admin:settings")

class UpdateProjectDropdownsMaster(LoginRequiredMixin,UpdateView):
    model = ProjectDropDownsMaster
    form_class = ProjectDropdownsMasterForm
    template_name = "admin/accounts/check_list_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "project_dropdown"
        context['title'] = "Settings"
        return context

    def form_valid(self,form):
        chkmst = form.save(commit=False)
        chkmst.lastupdated_by = self.request.user
        chkmst.lastupdated_date = timezone.now()
        chkmst.save()
        messages.success(self.request,"Dropdown Updated Successfully")
        return redirect("admin:settings") 



class CreateRegionMaster(LoginRequiredMixin,CreateView):
    model = RegionMaster
    form_class = RegionMasterForm

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Region Master Added Successfully")
        return redirect("admin:settings")
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:create_region")

class UpdateRegionMaster(LoginRequiredMixin,UpdateView):
    model = RegionMaster
    form_class = RegionMasterForm
    template_name = "admin/accounts/check_list_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "region_dropdown"
        context['title'] = "Settings"
        return context

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Region Master Updated Successfully")
        return redirect("admin:settings")
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_region",pk=self.kwargs['pk'])


class CreateUomMaster(LoginRequiredMixin,CreateView):
    model = UomMaster
    form_class = UomMasterForm

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Unit of Mesurement Master Added Successfully")
        return redirect("admin:settings")
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:create_uom")

class UpdateUomMaster(LoginRequiredMixin,UpdateView):
    model = UomMaster
    form_class = UomMasterForm
    template_name = "admin/accounts/check_list_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Settings"
        context['flag'] = "uom_dropdown"
        return context

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Unit of Mesurement Updated Successfully")
        return redirect("admin:settings")
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_uom",pk=self.kwargs['pk'])
