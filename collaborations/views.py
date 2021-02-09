
from django.urls import reverse
import datetime

from django.http import HttpResponse, FileResponse
from collaborations.models import Blog, BlogComment
from collaborations.forms import FaqsForm
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from collaborations.models import Faqs, Vacancy, Blog, BlogComment, Blog, BlogComment, JobApplication, JobCategoty, News, NewsImages
                                     #redirect with context
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import PollsQuestion, Choices, PollsResult, Tender, TenderApplicant
from .forms import PollsForm, TenderForm, TenderEditForm, CreateJobApplicationForm
from django.contrib import messages

from company.models import Company, CompanyBankAccount, Bank, CompanyStaff, CompanyEvent, EventParticipants
from accounts.models import User, CompanyAdmin, Company
import os

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.http import FileResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from accounts.email_messages import sendEventNotification

from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm, NewsForm
from django.http import HttpResponse, FileResponse
                         
from wsgiref.util import FileWrapper



from collaborations.forms import BlogsForm, BlogCommentForm, FaqsForm, VacancyForm,JobCategoryForm, TenderApplicantForm

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from collaborations.forms import (BlogsForm, BlogCommentForm, FaqsForm,
                                 VacancyForm,JobCategoryForm,
                                 ForumQuestionForm,CommentForm,CommentReplayForm,
                                 AnnouncementForm)

from collaborations.models import ( Blog, BlogComment,Faqs,
                                    Vacancy,JobApplication, JobCategoty,
                                    ForumQuestion, ForumComments, CommentReplay,
                                    Announcement,AnnouncementImages,
                                    )

from company.forms import EventParticipantForm




# --------------- Announcement
class ListAnnouncement(View):
    def get(self,*args,**kwargs):
        form = Announcement.objects.all()
        template_name="frontpages/announcement/announcement_list.html"
        context={'Announcements':form}
        return render(self.request, template_name,context)

class AnnouncementDetail(View):
    def get(self,*args,**kwargs):
        form = Announcement.objects.get(id=self.kwargs['id'])
        template_name="admin/announcement/announcement_detail.html"
        context={'form':form}
        return render(self.request, template_name,context)
    def post(self,*agrs,**kwargs):
        form = AnnouncementForm(self.request.POST)
        post = Announcement.objects.get(id=self.kwargs['id'])
        context={'form':form}
        template_name="admin/announcement/announcement_detail.html"
        if form.is_valid():
            post.title = form.cleaned_data.get('title')
            post.title_am = form.cleaned_data.get('title_am')
            post.containt = form.cleaned_data.get('containt')
            post.containt_am = form.cleaned_data.get('containt_am')
            post.save()
            print("----- | ----")
            print(self.request.FILES.getlist('images'))
            for images in self.request.FILES.getlist('images'):
                print("image name:"+str(images.name))
                announcementimages= AnnouncementImages()
                announcementimages.announcement = post
                announcementimages.image = images
                announcementimages.save()

            messages.success(self.request, "Edited Announcement Successfully")
            return redirect("admin:anounce_list")
        return render(self.request, template_name,context)


class ListAnnouncementAdmin(View):
    def get(self,*args,**kwargs):
        form = Announcement.objects.all()
        template_name="admin/announcement/announcement_list.html"
        context={'Announcements':form}
        return render(self.request, template_name,context)

class CreatAnnouncement(LoginRequiredMixin,View):
    def company_admin(self,*args,**kwarges):
        force = Company.objects.get(user=self.request.user)
        print("----------------"+str(force))
        return force
    
    def get(self,*args,**kwargs):
        try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                    
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = Company.objects.get(id = company_staff.company.id)
        except Exception as e:
                messages.warning(self.request, "Currently, You are not related with any registered Company.")
                print("Exception while trying to find the company of an company admin or company staff user in CreateNews ", str(e))
                return redirect("admin:create_company_profile")
       
        form = AnnouncementForm()
        template_name="admin/announcement/announcement_form.html"
        context={'form':form}
        return render(self.request, template_name,context)
    def post(self,*args,**kwargs):
        form = AnnouncementForm(self.request.POST,self.request.FILES)
        context={'form':form}
        template_name="admin/announcement/announcement_form.html"
        context={'form':form}
        print("----------")
        if form.is_valid():
            post = Announcement()
            post = form.save(commit=False)
            post.user = self.request.user  
            post.company = self.company_admin()                 
            post.save()
            for images in self.request.FILES.getlist('images'):
                print("image name:"+str(images.name))
                announcementimages= AnnouncementImages()
                announcementimages.announcement = post
                announcementimages.image = images
                announcementimages.save()


            announcementimages.image
            messages.success(self.request, "Added New Announcement Successfully")
            return redirect("admin:anounce_Create")
        return render(self.request, template_name,context)

