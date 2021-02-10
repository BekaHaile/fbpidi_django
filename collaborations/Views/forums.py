
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

from collaborations.forms import (ForumQuestionForm,CommentForm,CommentReplayForm)

from collaborations.models import ( ForumQuestion, ForumComments,
									CommentReplay)
class ListForumQuestionAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = ForumQuestion.objects.all()
		template_name = "admin/forum/Forumquestions/list.html"
		context = {'researchprojectcategorys':form}
		return render(self.request, template_name,context)

class CreateForumQuestionAdmin(LoginRequiredMixin, View):
	def get(self,*args,**kwargs):
		form = ForumQuestionForm()
		template_name = "admin/forum/Forumquestions/form.html"
		context = {'forms':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ForumQuestionForm(self.request.POST,self.request.FILES)
		template_name = "admin/forum/Forumquestions/form.html"
		context = {'forms':form}
		if form.is_valid():
			forum = ForumQuestion()
			forum = form.save(commit=False)
			if form.cleaned_data.get("attachements"):
				forum.attachements = form.cleaned_data.get("attachements")
			forum.user = self.request.user
			forum.save()
			messages.success(self.request, "Added New Forum Successfully")
			return redirect("admin:forum_form")
		return render(self.request, template_name,context)

class ForumQuestionDetail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = ForumQuestion.objects.get(id=self.kwargs['id'])
		template_name = "admin/forum/Forumquestions/detail.html"
		context = {'forms':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ForumQuestionForm(self.request.POST,self.request.FILES)
		emplate_name = "admin/forum/Forumquestions/detail.html"
		context = {'forms':form}
		if form.is_valid():
			research = ForumQuestion.objects.get(id=self.kwargs['id'])
			research.title=form.cleaned_data.get('title')
			research.description=form.cleaned_data.get('description')
			if form.cleaned_data.get("attachements"):
				research.attachements = form.cleaned_data.get("attachements")
			#research.user = self.request.user 
			research.save()
			messages.success(self.request, "Edited a Forum Successfully")
			return redirect("admin:forum_list")
		return render(self.request, template_name,context)

class ListForumCommentAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = ForumComments.objects.all()
		template_name = "admin/forum/ForumComments/list.html"
		context = {'researchprojectcategorys':form}
		return render(self.request, template_name,context)

class ForumCommentsDetail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = ForumComments.objects.get(id=self.kwargs['id'])
		template_name = "admin/forum/ForumComments/detail.html"
		context = {'forms':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = CommentForm(self.request.POST,self.request.FILES)
		emplate_name = "admin/forum/ForumComments/detail.html"
		context = {'forms':form}
		if form.is_valid():
			research = ForumComments.objects.get(id=self.kwargs['id'])
			research.comment=form.cleaned_data.get('comment')
			if form.cleaned_data.get("attachements"):
				research.attachements = form.cleaned_data.get("attachements")
			#research.user = self.request.user 
			research.save()
			messages.success(self.request, "Edited a Forum Comment Successfully")
			return redirect("admin:forum_comment_list")
		return render(self.request, template_name,context)

class ListCommentReplayAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = CommentReplay.objects.all()
		template_name = "admin/forum/CommentReplay/list.html"
		context = {'researchprojectcategorys':form}
		return render(self.request, template_name,context)

class CommentReplayDetail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = CommentReplay.objects.get(id=self.kwargs['id'])
		template_name = "admin/forum/CommentReplay/detail.html"
		context = {'forms':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = CommentReplayForm(self.request.POST,self.request.FILES)
		emplate_name = "admin/forum/CommentReplay/detail.html"
		context = {'forms':form}
		if form.is_valid():
			research = CommentReplay.objects.get(id=self.kwargs['id'])
			research.content=form.cleaned_data.get('content')
			if form.cleaned_data.get("attachements"):
				research.attachements = form.cleaned_data.get("attachements")
			research.user = self.request.user 
			research.save()
			messages.success(self.request, "Edited a Forum Comment Successfully")
			return redirect("admin:comment_replay_list")
		return render(self.request, template_name,context)


class EditCommentForum(View):
	def post(self,*args,**kwargs):
		if(self.kwargs['type']=="ForumComments"):
			forum = CommentForm(self.request.POST,self.request.FILES)
			comment = ForumComments.objects.get(id=self.kwargs['id'])
			comment.comment =  forum.cleaned_data.get("content")
			if forum.cleaned_data.get("attachements"):
				comment.attachements = forum.cleaned_data.get("attachements")
			comment.save()
			return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
		if(self.kwargs['type']=="CommentReplay"):
			forum = CommentReplayForm(self.request.POST,self.request.FILES)
			comment = CommentReplay.objects.get(id=self.kwargs['id'])
			comment.content =  self.request.POST["content"]
			if forum.cleaned_data.get("attachements"):
				comment.attachements = forum.cleaned_data.get("attachements")
			comment.save()
			return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
			

class CreateCommentReplay(LoginRequiredMixin,View):
	def post(self,*args,**kwargs):
		print("We are here")
		comment = CommentReplayForm(self.request.POST,self.request.FILES)
		forum = ForumQuestion.objects.get(id=self.kwargs['forum'])
		main = ForumComments.objects.get(id=self.kwargs['id'])
		empity = CommentForm()
		context = {'forum':forum,'commentForm':empity}
		if comment.is_valid():
			form = CommentReplay()
			form = comment.save(commit=False)
			form.comment = main
			if comment.cleaned_data.get("attachements"):
				form.attachements = comment.cleaned_data.get("attachements")
			form.user = self.request.user
			form.save()
			print(str(comment.cleaned_data.get("attachements")))
			print("this worked")
			return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
		print("it didn't worked")
		template_name = "frontpages/forums/forum_detail.html"
		return render(self.request, template_name,context)

#----- create forum quesion
class CreateForumQuestion(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        forum = ForumQuestionForm()
        template_name="frontpages/forums/forums_form.html" 
        userCreated = ForumQuestion.objects.filter(user=self.request.user)
        context = {'form':forum,'usercreated':userCreated}
        return render(self.request,template_name,context)
    def post(self,*args,**kwargs):
        form = ForumQuestionForm(self.request.POST,self.request.FILES)
        userCreated = ForumQuestion.objects.filter(user=self.request.user)
        context = {'form':form,'usercreated':userCreated}
        template_name="frontpages/forums/forums_form.html" 
        if form.is_valid():
            forum = ForumQuestion()
            forum = form.save(commit=False)
            forum.user = self.request.user
            if form.cleaned_data.get("attachements"):
            	forum.attachements = form.cleaned_data.get("attachements")
            print("one")
            forum.save()
            forum = ForumQuestionForm()
            context={'form':forum}
            return redirect("forum_list")
        return render(self.request, template_name,context)

class ListForumQuestions(View):
	def get(self,*args,**kwargs):
		forum = ForumQuestion.objects.all()
		print("-------"+str(self.request.user))
		print(str(forum))
		if str(self.request.user) != "AnonymousUser":
			userCreated = ForumQuestion.objects.filter(user=self.request.user)
		else:
			userCreated = ""
		template_name = "frontpages/forums/forum_list.html"
		context = {'forums':forum,'usercreated':userCreated}
		return render(self.request, template_name,context)

class EditForumQuestions(View):
	def get(self,*args,**kwargs):
		forum = ForumQuestion.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			userCreated = ForumQuestion.objects.filter(user=self.request.user)
		else:
			userCreated = ""
		template_name = "frontpages/forums/forum_edit.html"
		context = {'forum':forum,'usercreated':userCreated}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ForumQuestionForm(self.request.POST,self.request.FILES)
		userCreated = ForumQuestion.objects.filter(user=self.request.user)
		template_name = "frontpages/forums/forum_edit.html"
		context = {'forum':form,'usercreated':userCreated}
		if form.is_valid():
			forum = ForumQuestion.objects.get(id=self.kwargs['id'])
			forum.title = form.cleaned_data.get('title')
			forum.description = form.cleaned_data.get('description')
			if forum.attachements:
				forum.attachements = self.request.POST['attachements']
			forum.save() 
			return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
		return render(self.request, template_name,context)

class SearchForum(View):
	def get(self,*args,**kwargs):
		return redirect(reverse("forum_list"))
	def post(self,*args,**kwargs):
		print("============")
		print(self.request.POST["search"])
		forum = ForumQuestion.objects.filter(title__contains=self.request.POST['search'])
		template_name = "frontpages/forums/forum_list.html"
		if str(self.request.user) != "AnonymousUser":
			userCreated = ForumQuestion.objects.filter(user=self.request.user)
		else:
			userCreated = ""
		context = {'forums':forum,'usercreated':userCreated}
		return render(self.request, template_name,context)

class ForumQuestionsDetail(View):
	def get(self,*args,**kwargs):
		forum = ForumQuestion.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			userCreated = ForumQuestion.objects.filter(user=self.request.user)
		else:
			userCreated = ""
		comment = CommentForm()
		commentreplay=CommentReplayForm()
		print("-----0--------")
		print(self.request.user)
		template_name = "frontpages/forums/forum_detail.html"
		context = {'forum':forum,'commentForm':comment,'commentreplay':commentreplay,'usercreated':userCreated}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = CommentForm(self.request.POST,self.request.FILES)
		if form.is_valid():
			forum = ForumComments()
			forum = form.save(commit=False)
			question = ForumQuestion.objects.get(id=self.kwargs['id'])
			forum.forum_question = question
			print(form.cleaned_data.get('attachements'))
			if form.cleaned_data.get('attachements'):
				forum.attachements = form.cleaned_data.get('attachements')
			forum.user = self.request.user
			print("Force - x")
			print(str(form.cleaned_data.get('attachements')))
			forum.save()
			return redirect(reverse("forum_detail",kwargs={'id':question.id}))
		return render(self.request, template_name,context)