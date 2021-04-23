
from django.urls import reverse
import datetime
from django.views import View
from django.utils import timezone


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

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.http import FileResponse, HttpResponse

from accounts.models import User
from accounts.email_messages import sendEventNotification

from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm, NewsForm
from django.http import HttpResponse, FileResponse
						 
from wsgiref.util import FileWrapper
from django.utils import timezone


from collaborations.forms import BlogsForm,BlogsEdit, BlogCommentForm, FaqsForm, VacancyForm,JobCategoryForm, TenderApplicantForm

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from collaborations.views import SearchByTitle_All, models, get_paginated_data
from collaborations.forms import (BlogsForm, BlogCommentForm, FaqsForm,
								 VacancyForm,JobCategoryForm,
								 ForumQuestionForm,CommentForm,CommentReplayForm,
								 AnnouncementForm,ResearchForm,
								 ResearchProjectCategoryForm)

from collaborations.models import ( Blog, BlogComment,Faqs,
									Vacancy,JobApplication, JobCategory,
									ForumQuestion, ForumComments, CommentReplay,
									Announcement,AnnouncementImages,
									Research,
									ResearchProjectCategory)

from collaborations.forms import (ForumQuestionForm,CommentForm,CommentReplayForm)

from collaborations.models import ( ForumQuestion, ForumComments,
									CommentReplay)

from admin_site.decorators import company_created,company_is_active

decorators = [never_cache, company_created(),company_is_active()]

@method_decorator(decorators,name='dispatch')
class ListForumQuestionAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = ForumQuestion.objects.all()
		template_name = "admin/forum/Forumquestions/list.html"
		context = {'researchprojectcategorys':form}
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
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
			forum.created_by = self.request.user
			forum.save()
			messages.success(self.request, "Added New Forum Successfully")
			return redirect("admin:forum_form")
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
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
			forum = ForumQuestion.objects.get(id=self.kwargs['id'])
			forum.title=form.cleaned_data.get('title')
			forum.description=form.cleaned_data.get('description')
			if form.cleaned_data.get("attachements"):
				forum.attachements = form.cleaned_data.get("attachements")
			#research.user = self.request.user 
			forum.last_updated_by = self.request.user
			forum.last_updated_date = timezone.now()
			forum.save()
			messages.success(self.request, "Edited a Forum Successfully")
			return redirect("admin:forum_list")
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class ListForumCommentAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = ForumComments.objects.all()
		template_name = "admin/forum/ForumComments/list.html"
		context = {'researchprojectcategorys':form}
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class ListForumCommentByIdAdmin(LoginRequiredMixin ,View): 
	def get(self,*args,**kwargs):
		form = ForumComments.objects.filter(forum_question=self.kwargs['id'])
		template_name = "admin/forum/ForumComments/list.html"
		context = {'researchprojectcategorys':form}
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class ListCommentReplayByIdAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = CommentReplay.objects.filter(comment=self.kwargs['id'])
		template_name = "admin/forum/CommentReplay/list.html"
		context = {'researchprojectcategorys':form}
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
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
			forumcommnent = ForumComments.objects.get(id=self.kwargs['id'])
			forumcommnent.comment=form.cleaned_data.get('comment')
			forumcommnent.last_updated_by = self.request.user
			forumcommnent.last_updated_date = timezone.now()
			forumcommnent.save()
			messages.success(self.request, "Edited a Forum Comment Successfully")
			return redirect("admin:forum_comment_list")
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
class ListCommentReplayAdmin(LoginRequiredMixin ,View):
	def get(self,*args,**kwargs):
		form = CommentReplay.objects.all()
		template_name = "admin/forum/CommentReplay/list.html"
		context = {'researchprojectcategorys':form}
		return render(self.request, template_name,context)

@method_decorator(decorators,name='dispatch')
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
			commentreplay = CommentReplay.objects.get(id=self.kwargs['id'])
			commentreplay.content=form.cleaned_data.get('content')
			commentreplay.last_updated_by = self.request.user
			commentreplay.last_updated_date = timezone.now()
			commentreplay.save()
			messages.success(self.request, "Edited a Forum Comment Successfully")
			return redirect("admin:comment_replay_list")
		return render(self.request, template_name,context)


class EditCommentForum(LoginRequiredMixin,View):
	def post(self,*args,**kwargs):
		if(self.kwargs['type']=="ForumComments"):
			forum = CommentForm(self.request.POST,self.request.FILES)
			comment = ForumComments.objects.get(id=self.kwargs['id'])
			comment.comment =  self.request.POST.get("content")
			comment.save()
			return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
		if(self.kwargs['type']=="CommentReplay"):
			forum = CommentReplayForm(self.request.POST,self.request.FILES)
			comment = CommentReplay.objects.get(id=self.kwargs['id'])
			comment.content =  self.request.POST.get("content")
			comment.last_updated_by = self.request.user
			comment.last_updated_date = timezone.now()
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
			form.created_by = self.request.user
			form.save()
			return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
		template_name = "frontpages/forums/forum_detail.html"
		return render(self.request, template_name,context)

