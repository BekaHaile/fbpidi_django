
import datetime

from django.urls import reverse
from django.utils import timezone


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
from django.utils import timezone

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
from django.db.models import Q


from collaborations.forms import BlogsForm,BlogsEdit, BlogCommentForm, FaqsForm, VacancyForm,JobCategoryForm, TenderApplicantForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.core.mail import EmailMessage
from collaborations.forms import (BlogsForm, BlogCommentForm, FaqsForm,
								 VacancyForm,JobCategoryForm,
								 ForumQuestionForm,CommentForm,CommentReplayForm,
								 AnnouncementForm,ResearchForm,
								 ResearchProjectCategoryForm
								 )
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from collaborations.models import ( Blog, BlogComment,Faqs,
									Vacancy,JobApplication, JobCategory,
									ForumQuestion, ForumComments, CommentReplay,
									Announcement,AnnouncementImages,
									Research,
									ResearchProjectCategory
									
									)
from collaborations.forms import (JobCategoryForm, VacancyForm, CreateJobApplicationForm)
from admin_site.decorators import company_created,company_is_active
from collaborations.models import ( Vacancy,JobApplication,JobCategory )
from collaborations.views import filter_by, SearchCategory_Title, get_paginated_data, FilterByCompanyname,SearchByTitle_All, models, search_title_related


decorators = [never_cache, company_created(),company_is_active()]

class Download(LoginRequiredMixin,View):
	def get(self, *args, **kwargs):
		obj = JobApplication.objects.get(id=self.kwargs['id'])
		if self.kwargs['name']=='cv':
			filename = obj.cv.path
		if self.kwargs['name']=='documents':
			filename = obj.documents.path
		if os.path.exists(filename):
			response = FileResponse(open(filename, 'rb'))
		else:
			message.error(self.request, "File does not exists")
			return redirect("admin:Applicant_info")
		return response

