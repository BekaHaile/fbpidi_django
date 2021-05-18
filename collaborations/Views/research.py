#python,django,library,our pakages
from django.urls import reverse
from django.views import View
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
									 #redirect with context
from django.http import HttpResponse, HttpResponseRedirect, FileResponse

from django.contrib import messages

from company.models import Company

from accounts.models import User, CompanyAdmin, Company
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from accounts.email_messages import sendEventNotification
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.contrib.sites.shortcuts import get_current_site

from collaborations.forms import (ResearchForm,ResearchProjectCategoryForm)
from collaborations.models import Research,ResearchAttachment,ResearchProjectCategory
from collaborations.views import SearchByTitle_All, filter_by, FilterByCompanyname, get_paginated_data

from admin_site.decorators import company_created,company_is_active
from django.utils import timezone

decorators = [never_cache, company_created(),company_is_active()]

@method_decorator(decorators,name='dispatch')
class CreateResearchCategory(LoginRequiredMixin, CreateView):
	model = ResearchProjectCategory
	form_class = ResearchProjectCategoryForm
	 
	def form_valid(self,form):
		try:
			research_cat = form.save(commit=False)
			research_cat.created_by = self.request.user
			research_cat.save()
			messages.success(self.request, "Research Category Added Successfully!")
			return redirect("admin:settings")
		except Exception as e:
			print ("@@@ Exception at CreateResearchCategory ",e)
			return redirect("admin:settings")

	def form_invalid(self, form):
		try:
			messages.warning(self.request, form.errors)
			return redirect("admin:settings")
		except Exception as e:
			print ("@@@ Exception at CreateResearchCategory ",e)
			return redirect("admin:index")


@method_decorator(decorators,name='dispatch')
class ResearchCategoryDetail(LoginRequiredMixin,UpdateView):
	model = ResearchProjectCategory
	form_class = ResearchProjectCategoryForm
	template_name = "admin/researchproject/research_project_category_detail.html"
	 
	def form_valid(self,form):
		try:
			research_cat = form.save(commit=False)
			research_cat.last_updated_by = self.request.user
			research_cat.last_updated_date = timezone.now()
			research_cat.save()
			messages.success(self.request, "Research Category Updated Successfully!")
			return redirect("admin:settings")
		except Exception as e:
			print ("@@@ Exception at ResearchCategoryDetail ",e)
			return redirect("admin:settings")

	def form_invalid(self, form):
		try:
			messages.warning(self.request,form.errors)
			return redirect("admin:settings")
		except Exception as e:
			print ("@@@ Exception at ResearchCategoryDetail form invalid",e)
			return redirect("admin:index")

	   

@method_decorator(decorators,name='get')
class ListResearchAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		context ={}
		if self.request.user.is_superuser:
			context['researchs'] = Research.objects.all()
		else:
			context['researchs'] = Research.objects.filter(company = self.request.user.get_company())
		template_name = "admin/researchproject/research_list.html"
		return render(self.request, template_name,context)

@method_decorator(decorators,name='get')
class ListPendingResearchAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		researchs = Research.objects.filter(accepted="PENDING")
		template_name = "admin/researchproject/pending_list.html"
		context = {'researchs':researchs}
		return render(self.request, template_name,context)