#----- create forum quesion
class CreateForumQuestion(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        forum = ForumQuestionForm()
        template_name="frontpages/forums/forums_form.html" 
        userCreated = ForumQuestion.objects.filter(created_by=self.request.user)
        context = {'form':forum,'usercreated':userCreated}
        return render(self.request,template_name,context)
    def post(self,*args,**kwargs):
        form = ForumQuestionForm(self.request.POST,self.request.FILES)
        userCreated = ForumQuestion.objects.filter(created_by=self.request.user)
        context = {'form':form,'usercreated':userCreated}
        template_name="frontpages/forums/forums_form.html" 
        if form.is_valid():
            forum = ForumQuestion()
            forum = form.save(commit=False)
            forum.created_by = self.request.user
            print("one")
            forum.save()
            forum = ForumQuestionForm()
            context={'form':forum}
            return redirect("forum_list")
        return render(self.request, template_name,context)

class ListForumQuestions(View):
	def get(self,*args,**kwargs):
		if not self.request.user.is_anonymous:
			userCreated = ForumQuestion.objects.filter(created_by=self.request.user)
		else:
			userCreated = ""
		if 'by_title' in self.request.GET:
			query = ForumQuestion.objects.filter(title__icontains = self.request.GET['by_title'])
			if query.count() > 0:
				result = {'query':query, 'message':f'{query.count()} result found!', 'message_am':f'{query.count()} ውጤቶች ተገኝተዋል' }
			else:
				result = {'query':ForumQuestion.objects.all()[:5], 'message':'No result found! Other Forums', 'message_am':'ምንም ውጤት አልተገኘም, ሌሎች ውጤቶች' }
		else:
			result = {'query':ForumQuestion.objects.all()[:5], 'message':'Forums', 'message_am':'ውይይቶች' }
		
		data = get_paginated_data(self.request, result['query'])
		template_name = "frontpages/forums/forum_list.html"
		context = {'forums': data,'usercreated':userCreated, 'message':result['message'], 'message_am':result['message_am']}
		return render(self.request, template_name, context)

class EditForumQuestions(View):
	def get(self,*args,**kwargs):
		forum = ForumQuestion.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			userCreated = ForumQuestion.objects.filter(created_by=self.request.user)
		else:
			userCreated = ""
		template_name = "frontpages/forums/forum_edit.html"
		context = {'forum':forum,'usercreated':userCreated}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = ForumQuestionForm(self.request.POST,self.request.FILES)
		userCreated = ForumQuestion.objects.filter(created_by=self.request.user)
		template_name = "frontpages/forums/forum_edit.html"
		context = {'forum':form,'usercreated':userCreated}
		if form.is_valid():
			forum = ForumQuestion.objects.get(id=self.kwargs['id'])
			forum.title = form.cleaned_data.get('title')
			forum.description = form.cleaned_data.get('description')
			forum.last_updated_by = self.request.user
			forum.last_updated_date = timezone.now()
			forum.save() 
			return redirect(reverse("forum_detail",kwargs={'id':self.kwargs['id']}))
		return render(self.request, template_name,context)

class SearchForum(View):
	def get(self,*args,**kwargs):
		return redirect(reverse("forum_list"))
	def post(self,*args,**kwargs):
		forum = ForumQuestion.objects.filter(title__contains=self.request.POST['search'])
		template_name = "frontpages/forums/forum_list.html"
		if str(self.request.user) != "AnonymousUser":
			userCreated = ForumQuestion.objects.filter(created_by=self.request.user)
		else:
			userCreated = ""
		context = {'forums':forum,'usercreated':userCreated}
		return render(self.request, template_name,context)

class ForumQuestionsDetail(View):
	def get(self,*args,**kwargs):
		forum = ForumQuestion.objects.get(id=self.kwargs['id'])
		if str(self.request.user) != "AnonymousUser":
			userCreated = ForumQuestion.objects.filter(created_by=self.request.user)
		else:
			userCreated = ""
		comment = CommentForm()
		commentreplay=CommentReplayForm()
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
			forum.created_by = self.request.user
			forum.last_updated_date = timezone.now()
			forum.save()
			return redirect(reverse("forum_detail",kwargs={'id':question.id}))
		return render(self.request, template_name,context)