
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
		
from PIL import Image
from io import BytesIO
from django.core.files import File 
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

from collaborations.forms import (BlogsForm,BlogsEdit,BlogCommentForm)

# --------------------------------------------
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core import files

TEMP_PROFILE_IMAGE_NAME = "temp_profile.png"




class ListBlogCommentAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = BlogComment.objects.all()
		template_name = "admin/blog/blogComment/list.html"
		context = {'blogcomments':form}
		return render(self.request, template_name,context)

class AdminBlogComments(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		blogs = BlogComment.objects.filter(blog=self.kwargs['id'])
		template_name="admin/blog/blogComment/list.html"
		context={'blogcomments':blogs}
		return render(self.request, template_name,context)

class BlogCommentDetailAdmin(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = BlogComment.objects.get(id=self.kwargs['id'])
		template_name = "admin/blog/blogComment/detail.html"
		context = {'forms':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = BlogCommentForm(self.request.POST,self.request.FILES)
		template_name = "admin/blog/blogComment/detail.html"
		context = {'forms':form}
		if form.is_valid():
			blog = BlogComment.objects.get(id=self.kwargs['id'])
			blog.content=form.cleaned_data.get('content')
			blog.last_updated_by = self.request.user
			blog.last_updated_date = timezone.now()
			blog.save()
			messages.success(self.request, "Edited a Blog Comment Successfully")
			return redirect("admin:blogComment_list")
		return render(self.request, template_name,context)

class CreatBlog(LoginRequiredMixin,View):

	def get(self,*args,**kwargs):
		form = BlogsForm()
		template_name="admin/pages/blog_form.html"
		context={'form':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = BlogsForm(self.request.POST,self.request.FILES)
		import pprint
		pprint.pprint(self.request.FILES)
		context={'form':form}
		if form.is_valid():
			# the data we need for cropping
			x = self.request.POST.get('x')
			y = self.request.POST.get('y')
			w = self.request.POST.get('width')
			h = self.request.POST.get('height')
			## english Tags
			tag_list = ""
			for t in self.request.POST.getlist('tag'):
				print(t)
				tag_list+=t+","
			tag_list = tag_list[:-1]

			## amharic Tags
			tag_list_am = ""
			for t in self.request.POST.getlist('tag_am'):
				print(t)
				tag_list_am+=t+","
			tag_list_am = tag_list_am[:-1]
			company = self.request.user.get_company()
			blog = form.save(self.request.user,company,x,y,w,h,tag_list,tag_list_am)
			messages.success(self.request, "Added New Blog Successfully")
			return redirect("admin:admin_Blogs")
		return render(self.request, "admin/pages/blog_form.html",context)

class AdminBlogList(LoginRequiredMixin, ListView):
	template_name="admin/pages/blog_list.html"
	model = Blog
	context_object_name = 'blogs'
	def get_queryset(self):
		if self.request.user.is_superuser:
			return Blog.objects.all()
		else:
			return Blog.objects.filter(created_by = self.request.user)
	# def get(self,*args,**kwargs):
		# if self.request.user.is_superuser:
		# 	blogs = Blog.objects.all()
		# 	template_name="admin/pages/blog_list.html"
		# 	context={'blogs':blogs}
		# 	return render(self.request, template_name,context)
		# else:
		# 	blogs = Blog.objects.all()
		# 	filterdblogs = []
		# 	for blog in blogs:
		# 		if self.request.user.get_company == blog.user.get_company:
		# 			filterdblogs.append(blog)
		# 	template_name="admin/pages/blog_list.html"
		# # 	context={'blogs':filterdblogs}
		# 	return render(self.request, template_name,{'blogs':Blog.objects.all()})


		
class BlogView(LoginRequiredMixin,View):
	def tag(self,tags):
		for t in tags:
			tag_list = ""
			tag_list+=t+","
			tag_list = tag_list[:-1]
			return tag_list

	def get(self,*args,**kwargs):
		blogs = Blog.objects.get(id=self.kwargs['id']) 
		template_name="admin/pages/blog_detail.html"
		blog = BlogsForm()
		choices = ['Food','Beverage','Pharmaceutical']
		choices_am = [ 'ምግብ', 'መጠጥ', 'መድሀኒት']
		context = {'form':blogs,"choices":choices, "choices_am":choices_am}
		return render(self.request, "admin/pages/blog_detail.html",context)
	def post(self,*args,**kwargs):
		form = BlogsEdit(self.request.POST,self.request.FILES)
		context={'form':form}
		if form.is_valid():
			blog = Blog.objects.get(id=self.kwargs['id'])
			blog.title = self.request.POST['title']
			## english Tags
			blog.tag = self.tag(self.request.POST.getlist('tag'))
			#------------------
			blog.tag_am = self.tag(self.request.POST.getlist('tag_am'))
			#------------------
			blog.content = self.request.POST['content']
			blog.title_am = self.request.POST['title_am']
			blog.content_am = self.request.POST['content_am']
			publ = 'publish' in self.request.POST
			blog.publish = publ
			# -----------------
			blog.last_updated_by = self.request.user
			blog.last_updated_date = timezone.now()
			# -----------------
			if self.request.FILES.get('blogImage') == None:
				blog.save()
				messages.success(self.request, "Edited Blogs Successfully")
				return redirect("admin:admin_Blogs")
			elif self.request.FILES.get('blogImage') != None:
				x = self.request.POST.get('x')
				y = self.request.POST.get('y')
				w = self.request.POST.get('width')
				h = self.request.POST.get('height')
				blog.blogImage = self.request.FILES.get('blogImage')
				blogedit = BlogsEdit()
				blogedit.save(self.request.user,self.kwargs['id'],x,y,w,h,blog)
				messages.success(self.request, "Edited Blogs Successfully")
				return redirect("admin:admin_Blogs")
		return render(self.request, "admin/pages/blog_detail.html",context)

#-------------------

#blog-grid-right 
class BlogList(View):

	def get_tags(self,lang):
		blog = Blog.objects.filter(publish=True) 
		string = ""
		if(lang=="amharic"):
			for b in blog:
				string+=b.tag_am+','
		if(lang=="english"):
			for b in blog:
				string+=b.tag+','
		string = string[:-1]
		tag_list = string.split(',')
		tag_list = set(tag_list)
		return tag_list

	def get(self,*args,**kwargs):
		blog = Blog.objects.filter(publish=True) 
		template_name="frontpages/blog-grid-right.html"
		tags=self.get_tags("english")
		tags_am=self.get_tags("amharic")
		context={'blogs':blog,'tags':tags,'tags_am':tags_am}
		return render(self.request, template_name,context)


class CreateBlogComment(LoginRequiredMixin,View):

	def post(self,*args,**kwargs):
		form = BlogCommentForm(self.request.POST)
		blog = Blog.objects.get(id=self.kwargs['id'])
		template_name="frontpages/blog-details-right.html" 
		if form.is_valid():
			blogComment=BlogComment(blog=blog,created_by=self.request.user,content=form.cleaned_data.get('content'))
			blogComment.save()
			return redirect(reverse("blog_details",kwargs={'id':str(self.kwargs['id'])}))
		return render(self.request, template_name,context)

class SearchBlog(View):
	def get_tags(self,lang):
		blog = Blog.objects.filter(publish=True) 
		string = ""
		if(lang=="amharic"):
			for b in blog:
				string+=b.tag_am+','
		if(lang=="english"):
			for b in blog:
				string+=b.tag+','
		string = string[:-1]
		tag_list = string.split(',')
		tag_list = set(tag_list)
		return tag_list

	def get(self,*args,**kwargs):
		return redirect(reverse("blog_grid_right"))

	def post(self,*args,**kwargs):
		blog = Blog.objects.filter(title__contains=self.request.POST['search'])
		template_name = "frontpages/blog-grid-right.html"
		print(blog)
		tags=self.get_tags("english")
		tags_am=self.get_tags("amharic")
		context = {'blogs':blog,'tags':tags,'tags_am':tags_am}
		return render(self.request, template_name,context)

class SearchBlogTag(View):
	def get_tags(self,lang):
		blog = Blog.objects.filter(publish=True) 
		string = ""
		if(lang=="amharic"):
			for b in blog:
				string+=b.tag_am+','
		if(lang=="english"):
			for b in blog:
				string+=b.tag+','
		string = string[:-1]
		tag_list = string.split(',')
		tag_list = set(tag_list)
		return tag_list


	def get(self,*args,**kwargs):
		blog = Blog.objects.filter(tag__contains=self.kwargs['name'])
		template_name = "frontpages/blog-grid-right.html"
		print(blog)
		tags=self.get_tags("english")
		tags_am=self.get_tags("amharic")
		context = {'blogs':blog,'tags':tags,'tags_am':tags_am}
		return render(self.request, template_name,context)

class BlogDetail(View):
	def get_tags(self,lang):
		blog = Blog.objects.filter(publish=True) 
		string = ""
		if(lang=="amharic"):
			for b in blog:
				string+=b.tag_am+','
		if(lang=="english"):
			for b in blog:
				string+=b.tag+','
		# deleting the last ,
		string = string[:-1] 
		tag_list = string.split(',')
		# making the list unique
		tag_list = set(tag_list)
		return tag_list

	def get(self,*args,**kwargs):
		blog = Blog.objects.get(id=self.kwargs['id'])
		comment = BlogCommentForm()
		tags=self.get_tags("english")
		tags_am=self.get_tags("amharic")
		template_name="frontpages/blog-details-right.html" 
		context = {'blog':blog,'comment':comment,'tags':tags,'tags_am':tags_am}
		return render(self.request, template_name,context)
