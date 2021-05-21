
from django.urls import reverse
import datetime
from django.utils import timezone
from django.views import View

from django.shortcuts import render, redirect, reverse

from django.views.generic import  DetailView, ListView
									
from django.views import View
from django.contrib import messages

import os
from django.contrib.auth.mixins import LoginRequiredMixin


from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


from admin_site.decorators import company_created,company_is_active




from collaborations.models import ( ResearchProjectCategory)
from collaborations.forms import (ProjectForm)

from collaborations.models import (  Project,ResearchProjectCategory)

# ------------ Project Admin side
decorators = [never_cache, company_created(),company_is_active()]
@method_decorator(decorators,name='dispatch')
class ListProjectAdmin(LoginRequiredMixin, ListView):
	model = Project
	template_name = "admin/researchproject/project_list.html"
	context_object_name = 'projects'
	def get_queryset(self):
		if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
			return Project.objects.all()
		else:
			return Project.objects.filter(company=self.request.user.get_company())
	
	# def get(self,*args,**kwargs):
	# 	form = Project.objects.all()
	# 	pending = Project.objects.filter(status="PENDING").count()
	# 	template_name = "admin/researchproject/project_list.html"
	# 	context = {'researchs':form,'pending':pending}
	# 	return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class CreateProjectAdmin(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		template_name = "admin/researchproject/project_form.html"
		return render(self.request, template_name,  {'forms': ProjectForm})
	def post(self,*args,**kwargs):	
		try:	
			form = ProjectForm(self.request.POST,self.request.FILES)
			if form.is_valid():
				project = form.save(commit=False)
				project.created_by = self.request.user
				if form.cleaned_data.get("attachements"):
					project.attachements = form.cleaned_data.get("attachements")
				project.save()
				messages.success(self.request, "Added New Project Successfully")
				return redirect("admin:project_list")
			messages.warning(self.request, "Couldn't create Project. Invalud input data!")
			return redirect("admin:project_list")
		except Exception as e:
			messages.warning(self.request, "Couldn't create Project. Exception occured!")
			return redirect("admin:project_list")

@method_decorator(decorators,name='dispatch')
class ProjectDetailAdmin(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = Project.objects.get(id=self.kwargs['id'])
		template_name = "admin/researchproject/project_detil.html"
		category = ResearchProjectCategory.objects.all()
		context = {'forms':form,"category":category}		
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ProjectForm(self.request.POST,self.request.FILES)
		template_name = "admin/researchproject/project_detil.html"
		if form.is_valid():
			project = Project.objects.get(id=self.kwargs['id'])
			project.title = form.cleaned_data.get('title')
			project.description = form.cleaned_data.get('description')
			project.status = form.cleaned_data.get('status')
			project.category = form.cleaned_data.get('category')
			if form.cleaned_data.get("attachements"):
				project.attachements = form.cleaned_data.get("attachements")
			project.last_updated_by = self.request.user
			project.last_updated_date = timezone.now()
			project.save()
			messages.success(self.request, "Edited Project Successfully")
			return redirect("admin:project_list")
		return render(self.request, template_name,context)


########### Customer side
class ListProject(View):
	def get(self,*args,**kwargs):
		form = Project.objects.filter(accepted="APPROVED")
		category = ResearchProjectCategory.objects.all()
		if str(self.request.user) != "AnonymousUser":
			usercreated = Project.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/project/project_list.html"
		
		return render(self.request, template_name,context)


class ProjectDetailView(LoginRequiredMixin, DetailView):
	model = Project
	context_object_name = 'forms'
	template_name = "admin/researchproject/project_view.html"


	# def get(self,*args,**kwargs):
	# 	form = Project.objects.get(id=self.kwargs['id'])
	# 	template_name = "admin/researchproject/project_view.html"
	# 	context = {'forms':form}
	# 	return render(self.request, template_name,context)


class SearchProject(View):
	def get(self,*args,**kwargs):
		return redirect(reverse("project_list"))
	def post(self,*args,**kwargs):
		print(self.request.POST["search"])

		form = Project.objects.filter(title__contains=self.request.POST['search'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Project.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/project/project_list.html"
		# if str(self.request.user) != "AnonymousUser":
		# 	userCreated = ForumQuestion.objects.filter(user=self.request.user)
		# else:
		# 	userCreated = ""
		return render(self.request, template_name,context)


class ProjectCategorySearch(View):
	def get(self,*args,**kwargs):
		form = Project.objects.filter(accepted="APPROVED",category=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Project.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'researchs':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/project/project_list.html"
		return render(self.request, template_name,context)


class ProjectDetail(View):
	def get(self,*args,**kwargs):
		form = Project.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Project.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'research':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/project/project_detail.html"
		
		return render(self.request, template_name,context)


class EditProject(View):

	def get(self,*args,**kwargs):
		form = Project.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			usercreated = Project.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/project/project_detail_edit.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form =  ProjectForm(self.request.POST,self.request.FILES)
		if str(self.request.user) != "AnonymousUser":
			usercreated = Project.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/project/project_detail_edit.html"
		context = {'form':form,"usercreated":usercreated,"category":category}
		if form.is_valid():
			project = Project.objects.get(id=self.kwargs['id'])
			project.title = form.cleaned_data.get('title')
			project.description = form.cleaned_data.get('description')
			project.detail = form.cleaned_data.get('detail')
			project.status = form.cleaned_data.get('status')
			project.category = form.cleaned_data.get('category')
			if form.cleaned_data.get("attachements"):
				project.attachements = form.cleaned_data.get("attachements")
			project.user = self.request.user
			project.save()
			return redirect("project_list")
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class CreateProject(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = ProjectForm()
		if str(self.request.user) != "AnonymousUser":
			usercreated = Project.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated  = ""
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/project/project_form.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ProjectForm(self.request.POST,self.request.FILES)
		if str(self.request.user) != "AnonymousUser":
			usercreated = Project.objects.filter(user=self.request.user,accepted="APPROVED")
		else:
			usercreated = ""
		category = ResearchProjectCategory.objects.all()
		context = {'form':form,"usercreated":usercreated,"category":category}
		template_name = "frontpages/project/project_form.html"
		context = {'form':form}
		if form.is_valid():
			project = Project()
			project = form.save(commit=False)
			if self.request.user.is_customer:
				project.accepted = "PENDING"
			else:
				project.accepted = "APPROVED"
			project.user=self.request.user
			#print("-----"+str(self.request.POST['attachements']))
			if form.cleaned_data.get("attachements"):
				project.attachements = form.cleaned_data.get("attachements")

			project.save()
			return redirect("project_form")
		return render(self.request, template_name,context)
