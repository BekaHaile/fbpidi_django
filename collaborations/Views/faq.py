
from django.urls import reverse
import datetime
from django.views import View

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

from django.http import FileResponse, HttpResponse

from accounts.models import User
from accounts.email_messages import sendEventNotification

from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm, NewsForm
from django.http import HttpResponse, FileResponse
						 
from wsgiref.util import FileWrapper



from collaborations.forms import BlogsForm,BlogsEdit, BlogCommentForm, FaqsForm, VacancyForm,JobCategoryForm, TenderApplicantForm

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from collaborations.forms import (BlogsForm, BlogCommentForm, FaqsForm,
								 VacancyForm,JobCategoryForm,
								 ForumQuestionForm,CommentForm,CommentReplayForm,
								 AnnouncementForm,ResearchForm,
								 ResearchProjectCategoryForm
								 )

from collaborations.models import ( Blog, BlogComment,Faqs,
									Vacancy,JobApplication, JobCategory,
									ForumQuestion, ForumComments, CommentReplay,
									Announcement,AnnouncementImages,
									Research,
									ResearchProjectCategory
									
									)
from collaborations.forms import (FaqsForm,)

from collaborations.models import ( Faqs, )


class FaqList(View):
	def get(self,*args,**kwargs):
		template_name="frontpages/faq.html"
		faq = Faqs.objects.filter(status="APPROVED")
		context = {'faqs':faq}
		return render(self.request, template_name,context)

class CreateFaqs(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = FaqsForm()
		context = {'form':form}
		return render(self.request,"admin/pages/faqs_forms.html",context)

	def post(self,*args,**kwargs):
		form = FaqsForm(self.request.POST)
		context = {"form":form}
		if form.is_valid():
			faqs = form.save(commit=False)
			if self.request.user.is_company_admin:
				faqs.status = "PENDDING"
			if self.request.user.is_superuser:
				faqs.status = "APPROVED"
			faqs.user = self.request.user
			faqs.save()
			form = FaqsForm()
			context = {'form':form}
			messages.success(self.request, "New Faqs Added Successfully")
			return redirect("admin:admin_Faqs")
		return render(self.request, "admin/pages/faqs_forms.html",context)

class FaqsView(LoginRequiredMixin,View):
	template_name="admin/pages/blog_list.html"
	def get(self,*args,**kwargs):
		faqs=Faqs.objects.get(id=self.kwargs['id'])
		template_name="admin/pages/faqs_detail.html"
		context={'faq':faqs}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = FaqsForm(self.request.POST)
		if form.is_valid():
			faq = Faqs.objects.get(id=self.kwargs['id'])
			faq.questions = self.request.POST['questions']
			faq.questions_am = self.request.POST['questions_am']
			faq.answers = self.request.POST['answers']
			faq.answers_am = self.request.POST['answers_am']
			faq.save()
		messages.success(self.request, "Edited Faqs Successfully")
		return redirect("admin:admin_Faqs") 

class FaqsList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		if self.request.user.is_superuser:
			faqs=Faqs.objects.all()
			pending = Faqs.objects.filter(status="PENDDING").count()
			
		if self.request.user.is_company_admin:
			faqs=Faqs.objects.filter(user=self.request.user)
			pending = ""
		context = {'faqs':faqs,'pending':pending}
		template_name = "admin/pages/faqs_list.html"
		return render(self.request, template_name,context)

class FaqPendingList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		faqs=Faqs.objects.filter(status="PENDDING")
		pending = Faqs.objects.filter(status="PENDDING").count()
		context = {'faqs':faqs,'pending':pending}
		template_name = "admin/pages/faqs_list.html"
		return render(self.request, template_name,context) 

class FaqApprovdList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		faqs=Faqs.objects.filter(status="APPROVED")
		pending = Faqs.objects.filter(status="PENDDING").count()
		context = {'faqs':faqs,'pending':pending}
		template_name = "admin/pages/faqs_list.html"
		return render(self.request, template_name,context)

class FaqApprove(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		faq = Faqs.objects.get(id=self.kwargs['id'])
		faq.status = "APPROVED"
		faq.save()
		messages.success(self.request, "Changed Status to APPROVED Successfully")
		return redirect("admin:admin_Faqs")
class FaqsDetail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		faq = Faqs.objects.get(id=self.kwargs['id'])
		context = {'forms':faq}
		template_name = "admin/pages/faqs_view.html"
		return render(self.request, template_name,context)