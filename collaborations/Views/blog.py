
from django.urls import reverse
import datetime
from django.views import View
from django.utils import timezone

from collaborations.models import Blog, BlogComment
from django.shortcuts import render, redirect, reverse

from django.views.generic import  ListView
from collaborations.models import  Blog, BlogComment, Blog, BlogComment
									 #redirect with context
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from company.models import Company
from accounts.models import  Company
import os
from django.contrib.auth.mixins import LoginRequiredMixin



from admin_site.decorators import company_created,company_is_active


from collaborations.forms import BlogsForm,BlogsEdit, BlogCommentForm

from collaborations.forms import (BlogsForm, BlogCommentForm)

from collaborations.models import ( Blog, BlogComment)

from collaborations.forms import (BlogsForm,BlogsEdit,BlogCommentForm)
from collaborations.views import get_paginated_data,  FilterByCompanyname
from django.db.models import Q
# --------------------------------------------
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core import files

TEMP_PROFILE_IMAGE_NAME = "temp_profile.png"
decorators = [never_cache, company_created(),company_is_active()]



@method_decorator(decorators,name='get')
class ListBlogCommentAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = BlogComment.objects.all()
		template_name = "admin/blog/blogComment/list.html"
		context = {'blogcomments':form}
		return render(self.request, template_name,context)