@method_decorator(decorators,name='dispatch')
class CloseVacancy(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		vacancy=Vacancy.objects.get(id=self.kwargs['id'])
		status = self.kwargs['closed']
		if status== "True":
			vacancy.closed = False
			vacancy.last_updated_by = self.request.user
			vacancy.last_updated_date = timezone.now()
			messages.success(self.request, "Vacancy Opened Successfully")
			vacancy.save()
			if self.request.user.is_superuser:
				return redirect("admin:super_Job_list")
		else:
			vacancy.closed = True
			vacancy.last_updated_by = self.request.user
			vacancy.last_updated_date = timezone.now()
			messages.success(self.request, "Vacancy Closed Successfully")
			vacancy.save()
			if self.request.user.is_superuser:
				return redirect("admin:super_Job_list")
		
		return redirect("admin:Job_list")

@method_decorator(decorators,name='get')
class ApplicantList(LoginRequiredMixin,View):	
	def get(self,*args,**kwargs):
		try:
			vacancy=Vacancy.objects.filter(company= self.request.user.get_company())
			context = {'vacancy':vacancy}
			template_name = "admin/vacancy/vacancy_list.html"
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@@@@@@@ Exception at ApplicantList ",e)
			return redirect("")
	

@method_decorator(decorators,name='get')
class Applicantinfo(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		jobapplicant=JobApplication.objects.filter(vacancy=self.kwargs['id']) 
		vacancyDetail = Vacancy.objects.get(id=self.kwargs['id'])
		context = {'jobapplicant':jobapplicant,'vacancy':self.kwargs['id'],'vacancyDetail':vacancyDetail}
		template_name = "admin/vacancy/applicant_list.html"
		return render(self.request, template_name,context)

@method_decorator(decorators,name='get')
class ApplicantListDetail(LoginRequiredMixin,View):	
	def get(self,*args,**kwargs):
		applicant=JobApplication.objects.get(id=self.kwargs['id'])
		context = {'applicant':applicant}
		template_name = "admin/vacancy/applicant_detail.html"
		return render(self.request, template_name,context)


@method_decorator(decorators,name='dispatch')
class CreateVacancyCategory(LoginRequiredMixin,CreateView):
	model = JobCategory
	form_class = JobCategoryForm
	
	def form_valid(self,form):
		catagory = form.save(commit=False)
		catagory.created_by = self.request.user
		catagory.save()
		messages.success(self.request, "Vacancy category Added Successfully")
		return redirect("admin:settings")

	def form_invalid(self,form):
		messages.warning(self.request,form.errors)
		return redirect("admin:settings")

@method_decorator(decorators,name='dispatch')
class JobCategoryDetail(LoginRequiredMixin,UpdateView):
	model = JobCategory
	form_class = JobCategoryForm
	template_name = "admin/vacancy/jobCategory_detail.html"

	def form_valid(self,form):
		form.save()
		messages.success(self.request, "Vacancy category Updated Successfully")
		return redirect("admin:settings")

	def form_invalid(self,form):
		messages.warning(self.request,form.errors)
		return redirect("admin:settings")
	
@method_decorator(decorators,name='dispatch')
class VacancyDetail(LoginRequiredMixin,View):
	def company_admin(self,*args,**kwarges):
		force = Company.objects.get(created_by=self.request.user)
		return force
	def get(self,*args,**kwargs):
		form = Vacancy.objects.get(id=self.kwargs['id'])
		jobcategory = JobCategory.objects.all()
		start=str(form.starting_date)
		start=start[:19]
		end=str(form.ending_date)
		end=end[:19]
		form.starting_date = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
		form.ending_date =  datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
		vacancy = VacancyForm() 
		context = {'form':form,'jobcategory':jobcategory,"vacancy":vacancy}
		return render(self.request,"admin/vacancy/job_detail.html",context)
	def post(self,*args,**kwarges):
		try:
			form = VacancyForm(self.request.POST,self.request.FILES)
			context = {'form':form}
			if form.is_valid():
				vacancy = Vacancy.objects.get(id=self.kwargs['id'])
				vacancy.last_updated_by=self.request.user
				vacancy.company=self.request.user.get_company()
				vacancy.last_updated_date = timezone.now()
				vacancy.location=form.cleaned_data.get('location')
				vacancy.salary=form.cleaned_data.get('salary')
				vacancy.title=form.cleaned_data.get('title')
				vacancy.description=form.cleaned_data.get('description')
				vacancy.requirement=form.cleaned_data.get('requirement')
				vacancy.title_am=form.cleaned_data.get('title_am')
				vacancy.description_am=form.cleaned_data.get('description_am')
				vacancy.requirement_am=form.cleaned_data.get('requirement_am')
				starting_date=datetime.datetime.strptime(self.request.POST['starting_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
				ending_date=datetime.datetime.strptime(self.request.POST['ending_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
				vacancy.starting_date = starting_date
				vacancy.ending_date = ending_date
				vacancy.category=form.cleaned_data.get('category')
				vacancy.employement_type=form.cleaned_data.get('employement_type')
				vacancy.save()
				messages.success(self.request, "Vacancy Edited Successfully")
				return redirect("admin:Job_list")
			return render(self.request,"admin/vacancy/job_detail.html",context)
		except Exception as e:
			return redirect('admin:Job_list')

@method_decorator(decorators,name='get')
class AdminVacancyList(LoginRequiredMixin,ListView):
	model = Vacancy
	template_name= "admin/vacancy/job_list.html"
	def get_queryset(self):
		try:
			return  Vacancy.objects.all() if self.request.user.is_superuser else  Vacancy.objects.filter(company=self.request.user.get_company())
		except:
			return []

## show form
@method_decorator(decorators,name='dispatch')
class CreateVacancy(LoginRequiredMixin, View):

	def company_admin(self,*args,**kwarges):
		force = Company.objects.get(created_by=self.request.user)
		return force
	
	def get(self,*args,**kwargs):
		vacancy = VacancyForm()
		context = {'vacancy':vacancy}
		template = "admin/vacancy/job_form.html"
		return render(self.request,template,context)
	def post(self,*args,**kwargs):
		form = VacancyForm(self.request.POST,self.request.FILES)
		context = {'vacancy':form}
		template = "admin/vacancy/job_form.html"
		if form.is_valid():
			category = JobCategory.objects.get(id=self.request.POST['category'],)
			vacancy=form.save(commit=False)
			vacancy.employement_type = form.cleaned_data.get('employement_type')
			vacancy.created_by=self.request.user
		
			vacancy.company=self.request.user.get_company()
			vacancy.category=category
			
			starting_date=datetime.datetime.strptime(self.request.POST['starting_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
			ending_date=datetime.datetime.strptime(self.request.POST['ending_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
			vacancy.starting_date = starting_date
			vacancy.ending_date = ending_date
			vacancy.save()
			messages.success(self.request, "New vacancy Added Successfully")
			vacancy = VacancyForm()
			context = {'vacancy':vacancy}
			return redirect("admin:Job_list")
		return render(self.request,template, context)

#apply to a job
class CreateApplication(LoginRequiredMixin,View):

	def get(self,*args,**kwargs):
		try:
			vacancy=Vacancy.objects.get(id=self.kwargs['id'] ,closed=False)
			if JobApplication.objects.filter(vacancy=vacancy, created_by=self.request.user).exists():
				messages.warning(self.request, "You can't apply to the same vacancy Twice")
				return redirect("vacancy")
					
			job = CreateJobApplicationForm()
			jobcategory = JobCategory.objects.all()
			template_name="frontpages/vacancy/job_apply.html"
			context={'job':job,'vacancy':vacancy,'category':jobcategory}
			return render(self.request, template_name,context) 
		except Exception as e:
			print("@@@@@@@@@@@@@ Exception at CreateApplication get  ",e )
			return redirect("vacancy")

	def post(self,*args,**kwargs):
		try:
			form = CreateJobApplicationForm(self.request.POST,self.request.FILES)
			if form.is_valid():
				job=form.save(commit=False)
				job.created_by=self.request.user
				job.vacancy = Vacancy.objects.get(id=self.kwargs['id'])
				job.save()
				return redirect("vacancy")
			else:
				messages.warning(self.request, "Unsupported file type detected, the supported files are pdf, jpg, png, doc and docx! ")
				return redirect("vacancy")
		except Exception as e:
			print("@@@@@@@@@@@@@ Exception at CreateApplication post  ",e )
			return redirect("vacancy")



class CategoryBasedSearch(View):
	def get(self,*args,**kwargs):
		try:
			vacancy = Vacancy.objects.filter(category=self.kwargs['id'],closed=False) 
			cateory = JobCategory.objects.get(id=self.kwargs['id'])
			jobcategory = JobCategory.objects.all()
			template_name="frontpages/vacancy/vacancy_list.html"
			context = {'vacancys':vacancy,'category':jobcategory,'message':'Vacancies on '+str(cateory)}
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@@@@@@@@@@@ Exception at CategoryBasedSearch  ",e )
			return redirect("vacancy")

class VacancyList(View):
	def get(self, *args, **kwargs):
		try:
			result = []
			category = JobCategory.objects.all()
			companies = []
			for comp in Company.objects.all():
				if comp.vacancy_set.count()>0:
					companies.append(comp)
			
			if 'by_category' in self.request.GET and 'by_title' in self.request.GET:
				q= Q( Q(title__icontains = self.request.GET['by_title']) | 
					Q(title_am__icontains = self.request.GET['by_title']) )
				query = Vacancy.objects.filter(q)# search by title then filter by category
				result = filter_by('category__category_name',self.request.GET.getlist('by_category'), query)
				
			elif 'by_category' in self.request.GET:
				result = filter_by('category__category_name', self.request.GET.getlist('by_category'), Vacancy.objects.all())
			elif 'by_company' in self.request.GET:
				result = FilterByCompanyname(self.request.GET.getlist('by_company'), Vacancy.objects.all())
			else: 
				result = SearchByTitle_All('Vacancy', self.request)

			if result['query'].count()==0:
				result['query'] = Vacancy.objects.all()
			
			#what ever the result is, paginate it and send
			data = get_paginated_data(self.request, result['query'])
			return render(self.request, "frontpages/vacancy/vacancy_list.html", {'vacancys':data, 'message':result['message'], 
			 'message_am':result['message_am'], 'category':category, 'companies':companies})
		
		except Exception as e:
			print("@@@@@@@@@@@@@ Exception at Vacancy List ",e )
			return redirect("vacancy")
        		
class VacancyMoreDetail(View):
	def get(self,*args,**kwargs):
		try:
			vac = Vacancy.objects.get(id=self.kwargs['id'])
			jobcategory = JobCategory.objects.all()
			template_name="frontpages/vacancy/vacancy_detail.html"
			context = {'vacancy':vac,'category':jobcategory,'message':'Vacancy Detail'}

			if self.request.user.is_authenticated and JobApplication.objects.filter(vacancy=vac, created_by=self.request.user).exists():
				context['applied'] = True
			return render(self.request, template_name,context)
		except Exception as e:
			print ("@@@@@@@@@@@@Exception at vacancy detail ", e)
			return redirect('vacancy')

