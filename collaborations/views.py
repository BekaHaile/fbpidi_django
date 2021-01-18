from collaborations.models import Blog, BlogComment
from collaborations.forms import CreateBlogComment
from collaborations.forms import CreateFaqs
from collaborations.models import Faqs, Vacancy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import PollsQuestion, Choices, PollsResult, JobApplication, JobCategoty
from .forms import PollsForm, CreateJobApplicationForm
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

#apply to a job
class CreateApplication(View):

    def get(self,*args,**kwargs):
        vacancy=Vacancy.objects.get(id=self.kwargs['id'] ,closed=False)
        job = CreateJobApplicationForm()
        jobcategory = JobCategoty.objects.all()
        template_name="frontpages/job_apply.html"
        context={'job':job,'vacancy':vacancy,'category':jobcategory}
        return render(self.request, template_name,context) 

    def post(self,*args,**kwargs):
        form = CreateJobApplicationForm(self.request.POST,self.request.FILES)

        if form.is_valid():
            job=JobApplication(vacancy=Vacancy.objects.get(id=self.kwargs['id']),
                user=self.request.user,
                status=self.request.POST['status'],
                bio = self.request.POST['bio'],
                documents=form.cleaned_data.get("documents"),
                cv=form.cleaned_data.get("cv"))
            job.save()
            return redirect("vacancy")

class CategoryBasedSearch(View):
    def get(self,*args,**kwargs):
        vacancy = Vacancy.objects.filter(category=self.kwargs['id'],closed=False) 
        cateory = JobCategoty.objects.get(id=self.kwargs['id'])
        jobcategory = JobCategoty.objects.all()
        template_name="frontpages/vacancy_list.html"
        context = {'vacancys':vacancy,'category':jobcategory,'message':'Vacancies on '+str(cateory)}
        return render(self.request, template_name,context)

class VacancyList(View):
    def get(self,*args,**kwargs):
        vacancy = Vacancy.objects.filter(closed=False)
        jobcategory = JobCategoty.objects.all()
        template_name="frontpages/vacancy_list.html"
        context = {'vacancys':vacancy,'category':jobcategory,'message':'All Vacancys '}
        return render(self.request, template_name,context)


#blog-grid-right 
class BlogList(View):

    def get(self,*args,**kwargs):
        blog = Blog.objects.filter(publish=True) 
        template_name="frontpages/blog-grid-right.html"
        context={'blogs':blog}
        return render(self.request, template_name,context)




class BlogDetail(View):

	def get(self,*args,**kwargs):
		blog = Blog.objects.get(id=self.kwargs['id'])
		comment = CreateBlogComment()
		template_name="frontpages/blog-details-right.html" 
		context = {'blog':blog,'comment':comment}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = CreateBlogComment(self.request.POST)
		blog = Blog.objects.get(id=self.kwargs['id'])
		template_name="frontpages/blog-details-right.html" 
		if form.is_valid():
			blogComment=BlogComment(blog=blog,
				sender=self.request.user,
				content=self.request.POST['content'])
			blogComment.save()
			comment = CreateBlogComment()
			context = {'blog':blog,'comment':comment}
			return render(self.request, template_name,context)


class FaqList(View):
	def get(self,*args,**kwargs):
		template_name="frontpages/faq.html"
		faq = Faqs.objects.all()
		context = {'faqs':faq}
		return render(self.request, template_name,context)


class PollIndex(View):
    def get(self, *args, **kwargs):
        context = {}
        polls = PollsQuestion.objects.all()
        context={'polls':polls}
        return render(self.request, "frontpages/polls-list.html", context)

       

#only visible to logged in and never voted before
class PollDetail(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        message = ""
        context = {}        
        if self.kwargs['id'] :
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id']  )
                context ['poll'] = poll
                if poll.pollsresult_set.filter(user = self.request.user).count() > 0:
                    context ['has_voted'] = True

                return render(self.request, "frontpages/poll_detail.html", context)

            except Exception as e:
                print ("444444444444444444444444" ,str(e))
                messages.error(self.request, "Poll not found")
                return redirect("polls") 

        else:
            messages.error(self.request, "Nothing selected!")
            return redirect("polls")

    def post(self,*args,**kwargs):
        if self.kwargs['id'] and self.request.POST['selected_choice']: 
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id'] )

                # if the creator tries to vote, redirect to poll list
                # if poll.user == self.request.user:
                #     messages.error(self.request, "You can not vote on this poll, since you are the creator of the poll!")
                #     return redirect("polls") 
                
                # # #if the user already voted on this poll, redirect to poll list
                # if PollsResult.objects.filter(poll=poll, user = self.request.user):
                #     messages.error(self.request, "You have already voted for on poll!")
                #     return redirect("polls") 
                
                vote = PollsResult(
                    poll = poll,
                    user = self.request.user,
                    choice = Choices.objects.get(id = self.request.POST['selected_choice']),
                    remark=self.request.POST['remark']
                )

                vote.save()
                messages.success(self.request, "Successfully voted!")
                return redirect("polls") 

            except Exception as e:
                messages.error(self.request, "Poll not found!")
                return redirect("polls") 
             
                
        messages.error(self.request, "Invalid Vote!")        
        return redirect("polls")
        
