
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
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core import files

TEMP_PROFILE_IMAGE_NAME = "temp_profile.png"

class CropImage(LoginRequiredMixin):
	def save_temp_profile(imageString, user):
		INCORRECT_PADDING_EXCEPTION = "incorrect padding"
		try:
			if not os.path.exists(settings.TEMP):
				os.mkdir(settings.TEMP)
			if not os.path.exists(f"{setting.TEMP}/{user.pk}"):
				os.mkdir(f"{setting.TEMP}/{user.pk}")
			url = os.path.join(f"{setting.TEMP}/{user.pk}",TEMP_PROFILE_IMAGE_NAME)
			storage = FileSystemStorage(Location=url)
			image = base64.b64decode(imageString)
			with storage.open('','wb+') as destination:
				destination.write(image)
				destination.close()
			return url
		except Expectation as e:
			if str(e) == INCORRECT_PADDING_EXCEPTION:
				imageString +='='* ((4-len(imageString) % 4) % 4)
				return save_temp_profile(imageString, user)
		return None

	def post(request, *args, **kwargs):
		payload = {}
		user = self.request.user
		if self.request.POST and user.is_authenticated:
			try:
				imageString = self.request.POST.get('image')
				url = save_temp_profile(imageString, user)

				img = cv2.imread(url)
				cropX = int(float(str(request.POST.get("cropX"))))
				cropY = int(float(str(request.POST.get("cropY"))))
				cropWidth = int(float(str(request.POST.get("cropWidth"))))
				cropHeight = int(float(str(request.POST.get("cropHeight"))))

				if cropX < 0:
					cropX = 0
				if cropY < 0:
					cropY = 0
				crop_img = img[cropY:cropY + cropHeight,cropX:cropX + cropWidth ]

				cv2.imwrite(url, crop_img)
				##

				payload['result'] = "success"
				payload['cropped_profile_image'] = user.profile_image.url

				os.remove(url)
			except Expectation as e:
				payload['result'] = "Error"
				payload['exception'] = str(e)
		return HttpResponse(json.dumps(payload), content_type="application/json")


class ListBlogCommentAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = BlogComment.objects.all()
		template_name = "admin/blog/blogComment/list.html"
		context = {'blogcomments':form}
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
			blog.save()
			messages.success(self.request, "Edited a Blog Comment Successfully")
			return redirect("admin:blogComment_list")
		return render(self.request, template_name,context)

