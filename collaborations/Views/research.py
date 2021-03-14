
from django.urls import reverse
import datetime
from django.utils import timezone
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
									ResearchAttachment,
									ResearchProjectCategory
									
									)
from collaborations.forms import (ResearchForm,ResearchProjectCategoryForm)

from collaborations.models import ( Research, Project,
									ResearchProjectCategory
									)


class CreateResearchProjectCategoryAdmin(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		template_name = "admin/researchproject/research_project_category_form.html"
		return render(self.request, template_name, {'forms':ResearchProjectCategoryForm})
	def post(self,*args,**kwargs):
		try:
			form = ResearchProjectCategoryForm(self.request.POST)
			if form.is_valid():
				research = form.save(commit=False)
				research.created_by = self.request.user
				research.save()
				messages.success(self.request, "Added New Category Successfully!")
				return redirect("admin:research_project_category_list")
		except Exception as e:
			print ("Exception at Create research project category ", e)
			return redirect("admin:research_project_category_list")
	
class ListResearchProjectCategoryAdmin(LoginRequiredMixin , ListView):
	model = ResearchProjectCategory
	context_object_name = 'researchprojectcategorys'
	template_name = "admin/researchproject/research_project_category_list.html"


class ResearchProjectCategoryDetail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		try:
			form = ResearchProjectCategory.objects.get(id=self.kwargs['id'])
			template_name = "admin/researchproject/research_project_category_detail.html"
			return render(self.request, template_name,  {'forms':form})
		except Exception as e:
			messages.warning(self.request, "Couldn't find the category!")
			return redirect("admin:research_project_category_list")
	def post(self,*args,**kwargs):
		try:
			rp_category = ResearchProjectCategory.objects.get(id=self.kwargs['id'])
			form = ResearchProjectCategoryForm(self.request.POST)
			if form.is_valid():
				rp_category.cateoryname=form.cleaned_data.get('cateoryname')
				rp_category.cateoryname_am=form.cleaned_data.get('cateoryname_am')
				rp_category.detail=form.cleaned_data.get('detail')
				rp_category.last_updated_by = self.request.user 
				rp_category.last_updated_date = timezone.now()
				rp_category.save()
				messages.success(self.request, "Edited ResearchProjectCategory Successfully")
				return redirect(f'/admin/researchprojectcategorys-detail/{rp_category.id}/')

			messages.WARNING(self.request, "Couldn't edit category. Invalid input data!")
			return redirect("admin:research_project_category_list")
		except Exception as e:
			print ("Exception at Research Project Categor Detail post", e)
			messages.warning(self.request, "Could not edit category!")
			return redirect("admin:research_project_category_list")


class ListResearchAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = Research.objects.all()
		pending = Research.objects.filter(status="PENDING").count()
		template_name = "admin/researchproject/research_list.html"
		context = {'researchs':form,"pending":pending}
		return render(self.request, template_name,context)


class ListPendingResearchAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = Research.objects.filter(accepted="PENDING")
		template_name = "admin/researchproject/pending_list.html"
		context = {'researchs':form}
		return render(self.request, template_name,context)


class ResearchDetailView(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = Research.objects.get(id=self.kwargs['id'])
		template_name = "admin/researchproject/research_view.html"
		context = {'forms':form}
		return render(self.request, template_name,context)


class CreateResearchAdmin(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = ResearchForm()
		template_name = "admin/researchproject/research_form.html"
		context = {'forms':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		
		form = ResearchForm(self.request.POST,self.request.FILES)
		template_name = "admin/researchproject/research_form.html"
		context = {'forms':form}
		if form.is_valid():
			research = Research()
			research = form.save(commit=False)
			if self.request.user.is_customer:
				research.accepted = "PENDING"
			else:
				research.accepted = "APPROVED"
			research.user = self.request.user
			research.save()
			for file in self.request.FILES.getlist('files'):
				print("file name:"+str(file.name))
				researchattachment= ResearchAttachment()
				researchattachment.research = research
				researchattachment.attachement = file
				researchattachment.save()


			researchattachment.attachement
			messages.success(self.request, "Added New Research Successfully")
			return redirect("admin:research_form")
		return render(self.request, template_name,context)


class ResearchApprove(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = Research.objects.get(id=self.kwargs['id'])
		form.accepted = "APPROVED"
		form.save()
		messages.success(self.request, "Changed Status to APPROVED Successfully")
		return redirect("admin:pedning_project_list")

class ResearchDetailAdmin(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = Research.objects.get(id=self.kwargs['id'])
		template_name = "admin/researchproject/research_detil.html"
		researchcategory=ResearchProjectCategory.objects.all()
		context = {'forms':form,"category":researchcategory}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ResearchForm(self.request.POST)
		template_name = "admin/researchproject/research_detil.html"
		context = {'forms':form}
		if form.is_valid():
			research = Research.objects.get(id=self.kwargs['id'])
			research.title = form.cleaned_data.get('title')
			research.description = form.cleaned_data.get('description')
			research.detail = form.cleaned_data.get('detail')
			research.status = form.cleaned_data.get('status')
			research.category = form.cleaned_data.get('category')
			research.save()
			for file in self.request.FILES.getlist('files'):
				print("file name:"+str(file.name))
				researchattachment= ResearchAttachment()
				researchattachment.research = research
				researchattachment.attachement = file
				researchattachment.save()
			messages.success(self.request, "Edited Research Successfully")
			return redirect("admin:research_list")
		print("Not Really")
		return render(self.request, template_name,context)

class SearchResearch(View):
	def get(self,*args,**kwargs):
		return redirect(reverse("research_list"))
	def post(self,*args,**kwargs):
		print("============")
		print(self.request.POST["search"])

		form = Research.objects.filter(title__contains=self.request.POST['search'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_list.html"
		# if str(self.request.user) != "AnonymousUser":
		# 	userCreated = ForumQuestion.objects.filter(user=self.request.user)
		# else:
		# 	userCreated = ""
		return render(self.request, template_name,context)

class ListResearch(View):
	def get(self,*args,**kwargs):
		form = Research.objects.filter(accepted="APPROVED")
		category = ResearchProjectCategory.objects.all()
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_list.html"
		
		return render(self.request, template_name,context)
class ResearchCategorySearch(View):
	def get(self,*args,**kwargs):
		form = Research.objects.filter(accepted="APPROVED",category=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_list.html"
		return render(self.request, template_name,context)

class ResearchDetail(View):
	def get(self,*args,**kwargs):
		form = Research.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'research':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_detail.html"
		
		return render(self.request, template_name,context)

class EditResearch(View):

	def get(self,*args,**kwargs):
		form = Research.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_detail_edit.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form =  ResearchForm(self.request.POST,self.request.FILES)
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_detail_edit.html"
		context = {'form':form,"usercreated":usercreated,"category":category}
		if form.is_valid():
			research = Research.objects.get(id=self.kwargs['id'])
			research.title = form.cleaned_data.get('title')
			research.description = form.cleaned_data.get('description')
			research.detail = form.cleaned_data.get('detail')
			research.status = form.cleaned_data.get('status')
			research.category = form.cleaned_data.get('category')
			if form.cleaned_data.get("attachements"):
				research.attachements = form.cleaned_data.get("attachements")
			research.user = self.request.user
			research.save()
			return redirect("research_list")
		return render(self.request, template_name,context)

class CreateResearch(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = ResearchForm()
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated  = ""
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_form.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ResearchForm(self.request.POST,self.request.FILES)
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_form.html"
		context = {'form':form}
		if form.is_valid():
			research = Research()
			research = form.save(commit=False)
			if self.request.user.is_customer:
				research.accepted = "PENDING"
			else:
				research.accepted = "APPROVED"
			research.user=self.request.user
			#print("-----"+str(self.request.POST['attachements']))
			if form.cleaned_data.get("attachements"):
				research.attachements = form.cleaned_data.get("attachements")

			research.save()
			return redirect("research_form")
		return render(self.request, template_name,context)
from company.forms import EventParticipantForm


