#python,django,library,our pakages
from django.urls import reverse
from django.views import View
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView	 #redirect with context

from django.contrib import messages
from PIL import Image

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


from collaborations.forms import (ResearchForm,ResearchProjectCategoryForm)
from collaborations.models import Research,ResearchAttachment,ResearchProjectCategory
from collaborations.views import  filter_by,  get_paginated_data

from admin_site.decorators import company_created,company_is_active
from django.utils import timezone


def image_cropper(x,y,w,h,raw_image):
        # if the image is not cropped 
		if (x == '' or y == '' or w == '' or h == ''):
			image = Image.open(raw_image)
			resized_image = image.resize((400, 140), Image.ANTIALIAS)
			resized_image.save(raw_image.path)
			return True
		
		x = float(x)
		y = float(y)
		w = float(w)
		h = float(h)
		image = Image.open(raw_image)
		cropped_image = image.crop((x, y, w+x, h+y))
		cropped_image.save(raw_image.path)
		return True



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
		try:
			context = {}
			if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
				context['researchs'] = Research.objects.all()
			else:
				context['researchs'] = Research.objects.filter(company = self.request.user.get_company())
			template_name = "admin/researchproject/research_list.html"
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at ListResearchAdmin ",e)
			messages.warning(self.request, "An Exception Occured!")
			return redirect("admin:index")
		

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
		return render(self.request, template_name,{'forms':form})
	def post(self,*args,**kwargs):
		try:
			form = ResearchForm(self.request.POST, self.request.FILES)
			if form.is_valid():
				research = form.save(commit=False)
				research.accepted = "APPROVED"
				research.created_by = self.request.user
				research.save()
				data = self.request.POST
				image_cropper(data['x'],data['y'],data['width'],data['height'], research.image )
				if 'files' in self.request.FILES:
					for file in self.request.FILES.getlist('files'):
						researchattachment= ResearchAttachment(research = research, attachement = file)
						researchattachment.save()
				
				messages.success(self.request, "Added New Research Successfully")
				return redirect("admin:research_list")
			
			messages.warning(self.request, "Invalid Form!")
			return render(self.request, "admin/researchproject/research_form.html", {'forms':form})

		except Exception as e:
			print("@@@ Exception occured at CreateResearchAdmin ",e)
			messages.warning(self.request, "An Exception Occured ")
			return redirect("admin:research_list")


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
			research = Research.objects.get(id=self.kwargs['id'])
			template_name = "admin/researchproject/research_detil.html"
			researchcategory=ResearchProjectCategory.objects.all()
			context = {'research':research,"category":researchcategory, 'form':ResearchForm(instance=research)}
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@@ Exception at ResearchDetailAdmin ",e)
			return redirect("admin:research_list")
	def post(self,*args,**kwargs):
		try:
			research = Research.objects.get(id=self.kwargs['id'])
			form = ResearchForm(self.request.POST, self.request.FILES, instance=research)
			if form.is_valid():
				research=form.save(commit=False)
				research.last_updated_by = self.request.user
				research.last_updated_date = timezone.now()
				research.save()
				data = self.request.POST
				image_cropper(data['x'],data['y'],data['width'],data['height'], research.image )
				if 'files' in self.request.FILES:
					for file in self.request.FILES.getlist('files'):
						researchattachment= ResearchAttachment(research = research, attachement = file)
						researchattachment.save()
				messages.success(self.request, "Edited Research Successfully")
				return redirect("admin:research_list")
			template_name = "admin/researchproject/research_detil.html"
			researchcategory=ResearchProjectCategory.objects.all()
			context = {'research':research,"category":researchcategory, 'form':form}
			messages.warning(self.request, 'Invalid Form Data!')
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at POST of Research Detail",e )
			messages.warning(self.request, "An Exception Occured!")
			return redirect("admin:research_list")