class CreatBlog(LoginRequiredMixin,View):
	def save_temp_profile(imageString, user):
		INCORRECT_PADDING_EXCEPTION = "incorrect padding"
		try:
			if not os.path.exists(settings.TEMP):
				os.mkdir(settings.TEMP)
			if not os.path.exists(f"{setting.TEMP}/{user.pk}"):
				os.mkdir(f"{setting.TEMP}/{user.pk}")
			url = os.path.join(f"{setting.TEMP}/{user.pk}",TEMP_PROFILE_IMAGE_NAME)
			storage = FileSystemStorage(Location=url)
			image = base64.b64decode(imageString)
			with storage.open('','wb+') as destination:
				destination.write(image)
				destination.close()
			return url
		except Expectation as e:
			if str(e) == INCORRECT_PADDING_EXCEPTION:
				imageString +='='* ((4-len(imageString) % 4) % 4)
				return save_temp_profile(imageString, user)
		return None
	def get(self,*args,**kwargs):
		form = BlogsForm()
		template_name="admin/pages/blog_form.html"
		context={'form':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = BlogsForm(self.request.POST,self.request.FILES)
		print("pork is good and bad - 1")
		print(self.request.POST['x'])
		print("pork is good and bad - 2")
		print(self.request.POST.get('y'))
		print("pork is good and bad - 3")
		print(self.request.POST.get('width'))
		print("pork is good and bad - 4")
		print(self.request.POST.get('height'))
		context={'form':form}
		if form.is_valid():

			x = self.request.POST.get('x')
			x = float(x)

			y = self.request.POST.get('y')
			
			y = float(y)
			w = self.request.POST.get('width')
			
			w = float(w)
			h = self.request.POST.get('height')
			
			h = float(h)
			blog = Blog()
			blog = form.save(self.request.user,x,y,w,h)
			blog.save()
			# print(blog.blogImage)
			# blog.user = self.request.user


			"""
			title = models.CharField(max_length=10000,null=False)
		    title_am = models.CharField(max_length=10000,null=False)
		    tag = models.CharField(max_length=500,null=False)
		    tag_am = models.CharField(max_length=500,null=False)
		    blogImage = models.ImageField(null=True,upload_to='Blogimage')
		    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
		    content = models.TextField(null=False)
		    content_am = models.TextField(null=False)
		    timestamp = models.DateTimeField(auto_now_add=True)
		    publish = models.BooleanField(null=False,default=False)
			# """
			# blog.title = form.cleaned_data.get('title')
			# blog.title_am = form.cleaned_data.get('title_am')
			# blog.tag = form.cleaned_data.get('tag')
			# blog.tag_am = form.cleaned_data.get('tag_am')
			# blog.content = form.cleaned_data.get('content')
			# blog.content_am = form.cleaned_data.get('content_am')
			# blog.publish = form.cleaned_data.get('publish')

			# blog.save()
			# #url = save_temp_profile(imageString, user)
			# #blog.blogImage = form.cleaned_data.get("blogImage")
			# print("----")
			# # print(form.x)
			# # publish =self.request.POST['publish']
			# # print(str(publish))
			# # if publish =="on":
			# # 	blog.publish=True 
			# # else:
			# # 	blog.publish=False            
			# print("must be working")
			# x = self.request.POST.get('x')
			
			# x = float(x)
			# print("x "+str(x))
			# y = self.request.POST.get('y')
			
			# y = float(y)
			# w = self.request.POST.get('width')
			
			# w = float(w)
			# h = self.request.POST.get('height')
			
			# h = float(h)


			# print(blog.blogImage.name)
			# ("------f-f-o-o----")
			# #----------------------------------------------
			# image = Image.open(blog.blogImage)
			# print(image)
			# cropped_image = image.crop((x, y, w+x, h+y))
			# print(cropped_image)
			# #blog.blogImage = cropped_image
			# #----------------------------------------------
			# rgb_im = cropped_image.convert('RGB')
			# rgb_im.save('audacious.jpg')
			# blob = BytesIO()
			# rgb_im.save(blob) 
			# fork = "cropped-" + str(blog.blogImage.name)
			# blog.blogImage.save(fork, File(rgb_im),save=False)
			# #blog.blogImage.save(blog.blogImage.name, File(cropped_image))
			# # resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
			# # resized_image.save(blog.blogImage.path)
			
			messages.success(self.request, "Added New Blog Successfully")
			form = BlogsForm()
			context={'form':form}
			return render(self.request, "admin/pages/blog_form.html",context)
		return render(self.request, "admin/pages/blog_form.html",context)

class AdminBlogList(LoginRequiredMixin,View):
	template_name="admin/pages/blog_list.html"
	def get(self,*args,**kwargs):
		if self.request.user.is_superuser:
			blogs = Blog.objects.all()
			template_name="admin/pages/blog_list.html"
			context={'blogs':blogs}
			return render(self.request, template_name,context)
		else:
			blogs = Blog.objects.all()
			filterdblogs = []
			for blog in blogs:
				if self.request.user.get_company == blog.user.get_company:
					filterdblogs.append(blog)
			template_name="admin/pages/blog_list.html"
			context={'blogs':filterdblogs}
			return render(self.request, template_name,context)
		
class BlogView(LoginRequiredMixin,View):
	template_name="admin/pages/blog_list.html"
	def get(self,*args,**kwargs):
		blogs = Blog.objects.get(id=self.kwargs['id'])
		template_name="admin/pages/blog_detail.html"
		print("^^^^^^^^^^^")
		print(blogs.publish)
		context = {'form':blogs}
		return render(self.request, "admin/pages/blog_detail.html",context)
	def post(self,*args,**kwargs):
		form = BlogsEdit(self.request.POST,self.request.FILES)
		context={'form':form}
		if form.is_valid():
			blog = Blog.objects.get(id=self.kwargs['id'])
		 
			blog.title = self.request.POST['title']
			blog.tag = self.request.POST['tag']
			blog.content = self.request.POST['content']
			blog.title_am = self.request.POST['title_am']
			blog.tag_am = self.request.POST['tag_am']
			blog.content_am = self.request.POST['content_am']
			publ = 'publish' in self.request.POST
			print("+++++++++++++"+str(publ))
			blog.publish = publ
			if self.request.FILES.get('blogImage') == None:
					pass
			elif self.request.FILES.get('blogImage') != None:
					blog.blogImage = self.request.FILES.get('blogImage')
			blog.save()
			messages.success(self.request, "Edited Blogs Successfully")
			return redirect("admin:admin_Blogs")
		return render(self.request, "admin/pages/blog_detail.html",context)

#-------------------

#blog-grid-right 
class BlogList(View):

	def get_tags(self,*args,**kwargs):
		blog = Blog.objects.filter(publish=True) 
		stringlist = []
		truestring = []
		for b in blog:
			splited = b.tag.split(" ");
			for split in splited:
				stringlist.append(split)

		taglist = set(stringlist)
		taglist = list(taglist)

		for string in taglist:
			if string == '':
				continue
			truestring.append(string)
		return truestring

	def get(self,*args,**kwargs):
		blog = Blog.objects.filter(publish=True) 
		template_name="frontpages/blog-grid-right.html"
		tags=self.get_tags()
		context={'blogs':blog,'tags':tags}
		return render(self.request, template_name,context)

class CreateBlogComment(LoginRequiredMixin,View):

	def post(self,*args,**kwargs):
		form = BlogCommentForm(self.request.POST)
		blog = Blog.objects.get(id=self.kwargs['id'])
		template_name="frontpages/blog-details-right.html" 
		if form.is_valid():
			blogComment=BlogComment(blog=blog,sender=self.request.user,content=form.cleaned_data.get('content'))
			blogComment.save()
			return redirect(reverse("blog_details",kwargs={'id':str(self.kwargs['id'])}))
		return render(self.request, template_name,context)

class SearchBlog(View):
	def get_tags(self,*args,**kwargs):
		blog = Blog.objects.filter(publish=True) 
		stringlist = []
		truestring = []
		for b in blog:
			splited = b.tag.split(" ");
			for split in splited:
				stringlist.append(split)

		taglist = set(stringlist)
		taglist = list(taglist)

		for string in taglist:
			if string == '':
				continue
			truestring.append(string)
		return truestring

	def get(self,*args,**kwargs):
		return redirect(reverse("blog_grid_right"))

	def post(self,*args,**kwargs):
		blog = Blog.objects.filter(title__contains=self.request.POST['search'])
		template_name = "frontpages/blog-grid-right.html"
		print(blog)
		context = {'blogs':blog,'tags':self.get_tags()}
		return render(self.request, template_name,context)

class SearchBlogTag(View):
	def get_tags(self,*args,**kwargs):
		blog = Blog.objects.filter(publish=True) 
		stringlist = []
		truestring = []
		for b in blog:
			splited = b.tag.split(" ");
			for split in splited:
				stringlist.append(split)

		taglist = set(stringlist)
		taglist = list(taglist)

		for string in taglist:
			if string == '':
				continue
			truestring.append(string)
		return truestring


	def get(self,*args,**kwargs):
		blog = Blog.objects.filter(tag__contains=self.kwargs['name'])
		template_name = "frontpages/blog-grid-right.html"
		print(blog)
		context = {'blogs':blog,'tags':self.get_tags()}
		return render(self.request, template_name,context)

class BlogDetail(View):
	def get_tags(self,*args,**kwargs):
		blog = Blog.objects.filter(publish=True) 
		stringlist = []
		truestring = []
		for b in blog:
			splited = b.tag.split(" ");
			for split in splited:
				stringlist.append(split)
		taglist = set(stringlist)
		taglist = list(taglist)

		for string in taglist:
			if string == '':
				continue
			truestring.append(string)
		return truestring

	def get(self,*args,**kwargs):
		blog = Blog.objects.get(id=self.kwargs['id'])
		comment = BlogCommentForm()
		template_name="frontpages/blog-details-right.html" 
		context = {'blog':blog,'comment':comment,'tags':self.get_tags()}
		return render(self.request, template_name,context)
