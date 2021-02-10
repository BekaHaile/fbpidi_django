
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
from .models import PollsQuestion, Choices, PollsResult, Tender, TenderApplicant
from .forms import PollsForm, TenderForm, TenderEditForm, CreateJobApplicationForm
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


##------------------ ResearchProjects



# --------------- Announcement


#---------------- forum and comment on forum


## ------------- Blogs Views



## --- Blogs Views


## --- Faqs views



	
# -----  vacancy and jobCategory




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
		tender= Tender.objects.get(id = self.kwargs['id'])
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
            #return redirect("/collaborations/tender_list/")
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