@method_decorator(decorators,name='get')
class AdminBlogComments(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		try:
			blogs = BlogComment.objects.filter(blog=self.kwargs['id'])
			template_name="admin/blog/blogComment/list.html"
			context={'blogcomments':blogs}
			return render(self.request, template_name,context)
		except Exception as e:
			print ("@@@ Exception at Blog comments ",e)
			messages.warning(self.request, "An Exception Occured!")
			return redirect("admin:index")

@method_decorator(decorators,name='dispatch')
class BlogCommentDetailAdmin(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		try:
			form = BlogComment.objects.get(id=self.kwargs['id'])
			template_name = "admin/blog/blogComment/detail.html"
			context = {'forms':form}
			return render(self.request, template_name,context)
		except Exception as e:
				print("@@@ Exception at Blog Comment Detail ",e)
				return redirect ("admin:index")

	def post(self,*args,**kwargs):
		try:
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
		except Exception as e:
			print ("@@@ Exception at Blog Comment Detail ",e)
			messages.warning(self.request, "An Exception Occured!")
			return redirect("admin:index")

@method_decorator(decorators,name='dispatch')
class CreatBlog(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = BlogsForm()
		template_name="admin/blog/blog/blog_form.html"
		context={'form':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		try:
			form = BlogsForm(self.request.POST,self.request.FILES)
			context={'form':form}
			if form.is_valid():
				x = self.request.POST.get('x')
				y = self.request.POST.get('y')
				w = self.request.POST.get('width')
				h = self.request.POST.get('height')
				## english Tags
				tag_list = ""
				for t in self.request.POST.getlist('tag'):
					tag_list+=t+","
				tag_list = tag_list[:-1]

				## amharic Tags
				tag_list_am = ""
				for t in self.request.POST.getlist('tag_am'):
					tag_list_am+=t+","
				tag_list_am = tag_list_am[:-1]
				company = self.request.user.get_company()
				blog = form.save(self.request.user,company,x,y,w,h,tag_list,tag_list_am)
				messages.success(self.request, "Added New Blog Successfully")
				return redirect("admin:admin_Blogs")
			return render(self.request, "admin/blog/blog/blog_form.html",context)
		except Exception as e:
			print ("@@@ Exception at Blog Create ",e)
			messages.warning(self.request, "An Exception Occured!")
			return redirect("admin:index")

@method_decorator(decorators,name='dispatch')
class AdminBlogList(LoginRequiredMixin, ListView):
	template_name="admin/blog/blog/blog_list.html"
	model = Blog
	context_object_name = 'blogs'
	def get_queryset(self):
		if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
			return Blog.objects.all()
		else:
			return Blog.objects.filter(created_by = self.request.user)
	# def get(self,*args,**kwargs):
		# if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
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
		try:
			blogs = Blog.objects.get(id=self.kwargs['id']) 
			template_name="admin/blog/blog/blog_detail.html"
			choices = ['Food','Beverage','Pharmaceutical']
			choices_am = [ 'ምግብ', 'መጠጥ', 'መድሀኒት']
			context = {'form':blogs,"choices":choices, "choices_am":choices_am}
			return render(self.request, template_name,context)
		except Exception as e:
			print ("@@@ Exception at BlogView ",e)
			messages.warning(self.request, "An Exception Occured!")
			return redirect("admin:index")

	def post(self,*args,**kwargs):
		try:
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
			return render(self.request, "admin/blog/blog/blog_detail.html",context)
		except Exception as e:
			print("@@@ Exception occured at BlogView POst ",e)
			messages.warning(self.request, "An Exception Occured!")
			return redirect("admin:index")


def set_message(result):
		if result['query'].count()==0:
			result['message'] = 'No Result Found!'
			result['message_am'] = "ምንም ውጤት አልተገኘም"
		else:
			result['message'] = f"{result['query'].count()} result found !"
			result['message_am']  = f"{result['query'].count()} ውጤት ተገኝቷል"
		return result

def get_tags(lang):
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

class BlogList(View):
	def get(self, *args,**kwargs):
		result ={}
		try:
			if 'by_company' in self.request.GET:
				result = FilterByCompanyname(self.request.GET.getlist('by_company'), Blog.objects.filter(publish=True))
			else:
				result['query'] = Blog.objects.filter(publish = True)
				if 'by_title' in self.request.GET:
					q = Q( Q(title__icontains = self.request.GET['by_title']) | Q(title_am__icontains = self.request.GET['by_title']) )
					result['query'] = result['query'].filter(q)
					result = set_message(result)
				elif 'by_tag' in self.request.GET:
					q = Q( Q(tag__icontains = self.request.GET['by_tag']) | Q(tag_am__icontains = self.request.GET['by_tag']) )
					result['query'] = result['query'].filter(q)
					result = set_message(result)
				else:
					result['query'] = Blog.objects.filter(publish=True)
					result['message']  = "Blogs"
					result['message_am'] = Blog.model_am
			tags = get_tags("english")
			tags_am = get_tags("amharic")
			companies = []
			for comp in Company.objects.all():
				if comp.blog_set.count() > 0:
					companies.append(comp)
			data = get_paginated_data(self.request, result['query'])
			return render(self.request, "frontpages/blog/blog_list.html", {'blogs':data, 'message':result['message'],  'message_am':result['message_am'],'companies':companies,'tags':tags,'tags_am':tags_am})
		
		except Exception as e:
			print("@@@ Exception at Blog List ",e)
			return redirect("/")

class CreateBlogComment(LoginRequiredMixin,View):
	def post(self,*args,**kwargs):
		try:
			form = BlogCommentForm(self.request.POST)
			blog = Blog.objects.get(id=self.kwargs['id'])
			template_name="frontpages/blog/blog-details-right.html" 
			if form.is_valid():
				blogComment=BlogComment(blog=blog,created_by=self.request.user,content=form.cleaned_data.get('content'))
				blogComment.save()
				return redirect(reverse("blog_details",kwargs={'id':str(self.kwargs['id'])}))
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@ Exception at CreateBlogComment ",e)
			return redirect("/collaborations/blog-list/")

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
		try:
			blog = Blog.objects.get(id=self.kwargs['id'])
			comment = BlogCommentForm()
			tags=self.get_tags("english")
			tags_am=self.get_tags("amharic")
			template_name="frontpages/blog/blog_detail.html" 
			context = {'blog':blog,'comment':comment,'tags':tags,'tags_am':tags_am}
			return render(self.request, template_name,context)
		except Exception as e:
			print("@@@@ Exception at BlogDetail ", e)
			return redirect("/collaborations/blog-list/")
