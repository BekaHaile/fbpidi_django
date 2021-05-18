
import datetime

from django.utils import timezone
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, FileResponse
from collaborations.models import Blog, BlogComment
from collaborations.forms import FaqsForm
from django.shortcuts import render, redirect, reverse

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from collaborations.models import Faqs, Vacancy, Blog, BlogComment, Blog, BlogComment, JobApplication, JobCategory, News, NewsImages
									 #redirect with context
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib import messages

from company.models import Company, CompanyBankAccount, Bank, CompanyStaff, CompanyEvent, EventParticipants
from accounts.models import User, CompanyAdmin, Company
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import FileResponse, HttpResponse

from accounts.models import User
from admin_site.decorators import company_created,company_is_active
						 
from collaborations.forms import (FaqsForm,)

from collaborations.models import ( Faqs, )

decorators = [never_cache, company_created(),company_is_active()]
class FaqList(View):
	def get(self,*args,**kwargs):
		template_name="frontpages/faq/faq.html"
		faq = Faqs.objects.filter(status="APPROVED")
		context = {'faqs':faq}
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class CreateFaqs(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = FaqsForm()
		context = {'form':form}
		return render(self.request,"admin/faq/faqs_forms.html",context)

	def post(self,*args,**kwargs):
		form = FaqsForm(self.request.POST)
		context = {"form":form}
		if form.is_valid():
			faqs = form.save(commit=False)
			if self.request.user.is_company_admin:
				faqs.status = "PENDDING"
			if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
				faqs.status = "APPROVED"
			faqs.created_by = self.request.user
			faqs.company = self.request.user.get_company()
			faqs.save()
			form = FaqsForm()
			context = {'form':form}
			messages.success(self.request, "New Faqs Added Successfully")
			return redirect("admin:admin_Faqs")
		return render(self.request, "admin/faq/faqs_forms.html",context)

@method_decorator(decorators,name='dispatch')
class FaqsView(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		faqs=Faqs.objects.get(id=self.kwargs['id'])
		template_name="admin/faq/faqs_detail.html"
		context={'faq':faqs}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = FaqsForm(self.request.POST)
		template_name="admin/faq/faqs_detail.html"
		faq = Faqs.objects.get(id=self.kwargs['id'])
		
		if form.is_valid():
			faq.questions = self.request.POST['questions']
			faq.questions_am = self.request.POST['questions_am']
			faq.answers = self.request.POST['answers']
			faq.answers_am = self.request.POST['answers_am']
			faq.last_updated_date = timezone.now()
			faq.last_updated_by = self.request.user
			faq.save()
			messages.success(self.request, "Edited Faqs Successfully")
			return redirect("admin:admin_Faqs")
		context = {'faq':faq, 'form':form}
		return render(self.request, template_name, context)

@method_decorator(decorators,name='dispatch')
class FaqsList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
			faqs=Faqs.objects.all()
			pending = Faqs.objects.filter(status="PENDDING").count()
			
		if self.request.user.is_company_admin:
			faqs=Faqs.objects.filter(created_by=self.request.user)
			pending = ""
		context = {'faqs':faqs,'pending':pending}
		template_name = "admin/faq/faqs_list.html"
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class FaqPendingList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		faqs=Faqs.objects.filter(status="PENDDING")
		pending = Faqs.objects.filter(status="PENDDING").count()
		context = {'faqs':faqs,'pending':pending}
		template_name = "admin/faq/faqs_list.html"
		return render(self.request, template_name,context) 


@method_decorator(decorators,name='dispatch')
class FaqApprovdList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		faqs=Faqs.objects.filter(status="APPROVED")
		pending = Faqs.objects.filter(status="PENDDING").count()
		context = {'faqs':faqs,'pending':pending}
		template_name = "admin/faq/faqs_list.html"
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class FaqApprove(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		faq = Faqs.objects.get(id=self.kwargs['id'])
		faq.status = "APPROVED"
		faq.save()
		messages.success(self.request, "Changed Status to APPROVED Successfully")
		return redirect("admin:admin_Faqs")

@method_decorator(decorators,name='dispatch')
class FaqPending(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		faq = Faqs.objects.get(id=self.kwargs['id'])
		faq.status = "PENDDING"
		faq.save()
		messages.success(self.request, "Changed Status to PENDDING Successfully")
		return redirect("admin:admin_Faqs")

@method_decorator(decorators,name='dispatch')
class FaqsDetail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		faq = Faqs.objects.get(id=self.kwargs['id'])
		context = {'forms':faq}
		template_name = "admin/faq/faqs_view.html"
		return render(self.request, template_name,context)