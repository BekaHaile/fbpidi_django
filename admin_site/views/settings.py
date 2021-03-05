
from django.utils import timezone

from django.shortcuts import render,redirect
from django.views.generic import (View,CreateView,ListView,UpdateView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from admin_site.models import ChecklistMaster
from admin_site.forms import ChecklistMasterForm

class CreateCheckListMaster(LoginRequiredMixin,CreateView):
    model = ChecklistMaster
    form_class = ChecklistMasterForm
    template_name = ""

    def form_valid(self,form):
        chkmst = form.save(commit=False)
        chkmst.created_by = self.request.user
        chkmst.save()
        messages.success(self.request,"Check List Added Successfully")
        return redirect("admin:settings")

class UpdateCheckListMaster(LoginRequiredMixin,UpdateView):
    model = ChecklistMaster
    form_class = ChecklistMasterForm
    template_name = ""

    def form_valid(self,form):
        chkmst = form.save(commit=False)
        chkmst.lastupdated_by = self.request.user
        chkmst.lastupdated_date = timezone.now()
        chkmst.save()
        messages.success(self.request,"Check List Added Successfully")
        return redirect("admin:settings") 

class CheckListMasterList(LoginRequiredMixin,ListView):
    model = ChecklistMaster
    template_name = "admin/accounts/settings_list.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['chkform'] = ChecklistMasterForm()
        return context
