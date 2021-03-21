#python,django,library,our pakages
from django.urls import reverse
from django.views import View
from django.db.models import Q
from django.shortcuts import render, redirect, reverse

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

from django.contrib.sites.shortcuts import get_current_site
from collaborations.forms import (ResearchForm,ResearchProjectCategoryForm)
from collaborations.views import SearchByTitle_All, filter_by, FilterByCompanyname

from collaborations.models import Research,ResearchAttachment,ResearchProjectCategory
from django.utils import timezone


class CreateResearchCategory(LoginRequiredMixin, CreateView):
	model = ResearchProjectCategory
	form_class = ResearchProjectCategoryForm
	 
	def form_valid(self,form):
		research_cat = form.save(commit=False)
		research_cat.created_by = self.request.user
		research_cat.save()
		messages.success(self.request, "Research Category Added Successfully!")
		return redirect("admin:settings")

	def form_invalid():
		messages.warning(self.request,form.errors)
		return redirect("admin:settings")


class ResearchCategoryDetail(LoginRequiredMixin,UpdateView):
	model = ResearchProjectCategory
	form_class = ResearchProjectCategoryForm
	template_name = "admin/researchproject/research_project_category_detail.html"
	 
	def form_valid(self,form):
		research_cat = form.save(commit=False)
		research_cat.last_updated_by = self.request.user
		research_cat.last_updated_date = timezone.now()
		research_cat.save()
		messages.success(self.request, "Research Category Updated Successfully!")
		return redirect("admin:settings")

	def form_invalid():
		messages.warning(self.request,form.errors)
		return redirect("admin:settings")
	   


class ListResearchAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = Research.objects.all()
		pending = Research.objects.filter(status="PENDING").count()
		template_name = "admin/researchproject/research_list.html"
		context = {"researchs":form,"pending":pending}
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

class ListResearch(View):
	def get(self,*args,**kwargs):
		result = {}
		if 'by_category' in self.request.GET:
			result = filter_by("category__cateoryname",self.request.GET.getlist('by_category'), Research.objects.all())
		elif 'by_title' in self.request.GET:
			q = Research.objects.filter(Q(title__icontains = self.request.GET['by_title']))
			print(q)
			if q.count()>0:
				result ={ 'query':q, 'message':f"{q.count()} Result found!"}
			else:
				result = {'query':Research.objects.all(),'message':"No result found!",'message_am':"ምንም ውጤት አልተገኘም!"}
		else:
			result = {'query':Research.objects.filter(accepted="APPROVED"),'message':"Researchs",'message_am':"ምርምር"}
		
		print(self.request.path)
		template_name="frontpages/research/research_list.html"
		return render(self.request, template_name, {'researchs':result['query'],"category":ResearchProjectCategory.objects.all(), 'message':result['message'], 'message_am':result['message_am']})

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

# class ListResearch(View):
# 	def get(self,*args,**kwargs):
# 		form = Research.objects.filter(accepted="APPROVED")
# 		category = ResearchProjectCategory.objects.all()
# 		if str(self.request.user) != "AnonymousUser":
# 			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
# 		else:
# 			usercreated = ""
# 		context = {'researchs':form,"usercreated":usercreated,"category":category}
# 		template_name = "frontpages/research/research_list.html"
		
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
		related = Research.objects.filter(category=form.category)
		category = ResearchProjectCategory.objects.all()
		context = {'research':form,"category":category,"related":related,"message":"Research"}
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

class CreateResearch(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = ResearchForm()
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated  = ""
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":ResearchProjectCategory.objects.all()}
		template_name = "frontpages/research/research_form.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		
		form = ResearchForm(self.request.POST,self.request.FILES)
		if str(self.request.user) != "AnonymousUser":
			usercreated = Research.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			redirect("research_list")
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

 
			messages.success(self.request, "Added New Research Successfully")
			return redirect("research_form")
		return render(self.request, template_name,context)
