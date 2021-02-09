
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse

from django.shortcuts import render, redirect, reverse

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