# customer side
class ListResearch(View):
	def get(self,*args,**kwargs):
		try:
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
			context = {'researchs':data, "category":ResearchProjectCategory.objects.all(), 'message':result['message'], 'message_am':result['message_am']}
			
			if not self.request.user.is_anonymous:
				context['usercreated'] = Research.objects.filter(created_by=self.request.user)
			
			return render(self.request, template_name, context)

		except Exception as e:
			print("@@@ Exception at List Research ",e)
			return redirect("research_list")


class SearchResearch(View):
	def get(self,*args,**kwargs):
		return redirect(reverse("research_list"))
	def post(self,*args,**kwargs):
		try:
			form = Research.objects.filter(title__contains=self.request.POST['search'])
			if self.request.user.is_anonymous:
				usercreated = Research.objects.filter(created_by=self.request.user,accepted="APPROVED")
			else:
				usercreated = ""
			category = ResearchProjectCategory.objects.all()
			context = {'researchs':form,"usercreated":usercreated,"category":category}
			template_name = "frontpages/research/research_list.html"
			
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at Search Research")
			return redirect("/")


class ResearchCategorySearch(View):
	def get(self,*args,**kwargs):
		try:
			form = Research.objects.filter(accepted="APPROVED",category=self.kwargs['id'])
			if str(self.request.user) != "AnonymousUser":
				usercreated = Research.objects.filter(created_by=self.request.user,accepted="APPROVED")
			else:
				usercreated = ""
			category = ResearchProjectCategory.objects.all()
			context = {'researchs':form,"usercreated":usercreated,"category":category}
			template_name = "frontpages/research/research_list.html"
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at Research Category")
			return redirect("/")


class ResearchDetail(View):
	def get(self,*args,**kwargs):
		try:
			form = Research.objects.get(id=self.kwargs['id'])
			related = Research.objects.filter(category=form.category).exclude(id=self.kwargs['id'])[:6]
			category = ResearchProjectCategory.objects.all()
			context = {'research':form,"category":category,"related":related,"message":"Research"}
			if not self.request.user.is_anonymous:
				context['usercreated'] = Research.objects.filter(created_by=self.request.user)
			template_name = "frontpages/research/research_detail.html"
			
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at Research Detail")
			return redirect("/")


class EditResearch(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		try:
			form = Research.objects.get(id=self.kwargs['id'])
			usercreated = Research.objects.filter(created_by=self.request.user)
			category = ResearchProjectCategory.objects.all()
			context = {'form':form,"usercreated":usercreated,"category":category}
			template_name = "frontpages/research/research_detail_edit.html"
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at EditResearch ",e)
			return redirect("research_list")
	def post(self,*args,**kwargs):
		form =  ResearchForm(self.request.POST,self.request.FILES)
		usercreated = Research.objects.filter(created_by=self.request.user,accepted="APPROVED")
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
		try:
			usercreated = Research.objects.filter(created_by=self.request.user)
			category = ResearchProjectCategory.objects.all()
			context = {'form':ResearchForm,"usercreated":usercreated,"category":category}
			template_name = "frontpages/research/research_form.html"
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at CreateResearch ",e)
			return redirect("research_list")

	def post(self,*args,**kwargs):
		
			form = ResearchForm(self.request.POST,self.request.FILES)
			if form.is_valid():
				research = form.save(commit=False)
				if self.request.user.is_customer:
					research.accepted = "PENDING"
				else:
					research.accepted = "APPROVED"
				research.created_by = self.request.user
				research.save()
				data = self.request.POST
				image_cropper(data['x'],data['y'],data['width'],data['height'], research.image )
				if 'files' in self.request.FILES:
					for file in self.request.FILES.getlist('files'):
						researchattachment= ResearchAttachment(research = research, attachement =file)
						researchattachment.save()
				messages.success(self.request, "Added New Research Successfully")
				return redirect("research_list")

			template_name = "frontpages/research/research_form.html"
			category = ResearchProjectCategory.objects.all()
			return render(self.request, template_name, {'form':form, "category":category})
		# except Exception as e:
		# 	print("@@@ Exception at Creating Research ", e)
		# 	return redirect("research_list")
