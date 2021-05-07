
from django.utils import timezone

from django.shortcuts import render,redirect
from django.views.generic import (View,CreateView,ListView,UpdateView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from PIL import Image

from admin_site.models import *
from admin_site.forms import *
from product.models import Dose,DosageForm
from product.forms import DoseForm,DosageFormForm
from collaborations.models import JobCategory,ResearchProjectCategory
from collaborations.forms import JobCategoryForm,ResearchProjectCategoryForm
from admin_site.decorators import company_created,company_is_active

decorators = [never_cache, company_created(),company_is_active()]

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

@method_decorator(decorators,name='dispatch')
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
        context['phpg_form'] = PharmaceuticalProductForm()
        context['phpg_list'] = PharmaceuticalProduct.objects.all()
        context['terapeutic_form'] = TherapeuticGroupForm()
        context['terapeutic_list'] = TherapeuticGroup.objects.all()
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


class CreatePhpgMaster(LoginRequiredMixin,CreateView):
    model = PharmaceuticalProduct
    form_class = PharmaceuticalProductForm

    def form_valid(self,form):
        phpg = form.save(commit=False)
        phpg.created_by = self.request.user
        phpg.save()
        messages.success(self.request,"Product Group Added Successfully")
        return redirect("admin:settings")
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:create_phpg")

class UpdatePhpgMaster(LoginRequiredMixin,UpdateView):
    model = PharmaceuticalProduct
    form_class = PharmaceuticalProductForm
    template_name = "admin/accounts/check_list_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "phpg"
        context['title'] = "Settings"
        return context

    def form_valid(self,form):
        phpg = form.save(commit=False)
        phpg.last_updated_by = self.request.user
        phpg.save()
        messages.success(self.request,"Product Group Updated Successfully")
        return redirect("admin:settings")
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_phpg",pk=self.kwargs['pk'])


class CreateTherapeuticMaster(LoginRequiredMixin,CreateView):
    model = TherapeuticGroup
    form_class = TherapeuticGroupForm

    def form_valid(self,form):
        tg = form.save(commit=False)
        tg.created_by = self.request.user
        tg.save()
        messages.success(self.request,"Therapeutic Group Added Successfully")
        return redirect("admin:settings")
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:create_therapeutic_grp")

class UpdateTherapeuticMaster(LoginRequiredMixin,UpdateView):
    model = TherapeuticGroup
    form_class = TherapeuticGroupForm
    template_name = "admin/accounts/check_list_update.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag'] = "tg"
        context['title'] = "Settings"
        return context

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Therapeutic Group Updated Successfully")
        return redirect("admin:settings")
    
    def form_invalid(self,form):
        messages.success(self.request,form.errors)
        return redirect("admin:update_therapeutic_grp",pk=self.kwargs['pk'])



def image_cropper(x,y,w,h,raw_image,size_x,size_y):
    if (x == '' or x == None or y == '' or y == None or w == '' or w == None or h == '' or h == None):
        image = Image.open(raw_image)
        resized_image = image.resize((size_x, size_y), Image.ANTIALIAS)
        resized_image.save(raw_image.path)
        return True
    else:
        x = float(x)
        y = float(y)
        w = float(w)
        h = float(h)
        image = Image.open(raw_image)
        cropped_image = image.crop((x, y, w+x, h+y))
        cropped_image.save(raw_image.path)
        return True