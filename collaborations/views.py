from collaborations.models import Blog, BlogComment
from collaborations.forms import FaqsForm
from django.shortcuts import render, redirect, reverse
from django.views import View
import datetime

from collaborations.models import Faqs, Vacancy
                                     #redirect with context
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import PollsQuestion, Choices, PollsResult, Tender, TenderApplicant, TenderApplications
from .forms import PollsForm, TenderForm, TenderEditForm, CreateJobApplicationForm
from django.contrib import messages

from company.models import Company, CompanyBankAccount, Bank
from accounts.models import User, CompanyAdmin, Company
import os
from django.http import FileResponse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from company.models import Company, CompanyStaff

from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm
from django.http import HttpResponse, FileResponse
                         
from wsgiref.util import FileWrapper

from collaborations.forms import BlogsForm, BlogCommentForm, FaqsForm, VacancyForm,JobCategoryForm
from collaborations.models import Blog, BlogComment,Faqs,Vacancy,JobApplication, JobCategoty


from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

## --- Blogs Views
class CreatBlog(LoginRequiredMixin,View):
    template_name="admin/pages/blog_form.html"
    def get(self,*args,**kwargs):
        form = BlogsForm()
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
        end=start[:19]
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
        vacancy = VacancyForm() 
        context = {'vacancy':vacancy}
        return render(self.request,"admin/pages/job_form.html",context)

    def post(self,*args,**kwargs):
        form = VacancyForm(self.request.POST,self.request.FILES)
        context = {'vacancy':form}
        template = "admin/pages/job_form.html"
        if form.is_valid():
            category = JobCategoty.objects.get(id=self.request.POST['category'],)
            print("------")
            print(self.request.POST['starting_date'])
            print("======")
            print()
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
            print("---------after save---------"+str(vacancy.starting_date))
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
                print ("444444444444444444444444" ,str(e))
                messages.warning(self.request, "Poll not found")
                return redirect("polls") 

        else:
            messages.warning(self.request, "Nothing selected!")
            return redirect("polls")

    def post(self,*args,**kwargs):
        if self.kwargs['id'] and self.request.POST['selected_choice']: 
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id'] )

                # if the creator tries to vote, redirect to poll list
                # if poll.user == self.request.user:
                #     messages.warning(self.request, "You can not vote on this poll, since you are the creator of the poll!")
                #     return redirect("polls") 
                
                # # #if the user already voted on this poll, redirect to poll list
                # if PollsResult.objects.filter(poll=poll, user = self.request.user):
                #     messages.warning(self.request, "You have already voted for on poll!")
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
                messages.warning(self.request, "Poll not found!")
                return redirect("polls") 
             
                
        messages.warning(self.request, "Invalid Vote!")        
        return redirect("polls")
        


########## tender related views
###
class CreateTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:    
            form = TenderForm()
            try:
                company = Company.objects.get(user = self.request.user)
            except Exception as e:
                return redirect("admin:create_company_profile")
            company_bank_accounts = company.get_bank_accounts()
            banks= Bank.objects.all() # if there will be a scenario where the admin needs to add register new bank account
            context = {'form':form, 'banks':banks, 'company_bank_accounts':company_bank_accounts}
            return render(self.request,'admin/collaborations/create_tender.html',context)
        except Exception as e: 
            print("execption at createtender ", str(e))
            return redirect("admin:index")
    
    def post(self,*args,**kwargs):
        form = TenderForm(self.request.POST)  
        try:                 
            if form.is_valid():
                print("form is valid")
                tender = form.save(commit=False)
                user = None
                if self.request.user.is_company_admin: 
                    user = CompanyAdmin.objects.get(user=self.request.user) 

                # elif self.request.user.is_staff:
                #     user = CompanyStaff.objects.get(user.self.request.user)
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
                import pprint
                pprint.pprint(self.request.POST)
           
                pprint.pprint(self.request.FILES)
                print(form.errors)
                messages.warning(self.request, "Error! Tender was not Created!" )
                return redirect("admin:tenders")
                
        except Exception as e:
            print("Exception at collaborations.views.CreateTender post" , str (e))
            return redirect("admin:tenders")

def check_tender_enddate(request, tenders):
    now = datetime.datetime.now()
    for tender in tenders:
        endstr = str(tender.end_date.date)
        if tender.end_date.day < datetime.datetime.now().day and tender.status == "Open":
            # if tender.end_date.time() <= datetime.datetime.now().time():
                    tender.status = "Closed"
                    tender.save()
                    sendTenderClosedEmailNotification(request, tender.user, tender)
    return tenders

def sendTenderClosedEmailNotification(request, user, tender):
    current_site = get_current_site(request)
    mail_message = f'The tender you created with a title "{tender.title}" has been just automatically closed by the system.\n This happens when the date you entered as an end date for the tender passes and you (the creator) did not update the status'

    mail_subject = f'Tender closed'
    to_email = user.email
    email = EmailMessage(
    mail_subject, mail_message, to=[tender.user.email]
    )
    email.content_subtype = "html"
    email.send()
    return email

class TenderList(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):          
        try:    
                tenders = Tender.objects.all()
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
                print(str(e))
                messages.warning(self.request,"Tender  edit error")
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
            context['start_date'] = start_date
            context['end_date'] = end_date
            banks= Bank.objects.all() # if there will be a scenario where the admin needs to add register new bank account
            context = {'form':form, 'banks':banks, 'company_bank_accounts':company_bank_accounts}
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
                tender.title = form.cleaned_data.get('title')
                tender.title_am = form.cleaned_data.get('title_am')
                tender.description = form.cleaned_data.get('description')
                tender.description_am = form.cleaned_data.get('description_am')
                tender.tender_type = form.cleaned_data.get('tender_type')
                tender.status = form.cleaned_data.get("status")
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
                return render(self.request, "frontpages/tender/customer_tender_list.html", {'tenders':tenders,})
        except Exception as e:
                messages.warning(self.request, "Error while getting tenders")
                return redirect("tender_list")     


class CustomerTenderDetail(View):
    def get(self, *args, **kwargs):  
          
        if self.kwargs['id'] :
            try:
                tender = Tender.objects.get(id = self.kwargs['id']  )
                
                return render(self.request, "frontpages/tender/customer_tender_detail.html", {'tender':tender,})

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
                company_tin_number=self.request.POST['company_tin_number']
            )
            applicant.save()
            application = TenderApplications(tender = tender, applicant=applicant)
            application.save()
            messages.success(self.request, "Application Successfully Completed")
            print("Created successfully") 
            # pdf_download(self.request, tender.id)
            return redirect("/collaborations/tender_list/")

            # return HttpResponseRedirect(reverse('customer_tender_detail',  kwargs={'id':tender.id} ))
                                        
            # return redirect(reverse("/collaborations/tender_list/", kwargs={ 'applied': True }))
            # return redirect(CustomerTenderDetail, id = tender.id, applied=True)

            # return HttpResponseRedirect(redirect_to= f"/collaborations/customer_tender_detail/{tender.id}/", kwargs={'applied':True})
            # HttpResponseRedirect()
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