#---------------- forum and comment on forum
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

class EditCommentForum(View):
    def post(self,*args,**kwargs):
        print("============") 
        print(self.request.POST["content"])
        if(self.kwargs['type']=="ForumComments"):
            comment = ForumComments.objects.get(id=self.kwargs['id'])
            comment.comment =  self.request.POST["content"]
            comment.save()
            return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
        if(self.kwargs['type']=="CommentReplay"):
            comment = CommentReplay.objects.get(id=self.kwargs['id'])
            comment.content =  self.request.POST["content"]
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
            form.user = self.request.user
            form.save()
            print("this worked")
            return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
        print("it didn't worked")
        template_name = "frontpages/forums/forum_detail.html"
        return render(self.request, template_name,context)

#----- create forum quesion
class CreateForumQuestion(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        forum = ForumQuestionForm()
        try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                    
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = Company.objects.get(id = company_staff.company.id)
        except Exception as e:
                messages.warning(self.request, "Currently, You are not related with any registered Company.")
                print("Exception while trying to find the company of an company admin or company staff user in CreateNews ", str(e))
                return redirect("admin:create_company_profile")

        template_name="frontpages/forums/forums_form.html" 
        userCreated = ForumQuestion.objects.filter(user=self.request.user)
        context = {'form':forum,'usercreated':userCreated}
        return render(self.request,template_name,context)
    def post(self,*args,**kwargs):
        form = ForumQuestionForm(self.request.POST,self.request.FILES)
        userCreated = ForumQuestion.objects.filter(user=self.request.user)
        context = {'form':forum,'usercreated':userCreated}
        template_name="frontpages/forums/forums_form.html" 
        if form.is_valid():
            forum = ForumQuestion()
            forum = form.save(commit=False)
            forum.user = self.request.user
            forum.attachements = form.cleaned_data.get("attachements")
            print("one")
            forum.save()
            forum = ForumQuestionForm()
            context={'form':forum}
            return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
        return render(self.request, template_name,context)

class ListForumQuestions(View):
    def get(self,*args,**kwargs):
        forum = ForumQuestion.objects.all()
        print("-------"+str(self.request.user))
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
            forum.attachements = self.request.POST['attachements']
            forum.save() 
            return redirect(reverse("forum_detail",kwargs={'id':str(self.kwargs['forum'])}))
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
            forum.user = self.request.user
            forum.save()
            return redirect(reverse("forum_detail",kwargs={'id':question.id}))
        return render(self.request, template_name,context)

## --- Blogs Views
class CreatBlog(LoginRequiredMixin,View):
    template_name="admin/pages/blog_form.html"
    def get(self,*args,**kwargs):
        form = BlogsForm()
        try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                    
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = Company.objects.get(id = company_staff.company.id)
        except Exception as e:
                messages.warning(self.request, "Currently, You are not related with any registered Company.")
                print("Exception while trying to find the company of an company admin or company staff user in CreateNews ", str(e))
                return redirect("admin:create_company_profile")
        template_name="admin/pages/blog_form.html"
        context={'form':form}
        return render(self.request, template_name,context)
    def post(self,*args,**kwargs):
        form = BlogsForm(self.request.POST,self.request.FILES)
        context={'form':form}
        if form.is_valid():
            blog = Blog()
            blog = form.save(commit=False)
            blog.user = self.request.user
            blog.blogImage = form.cleaned_data.get("blogImage")
            publish =self.request.POST['publish']
            print(str(publish))
            if publish =="on":
                blog.publish=True 
            else:
                blog.publish=False            
            blog.save()
            messages.success(self.request, "Added New Blog Successfully")
            form = BlogsForm()
            context={'form':form}
            return render(self.request, "admin/pages/blog_form.html",context)
        return render(self.request, "admin/pages/blog_form.html",context)

class AdminBlogList(LoginRequiredMixin,View):
    template_name="admin/pages/blog_list.html"
    def get(self,*args,**kwargs):
        blogs = Blog.objects.all()
        template_name="admin/pages/blog_list.html"
        context={'blogs':blogs}
        return render(self.request, template_name,context)
        
class BlogView(LoginRequiredMixin,View):
    template_name="admin/pages/blog_list.html"
    def get(self,*args,**kwargs):
        blogs = Blog.objects.get(id=self.kwargs['id'])
        template_name="admin/pages/blog_detail.html"
        context = {'form':blogs}
        return render(self.request, "admin/pages/blog_detail.html",context)
    def post(self,*args,**kwargs):
        form = BlogsForm(self.request.POST,self.request.FILES)
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

## --- Faqs views

class CreateFaqs(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                    
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = Company.objects.get(id = company_staff.company.id)
        except Exception as e:
                messages.warning(self.request, "Currently, You are not related with any registered Company.")
                print("Exception while trying to find the company of an company admin or company staff user in CreateNews ", str(e))
                return redirect("admin:create_company_profile")

        form = FaqsForm()
        context = {'form':form}
        return render(self.request,"admin/pages/faqs_forms.html",context)


    def post(self,*args,**kwargs):
        form = FaqsForm(self.request.POST)
        context = {"form":form}
        if form.is_valid():
            faqs = form.save(commit=False)
            faqs.save()
            form = FaqsForm()
            context = {'form':form}
            messages.success(self.request, "New Faqs Added Successfully")
            return redirect("admin:admin_Faqs")
        return render(self.request, "admin/pages/faqs_forms.html",context)

class FaqsView(LoginRequiredMixin,View):
    template_name="admin/pages/blog_list.html"
    def get(self,*args,**kwargs):
        faqs=Faqs.objects.get(id=self.kwargs['id'])
        template_name="admin/pages/faqs_detail.html"
        context={'faq':faqs}
        return render(self.request, template_name,context)
    def post(self,*args,**kwargs):
        form = FaqsForm(self.request.POST)
        if form.is_valid():
            faq = Faqs.objects.get(id=self.kwargs['id'])
            faq.questions = self.request.POST['questions']
            faq.questions_am = self.request.POST['questions_am']
            faq.answers = self.request.POST['answers']
            faq.answers_am = self.request.POST['answers_am']
            faq.save()
        messages.success(self.request, "Edited Faqs Successfully")
        return redirect("admin:admin_Faqs") 

class FaqsList(LoginRequiredMixin,View):
    template_name = "admin/pages/faqs_forms.html"
    def get(self,*args,**kwargs):
        faqs=Faqs.objects.all()
        context = {'faqs':faqs}
        template_name = "admin/pages/faqs_list.html"
        return render(self.request, template_name,context)

# -----  vacancy and jobCategory
class Download(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        obj = JobApplication.objects.get(id=self.kwargs['id'])
        if self.kwargs['name']=='cv':
            filename = obj.cv.path
        if self.kwargs['name']=='documents':
            filename = obj.documents.path
        if os.path.exists(filename):
            response = FileResponse(open(filename, 'rb'))
        else:
            message.error(self.request, "File does not exists")
            return redirect("admin:Applicant_info")
        return response

class CloseVacancy(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        vacancy=Vacancy.objects.get(id=self.kwargs['id'])
        status = self.kwargs['closed']
        print("============="+str(status))
        if status== "True":
            vacancy.closed = False
            print("iii")
            messages.success(self.request, "Vacancy Opened Successfully")
            vacancy.save()
            if self.request.user.is_superuser:
                return redirect("admin:super_Job_list")
        else:
            vacancy.closed = True
            print("lll")
            messages.success(self.request, "Vacancy Closed Successfully")    
            vacancy.save()
            if self.request.user.is_superuser:
                return redirect("admin:super_Job_list")
        
        return redirect("admin:Job_list")

class ApplicantList(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        vacancy=Vacancy.objects.filter(user=self.request.user)
        context = {'vacancy':vacancy}
        template_name = "admin/pages/vacancy_list.html"
        return render(self.request, template_name,context)

class Applicantinfo(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        jobapplicant=JobApplication.objects.filter(vacancy=self.kwargs['id']) 
        vacancyDetail = Vacancy.objects.get(id=self.kwargs['id'])
        context = {'jobapplicant':jobapplicant,'vacancy':self.kwargs['id'],'vacancyDetail':vacancyDetail}
        template_name = "admin/pages/applicant_list.html"
        return render(self.request, template_name,context)

class ApplicantListDetail(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        applicant=JobApplication.objects.get(id=self.kwargs['id'])
        context = {'applicant':applicant}
        template_name = "admin/pages/jobCategory_list.html"
        return render(self.request, template_name,context)

class JobCategoryList(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        jobCategoty=JobCategoty.objects.all()
        context = {'forms':jobCategoty}
        template_name = "admin/pages/jobCategory_list.html"
        return render(self.request, template_name,context)

class JobcategoryFormView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                    
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = Company.objects.get(id = company_staff.company.id)
        except Exception as e:
                messages.warning(self.request, "Currently, You are not related with any registered Company.")
                print("Exception while trying to find the company of an company admin or company staff user in CreateNews ", str(e))
                return redirect("admin:create_company_profile")
        form = JobCategoryForm()
        context = {'form':form}
        return render(self.request,"admin/pages/jobCategory_form.html",context)
    def post(self,*args,**kwargs):
        form = JobCategoryForm(self.request.POST)
        if form.is_valid():
            catagory = form.save(commit=False)
            catagory.save()
            messages.success(self.request, "New Job category Added Successfully")
            form = JobCategoryForm()
            context = {'form':form}
        return render(self.request,"admin/pages/jobCategory_form.html",context)

class JobCategoryDetail(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = JobCategoty.objects.get(id=self.kwargs['id'])
        #print(str(self.kwargs['id'])+"-----------------"+str(form.categoryName))
        context = {'form':form}
        return render(self.request,"admin/pages/jobCategory_detail.html",context)
    def post(self,*args,**kwarges):
        form = JobCategoryForm(self.request.POST)
        if form.is_valid():
            category = JobCategoty.objects.get(id=self.kwargs['id'])
            category.categoryName_am=self.request.POST['categoryName_am']
            category.categoryName = self.request.POST['categoryName']
            category.save()
            messages.success(self.request, "Job category Edited Successfully")
            form = JobCategoty()
            context = {'form':form}
            return redirect("admin:admin_jobcategoty")
        return render(self.request,"admin/pages/jobCategory_list.html",context)

class VacancyDetail(LoginRequiredMixin,View):
    def company_admin(self,*args,**kwarges):
        force = Company.objects.get(user=self.request.user)
        print("----------------"+str(force))
        return force
    def get(self,*args,**kwargs):
        form = Vacancy.objects.get(id=self.kwargs['id'])
        jobcategory = JobCategoty.objects.all()
        start=str(form.starting_date)
        start=start[:19]
        end=str(form.ending_date)
        end=end[:19]
        form.starting_date = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        form.ending_date =  datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        vacancy = VacancyForm() 
        #print(str(self.kwargs['id'])+"-----------------"+str(form.categoryName))
        context = {'form':form,'jobcategory':jobcategory,"vacancy":vacancy}
        return render(self.request,"admin/pages/job_detail.html",context)
    def post(self,*args,**kwarges):
        form = VacancyForm(self.request.POST,self.request.FILES)
        context = {'form':form}
        if form.is_valid():
            vacancy = Vacancy.objects.get(id=self.kwargs['id'])
            vacancy.user=self.request.user
            print("-----+++++-------"+str(form.cleaned_data.get('employement_type')))
            vacancy.company=self.company_admin()
            vacancy.location=form.cleaned_data.get('location')
            vacancy.salary=form.cleaned_data.get('salary')
            vacancy.job_title=form.cleaned_data.get('job_title')
            vacancy.description=form.cleaned_data.get('description')
            vacancy.requirement=form.cleaned_data.get('requirement')
            vacancy.job_title_am=form.cleaned_data.get('job_title_am')
            vacancy.description_am=form.cleaned_data.get('description_am')
            vacancy.requirement_am=form.cleaned_data.get('requirement_am')
            starting_date=datetime.datetime.strptime(self.request.POST['starting_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            ending_date=datetime.datetime.strptime(self.request.POST['ending_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            vacancy.starting_date = starting_date
            vacancy.ending_date = ending_date
            vacancy.category=form.cleaned_data.get('category')
            vacancy.employement_type=form.cleaned_data.get('employement_type')
            vacancy.save()
            
            messages.success(self.request, "Vacancy Edited Successfully")
            form = JobCategoty()
            context = {'form':form}
            return redirect("admin:Job_list")
        return render(self.request,"admin/pages/job_detail.html",context)

class SuperAdminVacancyList(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        vacancy=Vacancy.objects.all()
        context = {'vacancy':vacancy}
        template_name = "admin/pages/super_job_list.html"
        return render(self.request, template_name,context)

class AdminVacancyList(LoginRequiredMixin,View):
    
    def get(self,*args,**kwargs):
        vacancy=Vacancy.objects.filter(user=self.request.user)
        context = {'vacancy':vacancy}
        template_name = "admin/pages/job_list.html"
        return render(self.request, template_name,context)

## show form
class CreateVacancy(LoginRequiredMixin, View):
    def company_admin(self,*args,**kwarges):
        force = Company.objects.get(user=self.request.user)
        print("----------------"+str(force))
        return force

    def get(self,*args,**kwargs): 
        try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                    
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = Company.objects.get(id = company_staff.company.id)
        except Exception as e:
                messages.warning(self.request, "Currently, You are not related with any registered Company.")
                print("Exception while trying to find the company of an company admin or company staff user in CreateNews ", str(e))
                return redirect("admin:create_company_profile")
       
        vacancy = VacancyForm() 
        context = {'vacancy':vacancy}
        return render(self.request,"admin/pages/job_form.html",context)

    def post(self,*args,**kwargs):
        form = VacancyForm(self.request.POST,self.request.FILES)
        
        context = {'vacancy':form}
        template = "admin/pages/job_form.html"
        if form.is_valid():
            category = JobCategoty.objects.get(id=self.request.POST['category'],)
            print("======")
            print(self.request.POST['starting_date'])
            print("======")
            print(self.request.POST['ending_date'])
            vacancy=form.save(commit=False)
            vacancy.employement_type = form.cleaned_data.get('employement_type')
            vacancy.user=self.request.user
            vacancy.company=self.company_admin()
            vacancy.category=category
            starting_date=datetime.datetime.strptime(self.request.POST['starting_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            ending_date=datetime.datetime.strptime(self.request.POST['ending_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            vacancy.starting_date = starting_date
            vacancy.ending_date = ending_date
            vacancy.save()

            messages.success(self.request, "New vacancy Added Successfully")
            vacancy = VacancyForm()
            context = {'vacancy':vacancy}
        return render(self.request,"admin/pages/job_form.html",context)

#apply to a job
class CreateApplication(LoginRequiredMixin,View):

    def get(self,*args,**kwargs):
        vacancy=Vacancy.objects.get(id=self.kwargs['id'] ,closed=False)
        applicants=JobApplication.objects.filter(vacancy=vacancy.id)
        print("----------")
        for applicant in applicants:
            print(applicant.user)
        print("----------")
        print(self.request.user)
        for applicant in applicants:
            if(applicant.user == self.request.user):
                print("---vacancy---")
                messages.warning(self.request, "You can't apply to the same vacancy Twice")
                return redirect("vacancy")
                
        job = CreateJobApplicationForm()
        jobcategory = JobCategoty.objects.all()
        template_name="frontpages/job_apply.html"
        context={'job':job,'vacancy':vacancy,'category':jobcategory}
        return render(self.request, template_name,context) 

    def post(self,*args,**kwargs):
        form = CreateJobApplicationForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            job=form.save(commit=False)
            job.user=self.request.user
            job.vacancy = Vacancy.objects.get(id=self.kwargs['id'])
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

class VacancyMoreDetail(View):
    def get(self,*args,**kwargs):
        vac = Vacancy.objects.get(id=self.kwargs['id'],closed=False)
        jobcategory = JobCategoty.objects.all()
        template_name="frontpages/vacancy_detail.html"
        context = {'vacancy':vac,'category':jobcategory,'message':'Vacancy Detail'}
        return render(self.request, template_name,context)



#blog-grid-right 
class BlogList(View):

    def get(self,*args,**kwargs):
        blog = Blog.objects.filter(publish=True) 
        template_name="frontpages/blog-grid-right.html"
        context={'blogs':blog}
        return render(self.request, template_name,context)


class CreateComment(LoginRequiredMixin,View):
	def post(self,*args,**kwargs):
		form = BlogCommentForm(self.request.POST)
		blog = Blog.objects.get(id=self.kwargs['id'])
		template_name="frontpages/blog-details-right.html" 
		if form.is_valid():
			blogComment=BlogComment(blog=blog,sender=self.request.user,content=form.cleaned_data.get('content'))
			blogComment.save()
			comment = BlogCommentForm()
			context = {'blog':blog,'comment':comment}
			return render(self.request, template_name,context)

class BlogDetail(View):

	def get(self,*args,**kwargs):
		blog = Blog.objects.get(id=self.kwargs['id'])
		comment = BlogCommentForm()
		template_name="frontpages/blog-details-right.html" 
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
                messages.warning(self.request, "Poll not found")
                return redirect("polls") 

        else:
            messages.warning(self.request, "Nothing selected!")
            return redirect("polls")

    def post(self,*args,**kwargs):
        if self.kwargs['id'] and self.request.POST['selected_choice']: 
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
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
                messages.warning(self.request, "Poll not found!")
                return redirect("polls") 
             
        messages.warning(self.request, "Invalid Vote!")        
        return redirect("polls")
        

########## tender related views
class CreateTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:    
            form = TenderForm()
            try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                    
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = Company.objects.get(id = company_staff.company.id)
            except Exception as e:
                messages.warning(self.request, "Currently, You are not related with any registered Company.")
                print("Exception while trying to find the company of an company admin or company staff user in createTender ", str(e))
                return redirect("admin:create_company_profile")
            company_bank_accounts = company.get_bank_accounts()
            context = {'form':form, 'company_bank_accounts':company_bank_accounts}
            return render(self.request,'admin/collaborations/create_tender.html',context)
        except Exception as e: 
            print("execption at createtender ", str(e))
            return redirect("admin:index")
    
    def post(self,*args,**kwargs):
        form = TenderForm(self.request.POST)  
        try:                 
            if form.is_valid():
                tender = form.save(commit=False)
                user = None
                tender.user = self.request.user
                if  self.request.FILES['document']:
                    tender.document = self.request.FILES['document']

                if self.request.POST['tender_type'] == "Paid":
                    tender.document_price = self.request.POST['document_price']
                else:
                    tender.document_price = 0

                starting_date=datetime.datetime.strptime(self.request.POST['start_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                ending_date=datetime.datetime.strptime(self.request.POST['end_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                tender.start_date = starting_date
                tender.end_date = ending_date
                tender.save()
                tender.bank_account.add(self.request.POST['company_bank_account'])
                
                messages.success(self.request,"Tender Successfully Created")
                return redirect("admin:tenders")
                
            else:
                print(form.errors)
                messages.warning(self.request, "Error! Tender was not Created!" )
                return redirect("admin:tenders")
                
        except Exception as e:
            print("Exception at collaborations.views.CreateTender post" , str (e))
            return redirect("admin:tenders")

def check_tender_enddate(request, tenders):
    # now = datetime.datetime.now()
    for tender in tenders:
        endstr = str(tender.end_date.date)
        if tender.end_date.day < datetime.datetime.now().day and tender.status == "Open":
            # if tender.end_date.time() <= datetime.datetime.now().time():
                    tender.status = "Closed"
                    tender.save()
                    sendTenderClosedEmailNotification(request, tender.user, tender)
    return tenders

class TenderList(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
                  
        try:    
            if self.request.user.is_superuser:
                tenders = Tender.objects.all()
                tenders = check_tender_enddate(self.request, tenders)       
                return render(self.request, "admin/collaborations/tenders.html", {'tenders':tenders,})

            else:
                tenders = Tender.objects.filter(user = self.request.user)
                if not tenders:
                    messages.warning(self.request, "You have no tenders to control!!")
                    return render(self.request, "admin/collaborations/tenders.html")

                tenders = check_tender_enddate(self.request, tenders)       
                return render(self.request, "admin/collaborations/tenders.html", {'tenders':tenders,})
        except Exception as e:
                messages.warning(self.request, "Error while getting tenders",)
                print(str(e))
                return redirect("admin:index") 


class TenderDetail(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):         
        form = TenderForm()
        if self.kwargs['id']:
            try:
                tender = Tender.objects.get(id =self.kwargs['id'] )
                company = tender.get_company()
                company_bank_accounts = company.get_bank_accounts()
                context = {'form':form, 'company_bank_accounts':company_bank_accounts, 'tender':tender}
                return render(self.request,'admin/collaborations/tender_detail.html',context)
            except Exception as e:
                print("tender error", str(e))
                messages.warning(self.request,"Tender edit error")
                return redirect("admin:tenders")

        print("error at tenderDetail for admin")
        return redirect("admin:admin_polls")


class ManageBankAccount(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        tender = Tender.objects.get(id =self.kwargs['id'])
        if tender:
            if self.kwargs['option'] == 'remove':
                tender.bank_account.remove( CompanyBankAccount.objects.get(id = self.request.POST['remove_bank_account']) )
            else:
                tender.bank_account.add( CompanyBankAccount.objects.get(id = self.request.POST['relate_bank_account']) )
            tender.save()
            print(tender.bank_account.all())
            return redirect(f"/admin/edit_tender/{self.kwargs['id']} ")
        messages.warning(self.request, "Error while Managing Bank Account!")
        return redirect("admin:tenders")


class EditTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        
        form = TenderEditForm()
        context = {}
        tender = Tender.objects.get(id =self.kwargs['id'] )
        company = tender.get_company()

        if company:
            company_bank_accounts = company.get_bank_accounts()
            
            start_date =str(tender.start_date)
            start_date =start_date[:19]
            end_date =str(tender.end_date)
            end_date = end_date[:19]
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            banks= Bank.objects.all() # if there will be a scenario where the admin needs to add register new bank account
            context = {'form':form, 'banks':banks, 'company_bank_accounts':company_bank_accounts, 'start_date':start_date, 'end_date': end_date}
            if self.kwargs['id']:   
                    context['tender'] = tender 
                    context['edit'] = True
                    return render(self.request,'admin/collaborations/create_tender.html',context)
              
        else:
            print ("no company")

        return render(self.request,'admin/collaborations/create_tender.html',{})

    def post(self,*args,**kwargs):  
        form = TenderEditForm(self.request.POST)                       
        if form.is_valid():
            try:
                tender= Tender.objects.get(id = self.kwargs['id'])
                message = []             
                starting_date=datetime.datetime.strptime(self.request.POST['start_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                ending_date=datetime.datetime.strptime(self.request.POST['end_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                tender.start_date = starting_date
                tender.end_date = ending_date
                tender.title = self.request.POST['title']
                tender.title_am = self.request.POST['title_am']
                tender.description = self.request.POST['description']
                tender.description_am = self.request.POST['description_am']
                tender.tender_type = self.request.POST['tender_type']
                if self.request.POST["tender_type"] == "Free":
                    tender.document_price = 0
                else:
                    tender.document_price = self.request.POST["document_price"]
                tender.status = self.request.POST["status"]
                if self.request.FILES:
                    tender.document = self.request.FILES['document'] 
                tender.save()

            except Exception as e:
                print("There is an Exception while tying to edit a tender!")   
            
            messages.success(self.request,"Tender Successfully Edited")
            return redirect("admin:tenders") 
                
        else:
                import pprint
                print("Form is not valid")
                pprint.pprint(self.request.POST)
                print("2")
                pprint.pprint(self.request.FILES)
                print(form.errors)
                messages.warning(self.request, "Error! Tender was not Edited!" )
                return redirect("admin:tenders")


class DeleteTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['id'] :
            tender = Tender.objects.filter(id = self.kwargs['id']  )
            if tender:
                tender.delete()
                message = "Tender Deleted Successfully"
                messages.success(self.request,message)
                return redirect("admin:tenders")
            else:
                messages.warning(self.request, "NO such tender was found!")
                return redirect("admin:tenders")


        else:
            messages.warning(self.request, "Nothing selected!")
            return redirect("admin:tenders")


######## Tender for customers
class CustomerTenderList(View):
    def get(self, *args, **kwargs):          
        try:
                tenders = Tender.objects.all()
                # tenders = check_tender_enddate(self.request, tenders)
                return render(self.request, "frontpages/tender/customer_tender_list.html", {'tenders':tenders,})
        except Exception as e:
                messages.warning(self.request, "Error while getting tenders")
                return redirect("tender_list")     


class CustomerTenderDetail(View):
    def get(self, *args, **kwargs):  
        
        if self.kwargs['id'] :
            try:
                tender = Tender.objects.get(id = self.kwargs['id']  )
                applicant_form = TenderApplicantForm()
                return render(self.request, "frontpages/tender/customer_tender_detail.html", {'tender':tender, 'applicant_form':applicant_form})

            except Exception as e:
                print("Exception at customerTenderDetail :", str(e))
                messages.warning(self.request, "tender not found")
                return redirect("tender_list") 

        else:

            messages.warning(self.request, "Nothing selected!")
            return redirect("tender_list")

class ApplyForTender(View):
    def post(self, *args, **kwargs):   
 
        tender = Tender.objects.get(id = self.kwargs['id'])
        if tender:
            applicant = TenderApplicant(
                first_name = self.request.POST['first_name'], 
                last_name = self.request.POST['last_name'],
                email = self.request.POST['email'],
                phone_number = self.request.POST['phone_number'],
                company_name = self.request.POST['company_name'],
                company_tin_number=self.request.POST['company_tin_number'],
                tender = tender
            )
            applicant.save()
            messages.success(self.request, "Application Successfully Completed")
            print("Created successfully") 
            return render(self.request, "frontpages/tender/customer_tender_detail.html", {'tender':tender, 'applied':True})

            return redirect(f"{tender.document.url}")
            # return redirect("/collaborations/tender_list/")

          
        print("Error Occured!")
        messages.warning(self.request,"Error while Applying!")
        return redirect("/collaborations/tender_list/")

def pdf_download(request, id):
    tender = Tender.objects.get(id = id)
    path = tender.document.path
    print(path)
    f = open(path, "r")
    response = HttpResponse(FileWrapper(f), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=resume.pdf'
    f.close()
    return response


##### News

class CreateNews(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                    
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = Company.objects.get(id = company_staff.company.id)
        except Exception as e:
                messages.warning(self.request, "Currently, You are not related with any registered Company.")
                print("Exception while trying to find the company of an company admin or company staff user in CreateNews ", str(e))
                return redirect("admin:create_company_profile")

        form = NewsForm()    
        context = {'form':form,}
        return render(self.request,'admin/collaborations/create_news.html',context)
        return redirect("admin:news_list")
    
    def post(self, *args, **kwargs):
        form = NewsForm( self.request.POST) 
        if form.is_valid:
            news = form.save(commit=False)
            news.user = self.request.user
            news.save()
        
            for image in self.request.FILES.getlist('images'):
                print ("saving ", image.name)
                imag = NewsImages(news=news, name = image.name, image = image)
                imag.save()
            messages.success(self.request, "News Created Successfully!")
            return redirect("admin:news_list") 
        else:
            messages.warning(self.request, "Error! News not Created!")

class EditNews(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:   
            print("in the try")
            if self.kwargs['id']:
                print("in the if method", self.kwargs['id'])
                news = News.objects.get(id =  self.kwargs['id'])
                return render(self.request,'admin/collaborations/create_news.html',{'news':news, 'edit':True})
        except Exception as e: 
            print("execption at create News ", str(e))
            messages.warning(self.request,"Error, Could Not Find the News! ")
            return redirect("admin:index")
        
    def post(self, *args, **kwargs):
        if self.kwargs['id']:
            form = NewsForm(self.request.POST) 
            news = News.objects.filter(id = self.kwargs['id']).first()
            if form.is_valid:
                news.title = self.request.POST['title']
                news.title_am = self.request.POST['title_am']
                news.description = self.request.POST['description']
                news.description_am = self.request.POST['description_am']
                news.save()

                if self.request.FILES:
                    for image in self.request.FILES.getlist('images'):
                        print ("saving new images", image.name)
                        imag = NewsImages(news=news, name = image.name, image = image)
                        imag.save()
                messages.success(self.request, "News Edited Successfully!")
                return redirect(f"/admin/news_detail/{news.id}/") 
            else:
                messages.warning(self.request, "Error! News not Edited!")

class AdminNewsList(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        newslist = News.objects.all()
        return render(self.request, "admin/collaborations/admin_news_list.html", {'newslist':newslist})

class NewsDetail(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):         
        form = TenderForm()
        if self.kwargs['id']:
            try:
                news = News.objects.get(id =self.kwargs['id'] )
                context = {'form':form, 'news':news }
                return render(self.request,'admin/collaborations/news_detail.html',context)
            except Exception as e:
                print(str(e))
                return redirect("admin:news_list")
        print("error at newsDetail for admin")
        return redirect("admin:news_list")


##### News, Customer
class CustomerNewsList(View):
    def get(self, *args, **kwargs):          
        try:
                news_list = News.objects.all()

                return render(self.request, "frontpages/news/customer_news_list.html", {'news_list':news_list,'NEWS_CATAGORY':News.NEWS_CATAGORY})
        except Exception as e:
                return redirect("index")     

class CustomerNewsDetail(View):
    def get(self, *args, **kwargs):        
        if self.kwargs['id'] :
            news = News.objects.get(id = self.kwargs['id']  )
            return render(self.request, "frontpages/news/customer_news_detail.html", {'news':news,})
        else:
            return redirect("index")

##### Customer Events
def check_event_participation(request, event_participants):
    today = datetime.datetime.now().day
    for participant in event_participants:   
        start_day = participant.event.start_date.day
        if start_day > today and start_day - today == participant.notifiy_in:
            sendEventNotification(request, participant) 
    return True


class CustomerEventList(View):
    def get(self, *args, **kwargs):          
        try:
                events = CompanyEvent.objects.all()
                event_participants = EventParticipants.objects.filter(notified = False)   
                check_event_participation(self.request, event_participants)
                return render(self.request, "frontpages/news/customer_event_list.html", {'events':events,})
        except Exception as e:
                return redirect("index")     

class CustomerEventDetail(View):
    def get(self, *args, **kwargs):        
        if self.kwargs['id'] :
            event_participant_form = EventParticipantForm
            event = CompanyEvent.objects.get(id = self.kwargs['id']  )
            return render(self.request, "frontpages/news/customer_event_detail.html", {'event':event,'event_participant_form':event_participant_form})
        else:
            return redirect("index")

class EventParticipation(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):   
        event = CompanyEvent.objects.get(id = self.kwargs['id'])
        if event:
            applicant = EventParticipants(user = self.request.user, event = event, notified=False)
            applicant.patricipant_email = self.request.POST['patricipant_email']
            
            if self.request.POST['notify_in']:
                applicant.notifiy_in = self.request.POST['notify_in']
            else:
                applicant.notifiy_in = 1   
                    
            applicant.save()
            messages.success(self.request, "Successfully Completed")
            print("Created successfully") 
            return redirect("/collaborations/customer_event_list/")

        print("Error Occured!")
        messages.warning(self.request,"Error while Applying Event!")
        return redirect("/collaborations/customer_event_list/")