@method_decorator(decorators,name='dispatch')
class CreateResearchAdmin(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = ResearchForm
		template_name = "admin/researchproject/research_form.html"
		context = {'forms':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ResearchForm(self.request.POST,self.request.FILES)
		template_name = "admin/researchproject/research_form.html"
		context = {'forms':form}
		if form.is_valid():
			research = Research
			research = form.save(commit=False)
			if self.request.user.is_customer:
				research.accepted = "PENDING"
			else:
				research.accepted = "APPROVED"
			research.created_by = self.request.user
			research.save()
			for file in self.request.FILES.getlist('files'):
				
				researchattachment= ResearchAttachment()
				researchattachment.research = research
				researchattachment.attachement = file
				researchattachment.save()

			messages.success(self.request, "Added New Research Successfully")
			return redirect("admin:research_list")
		messages.warning(self.request, "Error occured while creating Research!")
		return redirect("admin:settings")


@method_decorator(decorators,name='get')
class ResearchApprove(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		try:
			action = self.kwargs['action']
			research = Research.objects.get(id=self.kwargs['id'])
			research.accepted = action
			research.save()
			if action == "APPROVED":
				messages.success(self.request, "Successfully Approved Research! Now it will be visible for everyone!")
			else:#action == 'PENDING
				messages.success(self.request, "Successfully Suspended Research! Now it will be visible only to Superusers!")
			return redirect("admin:research_view",id=research.id)
		except Exception as e:
			print("@@@ Exception at ResearchApprove ",e)
			return redirect ("admin:research_list")



@method_decorator(decorators,name='get')
class ResearchPending(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = Research.objects.get(id=self.kwargs['id'])
		form.accepted = "PENDING"
		form.save()
		messages.success(self.request, "Changed Status to PENDING Successfully")
		return redirect("admin:research_view",id=self.kwargs['id'])

@method_decorator(decorators,name='dispatch')
class ResearchDetailAdmin(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		try:
			form = Research.objects.get(id=self.kwargs['id'])
			template_name = "admin/researchproject/research_detil.html"
			researchcategory=ResearchProjectCategory.objects.all()
			context = {'forms':form,"category":researchcategory}
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@@ Exception at ResearchDetailAdmin ",e)
			return redirect("admin:research_list")
	def post(self,*args,**kwargs):
		try:
			form = ResearchForm(self.request.POST, self.request.FILES)
			template_name = "admin/researchproject/research_detil.html"
			context = {'forms':form}
			if form.is_valid():
				research = Research.objects.get(id=self.kwargs['id'])
				research.title = form.cleaned_data.get('title')
				research.description = form.cleaned_data.get('description')
				research.detail = form.cleaned_data.get('detail')
				research.status = form.cleaned_data.get('status')
				research.category = form.cleaned_data.get('category')
				research.last_updated_by = self.request.user
				research.last_updated_date = timezone.now()
				research.save()
				for file in self.request.FILES.getlist('files'):
					researchattachment= ResearchAttachment()
					researchattachment.research = research
					researchattachment.attachement = file
					researchattachment.save()
				messages.success(self.request, "Edited Research Successfully")
				return redirect("admin:research_list")
			messages.warning(self.request, 'Invalid Form Data!')
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at POST of Research Detail",e )
			return redirect("admin:research_list")


# customer side
class ListResearch(View):
	def get(self,*args,**kwargs):
		result = {}
		if 'by_category' in self.request.GET:
			result = filter_by("category__cateoryname",self.request.GET.getlist('by_category'), Research.objects.all())
		elif 'by_title' in self.request.GET:
			q = Research.objects.filter(Q(title__icontains = self.request.GET['by_title']))
			if q.count()>0:
				result ={ 'query':q, 'message':f"{q.count()} Result found!", 'message_am':f"{q.count()}  ውጤት ተገኝቷል!"}
			else:
				result = {'query':[],'message':"No result found!",'message_am':"ምንም ውጤት አልተገኘም!"}
		else:
			result = {'query':Research.objects.filter(accepted="APPROVED"),'message':"Researchs",'message_am':"ምርምር"}
		
		data = get_paginated_data(self.request, result['query'])
		template_name="frontpages/research/research_list.html"
		return render(self.request, template_name, {'researchs':data, "category":ResearchProjectCategory.objects.all(), 'message':result['message'], 'message_am':result['message_am']})

class SearchResearch(View):
	def get(self,*args,**kwargs):
		return redirect(reverse("research_list"))
	def post(self,*args,**kwargs):
		form = Research.objects.filter(title__contains=self.request.POST['search'])
		if self.request.user.is_anonymous:
			usercreated = Research.objects.filter(created_by=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_list.html"
		
		return render(self.request, template_name,context)

class ResearchCategorySearch(View):
	def get(self,*args,**kwargs):
		form = Research.objects.filter(accepted="APPROVED",category=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(created_by=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_list.html"
		return render(self.request, template_name,context)

class ResearchDetail(View):
	def get(self,*args,**kwargs):
		form = Research.objects.get(id=self.kwargs['id'])
		related = Research.objects.filter(category=form.category).exclude(id=self.kwargs['id'])[:6]
		category = ResearchProjectCategory.objects.all()
		context = {'research':form,"category":category,"related":related,"message":"Research"}
		template_name = "frontpages/research/research_detail.html"
		
		return render(self.request, template_name,context)

class EditResearch(View):
	def get(self,*args,**kwargs):
		form = Research.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(created_by=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_detail_edit.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form =  ResearchForm(self.request.POST,self.request.FILES)
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(created_by=self.request.user,accepted="APPROVED")
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
			research.last_updated_by = self.request.user
			research.last_updated_date = timezone.now()
			if form.cleaned_data.get("attachements"):
				research.attachements = form.cleaned_data.get("attachements")
			research.created_by = self.request.user
			research.save()
			return redirect("research_list")
		return render(self.request, template_name,context)

class CreateResearch(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = ResearchForm
		usercreated = Research.objects.filter(created_by=self.request.user,accepted="APPROVED")
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/research/research_form.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		try:
			form = ResearchForm(self.request.POST,self.request.FILES)
			template_name = "frontpages/research/research_form.html"
			if form.is_valid():
				research = form.save(commit=False)
				if self.request.user.is_customer:
					research.accepted = "PENDING"
				else:
					research.accepted = "APPROVED"
				research.created_by = self.request.user
				research.save()
				for file in self.request.FILES.getlist('files'):
					researchattachment= ResearchAttachment()
					researchattachment.research = research
					researchattachment.attachement = file
					researchattachment.save()
				messages.success(self.request, "Added New Research Successfully")
				return redirect("research_list")

			category = ResearchProjectCategory.objects.all()
			return render(self.request, template_name, {'form':form, "category":category})
		except Exception as e:
			print("@@@ Exception at Creating Research ", e)
			return redirect("research_list")
