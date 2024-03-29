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
from collaborations.forms import AnnouncementForm, image_cropper
from admin_site.decorators import company_created,company_is_active
from collaborations.views import SearchByTitle_All, filter_by, FilterByCompanyname, get_paginated_data
from company.models import Company

decorators = [never_cache, company_created(),company_is_active()]


### customer side 
class AnnouncementDetail(View):
	def get(self,*args,**kwargs):
		try:
			announcement = Announcement.objects.get(id=self.kwargs['id'])
			template_name="frontpages/announcement/customer_announcement_detail.html"
			return render(self.request, template_name,{'post':announcement})
		except Exception as e:
			print("@@@ Exception at Announcement Detail ", e)
			return redirect("/")
	

class ListAnnouncement(View):
	def get(self,*args,**kwargs):
			result = {}
			try:
				if 'by_company' in self.request.GET:
					result = FilterByCompanyname(self.request.GET.getlist('by_company'), Announcement.objects.all())
				else:
					result = SearchByTitle_All('Announcement', self.request)
				
				data = get_paginated_data(self.request, result['query'])
				companies = []
				for comp in Company.objects.all():
					if comp.announcement_set.count() > 0:
						companies.append(comp)
				template_name="frontpages/announcement/customer_announcement.html"
				return render(self.request, template_name, {'Announcements':data, 'message':result['message'],'message_am':result['message_am'], 'companies': companies})
			except Exception as e:
				print("@@@ Exception at List Announcement ",e)
				return redirect ("/")
		

#### Announcement related with admin side
@method_decorator(decorators,name='dispatch')
class CreatAnnouncementAdmin(LoginRequiredMixin,View): 
	def get(self,*args,**kwargs):
		template_name="admin/announcement/announcement_form.html"
		return render(self.request, template_name,{'form': AnnouncementForm})
	def post(self,*args,**kwargs):
		try:
			form = AnnouncementForm(self.request.POST,self.request.FILES) 
			if form.is_valid():				
				announcement = form.save(commit=False)
				announcement.created_by = self.request.user
				announcement.company = self.request.user.get_company()
				announcement.save()
				data = self.request.POST
				image_cropper(data['x'], data['y'],data['width'],data['height'], announcement.image)
				messages.success(self.request, "Added New Announcement Successfully")
				return redirect("admin:anounce_list")
			messages.warning(self.request, "Couldn't create announcement!")
			return render(self.request, "admin/announcement/announcement_form.html",{'form': form})
		except Exception as e:
			print("Exception at create announcement ",e)
			messages.warning(self.request, "Couldn't Create Announcement!")
			return redirect("admin:anounce_list")


@method_decorator(decorators,name='dispatch')
class ListAnnouncementAdmin(LoginRequiredMixin, ListView):
	model = Announcement
	template_name = "admin/announcement/announcement_list.html"
	context_object_name = "Announcements"
	def get_queryset(self):
			if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
				return Announcement.objects.all()
			else:
				return Announcement.objects.filter(company=self.request.user.get_company()) 



@method_decorator(decorators,name='dispatch')	
class AnnouncementDetailAdmin(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		try:
			announcement = Announcement.objects.get(id=self.kwargs['id'])
			form = AnnouncementForm(instance=announcement)
			template_name="admin/announcement/announcement_detail.html"
			return render(self.request, template_name, {'announcement':announcement, "form":form})
		except Exception as e:
			print("Exception at Announcement Detail ",e)
			return redirect("admin:anounce_list")

	def post(self,*agrs,**kwargs):
		try:
			announcementpost = Announcement.objects.get(id=self.kwargs['id'])
			form = AnnouncementForm(self.request.POST, self.request.FILES, instance=announcementpost)
			if form.is_valid():
				announcementpost=form.save(commit=False)
				announcementpost.last_updated_by = self.request.user
				announcementpost.last_updated_date = timezone.now()					
				announcementpost.save()
				data = self.request.POST
				image_cropper(data['x'], data['y'],data['width'],data['height'], announcementpost.image)
				messages.success(self.request, "Edited Announcement Successfully")
				return redirect(f"/admin/anounce-Detail/{announcementpost.id}/")
			messages.warning(self.request, "Could not edit announcement, invalid form!")
			return redirect('admin:anounce_list')
		except Exception as e:
			print("Exception at announcement detail post ",e)
			messages.warning(self.request, "Couldn't Edit announcement!")
			return redirect('admin:anounce_list')



