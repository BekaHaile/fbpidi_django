import os
import datetime
from django.utils import timezone
from django.views import View 
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User						 
from collaborations.models import Announcement,AnnouncementImages
from collaborations.forms import AnnouncementForm
from admin_site.decorators import company_created,company_is_active
from collaborations.views import SearchByTitle_All, filter_by, FilterByCompanyname, get_paginated_data
from company.models import Company

decorators = [never_cache, company_created(),company_is_active()]


### customer side 
class AnnouncementDetail(View):
	def get(self,*args,**kwargs):
		announcement = Announcement.objects.get(id=self.kwargs['id'])
		template_name="frontpages/announcement/customer_announcement_detail.html"
		return render(self.request, template_name,{'post':announcement})
	

class ListAnnouncement(View):
	def get(self,*args,**kwargs):
			result = {}
			if 'by_company' in self.request.GET:
				result = FilterByCompanyname(self.request.GET.getlist('by_company'), Announcement.objects.all())
			else:
				result = SearchByTitle_All('Announcement', self.request)
			if result['query']  :
				result['query'] = Announcement.objects.all()
			data = get_paginated_data(self.request, result['query'])
			companies = []
			for comp in Company.objects.all():
				if comp.announcement_set.count() > 0:
					companies.append(comp)
			template_name="frontpages/announcement/customer_announcement.html"
			return render(self.request, template_name, {'Announcements':data, 'message':result['message'],'message_am':result['message_am'], 'companies': companies})
		
		

#### Announcement related with admin side
@method_decorator(decorators,name='dispatch')
class CreatAnnouncementAdmin(LoginRequiredMixin,View): 
	def get(self,*args,**kwargs):
		template_name="admin/announcement/announcement_form.html"
		return render(self.request, template_name,{'form': AnnouncementForm})
	def post(self,*args,**kwargs):
		form = AnnouncementForm(self.request.POST,self.request.FILES) 
		try:
			if form.is_valid():
				announcement = form.save(commit=False)
				announcement.created_by = self.request.user  
				announcement.save()
				for image in self.request.FILES.getlist('images'):
					announcementimage= AnnouncementImages( announcement=announcement, image = image )
					announcementimage.save()
				messages.success(self.request, "Added New Announcement Successfully")
				return redirect("admin:anounce_list")
			messages.warning(self.request, "Couldn't create announcement! Form contains invalid inputs!")
			return redirect("admin:anounce_list")
		except Exception as e:
			print("Exception at create announcement ",e)
			return redirect("admin:anounce_list")


@method_decorator(decorators,name='dispatch')
class ListAnnouncementAdmin(LoginRequiredMixin, ListView):
	model = Announcement
	template_name = "admin/announcement/announcement_list.html"
	context_object_name = "Announcements"
	def get_queryset(self):
			if self.request.user.is_superuser:
				return Announcement.objects.all()
			else:
				return Announcement.objects.filter(company=self.request.user.get_company()) 


@method_decorator(decorators,name='dispatch')	
class AnnouncementDetailAdmin(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		try:
			announcement = Announcement.objects.get(id=self.kwargs['id'])
			template_name="admin/announcement/announcement_detail.html"
			return render(self.request, template_name, {'announcement':announcement})
		except Exception as e:
			print("Exception at Announcement Detail ",e)
			return redirect("admin:anounce_list")

	def post(self,*agrs,**kwargs):
		try:
			announcement = AnnouncementForm(self.request.POST)
			announcementpost = Announcement.objects.get(id=self.kwargs['id'])
			if announcement.is_valid():
				announcementpost.title = announcement.cleaned_data.get('title')
				announcementpost.title_am = announcement.cleaned_data.get('title_am')
				announcementpost.description = announcement.cleaned_data.get('description')
				announcementpost.description_am = announcement.cleaned_data.get('description_am')
				announcementpost.last_updated_by = self.request.user
				announcementpost.last_updated_date = timezone.now()
				announcementpost.save()
				if 'images' in self.request.FILES:
					for image in self.request.FILES.getlist('images'):
						announcementimage= AnnouncementImages( announcement=announcementpost, image= image)
						announcementimage.save()
				messages.success(self.request, "Edited Announcement Successfully")
				return redirect(f"/admin/anounce-Detail/{announcementpost.id}/")
			messages.warning(self.request, "Could not edit announcement, invalid form!")
			return redirect('admin:anounce_list')
		except Exception as e:
			print("Exception at announcement detail post ",e)
			messages.warning(self.request, "Couldn't Edit announcement!")
			return redirect('admin:anounce_list')



