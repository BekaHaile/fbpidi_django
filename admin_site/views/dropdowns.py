
from django.utils import timezone

from django.shortcuts import render,redirect
from django.views.generic import (View,CreateView,ListView,UpdateView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from admin_site.models import CompanyDropdownsMaster,ProjectDropDownsMaster
from admin_site.forms import CompanyDropdownsMasterForm,ProjectDropdownsMasterForm
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

        context['flag'] = "company_dropdown"
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
        return context

    def form_valid(self,form):
        chkmst = form.save(commit=False)
        chkmst.lastupdated_by = self.request.user
        chkmst.lastupdated_date = timezone.now()
        chkmst.save()
        messages.success(self.request,"Dropdown Updated Successfully")
        return redirect("admin:settings") 


