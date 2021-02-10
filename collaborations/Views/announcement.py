
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

from collaborations.forms import (AnnouncementForm,)

from collaborations.models import ( Announcement, )

class AnnouncementDetail(View):
	def get(self,*args,**kwargs):
		announcement = Announcement.objects.get(id=self.kwargs['id'])
		template_name="frontpages/announcement/announcement_detail.html"
		context={'post':announcement}
		return render(self.request, template_name,context)

class ListAnnouncement(View):
	def get(self,*args,**kwargs):
		announcement = Announcement.objects.all()
		template_name="frontpages/announcement/announcement_list.html"
		context={'Announcements':announcement}
		return render(self.request, template_name,context)

class ListAnnouncementAdmin(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		announcement = Announcement.objects.all()
		template_name="admin/announcement/announcement_list.html"
		context={'Announcements':announcement}
		return render(self.request, template_name,context)

class AnnouncementDetailAdmin(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		announcement = Announcement.objects.get(id=self.kwargs['id'])
		template_name="admin/announcement/announcement_detail.html"
		context={'announcement':announcement}
		return render(self.request, template_name,context)
	def post(self,*agrs,**kwargs):
		announcement = AnnouncementForm(self.request.POST)
		announcementpost = Announcement.objects.get(id=self.kwargs['id'])
		context={'announcement':announcement}
		template_name="admin/announcement/announcement_detail.html"
		if announcement.is_valid():
			announcementpost.title = announcement.cleaned_data.get('title')
			announcementpost.title_am = announcement.cleaned_data.get('title_am')
			announcementpost.containt = announcement.cleaned_data.get('containt')
			announcementpost.containt_am = announcement.cleaned_data.get('containt_am')
			announcementpost.save()
			for images in self.request.FILES.getlist('images'):
				print("image name:"+str(images.name))
				announcementimages= AnnouncementImages()
				announcementimages.announcement = post
				announcementimages.image = images
				announcementimages.save()

			messages.success(self.request, "Edited Announcement Successfully")
			return redirect("admin:anounce_list")
		return render(self.request, template_name,context)



class CreatAnnouncementAdmin(LoginRequiredMixin,View): 
	def company_admin(self,*args,**kwarges):
		force = Company.objects.get(user=self.request.user)
		return force
	
	def get(self,*args,**kwargs):
		announcement = AnnouncementForm()
		template_name="admin/announcement/announcement_form.html"
		context={'form':announcement}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		announcement = AnnouncementForm(self.request.POST,self.request.FILES)
		context={'announcement':announcement}
		template_name="admin/announcement/announcement_form.html"
		print("----------")
		if announcement.is_valid():
			post = Announcement()
			post = announcement.save(commit=False)
			post.user = self.request.user  
			post.company = self.company_admin()         
			post.save()
			for images in self.request.FILES.getlist('images'):
				print("image name:"+str(images.name))
				announcementimages= AnnouncementImages()
				announcementimages.announcement = post
				announcementimages.image = images
				announcementimages.save()


			announcementimages.image
			messages.success(self.request, "Added New Announcement Successfully")
			return redirect("admin:anounce_Create")
		return render(self.request, template_name,context)