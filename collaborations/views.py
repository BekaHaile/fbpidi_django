
import os
import datetime
from django.utils import timezone
 
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.views import View
from django.db.models import Q, Count

from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
									 #redirect with context 
 
from .forms import PollsForm, TenderForm, TenderEditForm, CreateJobApplicationForm

from company.models import Company, CompanyBankAccount, Bank, CompanyStaff, CompanyEvent, EventParticipants
from accounts.models import User, CompanyAdmin, Company

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from accounts.email_messages import sendEventNotification, sendEventClosedNotification, sendTenderEmailNotification
from wsgiref.util import FileWrapper
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from collaborations.forms import (BlogsForm, BlogsEdit, BlogCommentForm, FaqsForm, VacancyForm,JobCategoryForm,ForumQuestionForm,CommentForm,CommentReplayForm,NewsForm, CompanyEventForm, EventParticipantForm, 
								AnnouncementForm,ResearchForm,ResearchProjectCategoryForm, TenderApplicantForm, PollsForm, CreatePollForm, CreateChoiceForm, DocumentForm )

from collaborations.models import ( PollsQuestion, Choices, PollsResult, Tender, TenderApplicant, Blog, BlogComment,Faqs, Vacancy,JobApplication, 
									JobCategory,ForumQuestion, Faqs, Vacancy, JobApplication, JobCategory, News, NewsImages, ForumComments, 
									CommentReplay,Announcement,AnnouncementImages,Research,ResearchProjectCategory, Document)

from collaborations.api.serializers import NewsListSerializer

from django.http import JsonResponse

### a dictionay holding model names with model objects, Used to hold a model object for a string
models = { 'Research':Research,'Announcement':Announcement, 'Blog':Blog, 'BlogComment':BlogComment, 'Choice':Choices, 'Event':CompanyEvent, 'Tender':Tender, 'TenderApplicant':TenderApplicant, 
            'Forums':ForumQuestion, 'Forum Comments':ForumComments, 'Job Application':JobApplication, 'Job Category':JobCategory, 'Polls':PollsQuestion, 'News':News }

def check_user_has_company(request):
    try:
        return request.user.get_company()
    except Exception as e:
        messages.warning(request, "Currently, You are not related with any registered Company.")
        print("Exception while trying to find the company of an company admin or company staff user in  ", str(e))
        return False


def related_company_title(model_name, obj):
    """
    given a modle name and an obj, searchs for other model objs with related company, if none found search for related objs with related title or description,
    if none found returns 4 elements from the model
    """
    model = models[model_name]
    result = FilterByCompanyname( [obj.company], model.objects.exclude(id =obj.id)  )
    if result['query'].count() != 0:
        return {'query':result['query'], 'message':f"Other {model_name}s from {obj.company.name} ", 'message_am': f"ሌሎቸ በ{obj.company.name_am} ድርጅት የተለቀቁ {model.model_am}" }
    else:
        result = search_title_related_objs(  obj, model.objects.exclude(id =obj.id)  )
        if result['query'].count() != 0:
            return {'query': result, 'message':f'Other {model_name}s with related content', 'message_am': f"ሌሎች ተቀራራቢ ውጤቶች "}
        else:
            return {'query':model.objects.exclude(id = obj.id)[:4], 'message': f'Other {model_name}s ', 'message_am': 'ሌሎች ውጤቶች'}
   

def related_company_title_status(model_name, obj):
    """
    given status column containing obj finds related objs with related company or title with status open or upcoming \n 
    For Event, Poll, Status
    """
    model = models[model_name]
    q =  Q(   Q(status = 'Open') | Q(status = 'Upcoming')  )
    c =  Q(   Q(company__name__contains = obj.company.name ) | Q(company__name_am__contains = obj.company.name_am ) ) 
    result = model.objects.filter(c , q).exclude(id = obj.id)
    if result.count() == 0:
        t = Q (  Q(title__icontains = obj.title) | Q(title_am__icontains = obj.title_am )  )
        result = model.objects.filter(  q , t  ).exclude(id = obj.id)
        if result.count() == 0:
            return {'query':model.objects.exclude(id = obj.id)[:3], 'message': f'Other {model_name}s ', 'message_am': 'ሌሎቸ ውጤቶች' }
        else:
            return {'query': result, 'message':f'Other {model_name}s with related content', 'message_am':'ሌሎች ተቀራራቢ ውጤቶቸ'  }
    else:
        return {'query': result, 'message':f"Other {model_name}s from {obj.company.name} ", 'message_am': f"ሌሎቸ በ{obj.company.name_am} ድርጅት የተለቀቁ" }


def search_title_related_objs( obj, query_list):
    return {'query':query_list.filter( Q(title__icontains = obj.title) | Q(title_am__icontains = obj.title_am) |Q(description__icontains = obj.title ) | Q(description_am__icontains = obj.title_am) ).distinct()} 

# returns all if there is no filter_key or there is no match, or the objects containg the filter_key, with their appropriat messages.
def SearchByTitle_All(model_name, request ): 
    """
    Search objects with requested title or title_am, if by_title is in request.kwargs, else return all
    """   
    try:
        model= models[model_name]
        if not 'by_title' in request.GET: #not searching, just displaying latest news 
            query  = model.objects.all()
            return { 'query': query, 'message': f" {model_name} ",  'message_am': f" {model.model_am} "} # 3 Polls Found!
        else:   #if there is a filter_key list
            filter_key = request.GET['by_title']
            query = model.objects.filter( Q(title__icontains = filter_key) | Q(title_am__icontains = filter_key) |Q(description__icontains = filter_key ) | Q(description_am__icontains = filter_key) ).distinct() 
            # if there is no match for the filter_key or there is no filter_key at all
            if query.count() == 0: 
                query = model.objects.all()
                return { 'query': query, 'message': f"No match containing '{filter_key}'!", 'message_am': f"ካስገቡት ቃል '{filter_key}' ጋር የሚግናኝ አልተገኘም፡፡ !" }       
            return { 'query': query, 'message': f"{query.count()} result found!", 'message_am': f"{query.count()} ውጤት ተገኝቷል!" }
    except Exception as e:
        print("Exception at SearchBYTitle_All", str(e))
        return {'query':[], 'message':'Exception occured!'}


def FilterByCompanyname(company_list,  query_set):
    try:
        q_object = Q()
        for company_name in company_list:
            q_object.add( Q(company__name = company_name ), Q.OR )
            q_object.add( Q(company__name_am = company_name ), Q.OR )
        query = query_set.filter(q_object).distinct()
        return {'query':query, 'message':f'{query.count()} result Found!', 'message_am': f" {query.count()} ውጤት ተገኝቷል" }
    except Exception as e:
        print("###########Exception at FilterByCompanyName", str(e))
        return {'query':query, 'message':f"No company found!", 'message_am':f"ምንም ማግኘት አልተቻለም!"}

#  Uses both search by title and filter by category at once
def SearchCategory_Title(model_name, request):
    """
    Uses both search by title and filter by category at once
    """
    result = SearchByTitle_All(model_name, request) #returns matching objects by title and title_am, if none all objects
    category_name = request.GET.getlist('by_category')
    if category_name[0] == 'All':
            return {'query':result['query'],'message':f"{result['query'].count()} {request.GET['by_title']} result found in {category_name[0]} category!", 
                                            'message_am': f"በ {category_name[0]} {result['query'].count()} ውጤት ተገኝቷል",
                                            'searched_category':'All', 'searched_name': request.GET['by_title'] }   
    result = filter_by('catagory', category_name, result['query'])
    result['searched_category'] = category_name[0]
    result['searched_name'] = request.GET['by_title']
    return result

# accepts dynamic field name with filtering field value keys, and filters from the query
def filter_by(field_name, field_values, query):
    """
    accepts field_name like category or title etc and filter keys like ['Food','Beverage'] and filters from a query
    """
    kwargs ={}
    q= Q()  
    for value in field_values:
        if value == 'All':
            break
        kwargs ['{0}__{1}'.format(field_name, 'contains')] = value
        q.add(Q(**kwargs),Q.OR)
        kwargs = {}
    result = query.filter(q)
    if not result.count() == 0:
        return {'query':result,'message':f"{result.count()} result found!",'searched_category':'All','message_am':f"{result.count()} ተገኝቷል! " ,'searched_name': field_name }
    return {'query':result, 'message':f"No results Found!", 'message_am':f" ምንም ውጤት አልተገኘም፡፡ !" ,'searched_category':'All', 'searched_name': field_name }

# returns paginated data from a query set
def get_paginated_data(request, query):
    page_number = request.GET.get('page', 1)
    try:
        return Paginator(query, 2).page(page_number)
    except Exception as e:
        print("exception at get_paginate_data ",e)
        return Paginator(query, 2).page(1)


class CustomerPollList(View):
    def get(self, *args, **kwargs):
        result ={}
        try:
            if 'by_company' in self.request.GET:
                result = FilterByCompanyname(self.request.GET.getlist('by_company'), PollsQuestion.objects.all())
            elif 'by_no_vote' in self.request.GET:
                result['query'] = PollsQuestion.objects.annotate(num_vote=Count('pollsresult')).order_by('-num_vote')
                if result['query'].count() > 0:
                    result['message'] = "Polls in order of number of votes!"
                    result['message_am'] = "በመራጮች ብዛት ቅደም ተከተል"
                else:
                    result['message'] = "No result Found!"
                    result['message_am'] = "ምንም ውጤት አልተገኘም"
            else:
                result = SearchByTitle_All('Polls', self.request) # this returns all if there is no search key or filter by search
            
            companies = []
            for comp in Company.objects.all():
                if comp.pollsquestion_set.count()>0:
                    companies.append(comp)
            if result['query']==0:
                result['query'] = PollsQuestion.objects.all()
                result['message'] = 'No Result Found!'
            data = get_paginated_data(self.request, result['query'])
            return render(self.request, "frontpages/poll/polls-list.html", { 'polls':data, 'message' : result['message'], 'message_am':result['message_am'],'companies':companies})

        except Exception as e:
            print("exceptio at polls list ",e)
            return redirect('index')

# class CompanyPollList(Listview):
#     model = PollsQuestion
#     template_name = "admin/collaborations/tenders.html"
#     context_object_name = 'polls'  

#     def get_queryset(self):            
#             return PollsQuestion.objects.filter(company = Compnay.objects.get(id = self.request.GET['id']) )

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
                return render(self.request, "frontpages/poll/poll_detail.html", context)
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
        

def change_to_datetime(calender_date):
    str_date = datetime.datetime.strptime(calender_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    return datetime.datetime.strptime(str_date,'%Y-%m-%d' )


########## tender related views
class CreateTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:    
            company = self.request.user.get_company()
            return render(self.request,'admin/collaborations/create_tender.html',{'form':TenderForm})
        except Exception as e: 
            print("execption at createtender ", str(e))
            return redirect("admin:index")
    def post(self,*args,**kwargs):
        try:
            form = TenderForm(self.request.POST)       
            if form.is_valid():
                tender = form.save(commit=False)
                tender.created_by = self.request.user
                if  self.request.FILES['document']:
                    tender.document = self.request.FILES['document']
                if self.request.POST['tender_type'] == "Paid":
                    tender.document_price = self.request.POST['document_price']
                else:
                    tender.document_price = 0     
                tender.start_date = change_to_datetime(self.request.POST['start_date'])
                tender.end_date = change_to_datetime(self.request.POST['end_date'])
                today = datetime.datetime.now().date()
                if tender.start_date.date() > today:
                    tender.status = "Upcoming"
                elif tender.start_date.date() <= today  :
                    tender.status = "Open"
                else:
                    tender.status = "Closed"
                tender.save()                  
                messages.success(self.request,"Tender Successfully Created")
                return redirect("admin:tenders")   
            else:
                messages.warning(self.request, "Error! Tender was not Created!" )
                return redirect("admin:tenders")   
        except Exception as e:
            print("Exception at collaborations.views.CreateTender post" , str (e))
            return redirect("admin:tenders")


def check_tender_startdate(request, tenders):
    today = timezone.now().date()
    for tender in tenders:
        if tender.start_date.date() <= today and tender.status != 'Open':
            if sendTenderEmailNotification(request, tender.created_by, tender, f"IIMP system has changed the status of the Tender titled '{tender.title}' to 'Open'. This occurs when the start date you set for a tender has reached.\n Then the system will automatically change the status for data consistency ."):
                tender.status = "Open"
                tender.save()
            else:
                print("########## could not send email to open tender ")                 


def check_tender_enddate(request, tenders):
    today = timezone.now().date()
    for tender in tenders:
        if tender.end_date.date() == today and tender.status != 'Closed':
            if sendTenderEmailNotification(request, tender.created_by, tender, f"IIMP system has changed the status of the Tender titled '{tender.title}' to 'Closed'. This occurs when the end date you set for a tender has reached. \n Then the system will automatically change the status for data consistency ."):
                tender.status = "Closed"
                tender.save() 
            else:
                print("could not send email to close tender")                


class TenderList(LoginRequiredMixin, ListView):
    model = Tender
    template_name = "admin/collaborations/tenders.html"
    context_object_name = 'tenders'  
    def get_queryset(self):
        check_tender_startdate(self.request, Tender.objects.filter( status='Upcoming') )
        check_tender_enddate(self.request, Tender.objects.filter( Q(status = 'Open') | Q(status = 'Upcoming') )  )
        if self.request.user.is_superuser:
            return Tender.objects.all() 
        else:
            return Tender.objects.filter(company = self.request.user.get_company()) if check_user_has_company(self.request) else []

    # def get(self, *args, **kwargs):           
    #     try:
    #         if self.request.user.is_superuser:
    #             tenders = Tender.objects.all()
    #             return render(self.request, "admin/collaborations/tenders.html", {'tenders':tenders,})
    #         else: 
    #             tenders = Tender.objects.filter(company = self.request.user.get_company())
    #             if not tenders:
    #                 messages.warning(self.request, "You have no tenders to control!!")
    #                 return render(self.request, "admin/collaborations/tenders.html")
    #             check_tender_enddate(self.request, tenders)       
    #             return render(self.request, "admin/collaborations/tenders.html", {'tenders':tenders,})
    #     except Exception as e:
    #             messages.warning(self.request, "Error while getting tenders",)
    #             print("Exception at tenderList get",str(e))
    #             return redirect("admin:index") 


class TenderDetail(LoginRequiredMixin, DetailView):
    model = Tender
    context_object_name = 'tender'
    template_name = 'admin/collaborations/tender_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TenderForm
        return context

 # def get(self, *args, **kwargs):         
    #     form = TenderForm()
    #     if 'id' in self.kwargs:
    #         try:
    #             tender = Tender.objects.get(id =self.kwargs['id'] )
    #             company_bank_accounts = tender.company.get_bank_accounts()
    #             context = {'form':form, 'company_bank_accounts':company_bank_accounts, 'tender':tender}
    #             return render(self.request,'admin/collaborations/tender_detail.html',context)
    #         except Exception as e:
    #             print("tender error", str(e))
    #             messages.warning(self.request,"Tender edit error")
    #             return redirect("admin:tenders")

    #     print("error at tenderDetail for admin")
    #     return redirect("admin:admin_polls")


class ManageBankAccount(LoginRequiredMixin,View):
	def post(self,*args,**kwargs):
		tender = Tender.objects.get(id =self.kwargs['id'])
		if tender:
			if self.kwargs['option'] == 'remove':
				tender.bank_account.remove( CompanyBankAccount.objects.get(id = self.request.POST['remove_bank_account']) )
			else:
				tender.bank_account.add( CompanyBankAccount.objects.get(id = self.request.POST['relate_bank_account']) )
			tender.save()
			return redirect(f"/admin/edit_tender/{self.kwargs['id']} ")
		messages.warning(self.request, "Error while Managing Bank Account!")
		return redirect("admin:tenders")


class EditTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            tender = Tender.objects.get(id =self.kwargs['id'] )
            banks= Bank.objects.all() # if there will be a scenario where the admin needs to add register new bank account
            return render(self.request,'admin/collaborations/create_tender.html', {'form':TenderEditForm(),'tender':tender,'edit':True})
        except Exception as e:
            print("Exception at Edit Tender,get ", e)
            return redirect("admin:tenders")

    def post(self,*args,**kwargs):  
        form = TenderEditForm(self.request.POST)                       
        if form.is_valid():
            try:
                tender= Tender.objects.get(id = self.kwargs['id'])            
                tender.title = self.request.POST['title']
                tender.title_am = self.request.POST['title_am']
                tender.description = self.request.POST['description']
                tender.description_am = self.request.POST['description_am']
                tender.tender_type = self.request.POST['tender_type']
                tender.start_date = change_to_datetime(self.request.POST['start_date'])
                tender.end_date = change_to_datetime(self.request.POST['end_date'])
                if self.request.POST["tender_type"] == "Free":
                    tender.document_price = 0
                else:
                    tender.document_price = self.request.POST["document_price"]
                if self.request.FILES:
                    tender.document = self.request.FILES['document'] 

                today = datetime.datetime.now().date()
                if tender.start_date.date() > today:
                    tender.status = "Upcoming"
                elif tender.start_date.date() <= today :
                    tender.status = "Open"
                else:
                    tender.status = "Closed"
                tender.last_updated_by = self.request.user
                tender.last_updated_date = timezone.now()
                tender.save()

            except Exception as e:
                print("There is an Exception while tying to edit a tender!", e)  
                return redirect("admin:tenders")
            messages.success(self.request,"Tender Successfully Edited")
            return redirect("admin:tenders") 
        else:
            messages.warning(self.request, "Error! Tender was not Edited!" )
            return redirect("admin:tenders")

######## Tender for customers
class CustomerTenderList(View):
    def get(self, *args, **kwargs): 
        try:
            result = {}       
            if 'by_status' in self.request.GET:
                result = filter_by('status', self.request.GET.getlist('by_status'), Tender.objects.all())
            elif 'by_company' in self.request.GET:
                by_company = FilterByCompanyname(self.request.GET.getlist('by_company'),  Tender.objects.all())
                result = filter_by('status', ['Open', 'Upcoming'], by_company['query'])
            elif 'by_document_type' in self.request.GET:
                by_type = filter_by('tender_type', self.request.GET.getlist('by_document_type'),  Tender.objects.all())
                result = filter_by('status', ['Open', 'Upcoming'], by_type['query'])
            else:
                result = SearchByTitle_All('Tender', self.request)
            if  result['query'].count() == 0:
                result['query'] = Tender.objects.filter( Q(status='Open') | Q(status = 'Upcoming') )
            companies = []
            for comp in Company.objects.all():
                if comp.tender_set.count() > 0:
                    companies.append(comp)
 
            data = get_paginated_data(self.request, result['query'])

            return render(self.request, "frontpages/tender/customer_tender_list.html", {'tenders':data, 'companies': companies, 'message':result['message'], 'message_am':result['message_am']})
        
        except Exception as e:
                print( "Error while getting tenders",e)
                return redirect("index")     


class CustomerTenderDetail(View):
    def get(self, *args, **kwargs):  
        try:
            tender = Tender.objects.get(id = self.kwargs['id']  )
            return render(self.request, "frontpages/tender/customer_tender_detail.html", {'tender':tender, 'applicant_form':TenderApplicantForm})
        except Exception as e:
            print("Exception at customerTenderDetail :", str(e))
            messages.warning(self.request, "tender not found")
            return redirect("tender_list")


class ApplyForTender(View):
	def post(self, *args, **kwargs):
            tender= Tender.objects.get(id = self.kwargs['id']) 
            applicant = TenderApplicant(first_name = self.request.POST['first_name'], last_name = self.request.POST['last_name'],email = self.request.POST['email'],phone_number = self.request.POST['phone_number'],company_name = self.request.POST['company_name'],company_tin_number=self.request.POST['company_tin_number'],tender = tender)
            applicant.save()
            messages.success(self.request, "Application Successfully Completed")
            return render(self.request, "frontpages/tender/customer_tender_detail.html", {'tender':tender, 'applied':True})
        # except Exception as e:
        #     print("Exception at Apply for tender ",e)
        #     return redirect("/collaborations/tender_list/")


############ News

class CreateNews(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        check_user_has_company(self.request) 
        return render(self.request,'admin/collaborations/create_news.html',{'form':NewsForm})
    
    def post(self, *args, **kwargs):
        form = NewsForm( self.request.POST) 
        if form.is_valid:
            news = form.save(commit=False)
            news.created_by = self.request.user
            news.save()
            for image in self.request.FILES.getlist('images'):
                imag = NewsImages(created_by=self.request.user, created_date=timezone.now(), news=news, name = image.name, image = image)
                imag.save()
            messages.success(self.request, "News Created Successfully!")
            return redirect("admin:news_list") 
        else:
            messages.warning(self.request, "Error! News not Created!")


class EditNews(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:   
            if 'id' in self.kwargs:
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
                news.last_updated_by = self.request.user
                news.last_updated_date = timezone.now()    
                news.save()
                if 'images' in self.request.FILES:
                    for image in self.request.FILES.getlist('images'):
                        imag = NewsImages(created_by=self.request.user, created_date=timezone.now(), news=news, name = image.name, image = image)
                        imag.save()
                messages.success(self.request, "News Edited Successfully!")
                return redirect(f"/admin/news_detail/{news.id}/") 
            else:
                messages.warning(self.request, "Error! News not Edited!")


class AdminNewsList(LoginRequiredMixin, ListView):
    model = News
    template_name = "admin/collaborations/admin_news_list.html"
    context_object_name = 'newslist'
    def get_queryset (self):
        if self.request.user.is_superuser:
            return News.objects.all()
        else:
            try: 
                return News.objects.filter(company=self.request.user.get_company()) if check_user_has_company(self.request) else []
            except Exception as e:
                print("Exception while trying to fetch news objects")
                return redirect("admin:index")


class NewsDetail(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):         
        if self.kwargs['id']:
            try:
                news = News.objects.get(id =self.kwargs['id'] )
                context = {'form':NewsForm, 'news':news , "NEWS_CATEGORY": News.NEWS_CATAGORY}
                return render(self.request,'admin/collaborations/news_detail.html',context)
            except Exception as e:
                return redirect("admin:news_list")
        print("error at newsDetail for admin")
        return redirect("admin:news_list")


#just checking Ajax, not exactly working
def Ajax(request):
    if request.is_ajax and request.method == "GET":
        selected_categories = request.GET["by_category"].split(",")
        news= News.objects.filter(catagory = selected_categories[0] )
        return JsonResponse ({'respo': NewsListSerializer(news, many = True).data})
    else:
        result = SearchByTitle_All('News', self.request)
        return render(self.request, "frontpages/news/customer_news_list.html", {'news_list':result['query'], 'message':result['message'], 'NEWS_CATAGORY':News.NEWS_CATAGORY})
       

##### News, Customer
# list all or by_category or by_title or description
#Searchbytitle searchs a key from title and description and return PollsResult
#searchbycategory accepts a model, categories, and a query_list to filter from. If it does not found
#any result it will return all objects by using the model
class CustomerNewsList(View):
    def get(self, *args, **kwargs):
        result = []
        try:
            if 'by_category' in self.request.GET and 'by_title' in self.request.GET:
                result = SearchCategory_Title('News', self.request)
                data = get_paginated_data(self.request, result['query'])
                return render(self.request, "frontpages/news/customer_news_list.html", {'news_list':data, 'message':result['message'],  'message_am':result['message_am'],'NEWS_CATAGORY':News.NEWS_CATAGORY,
                                                                    'searched_category':result['searched_category'], 'searched_name':result['searched_name']})
            elif 'by_category' in self.request.GET:
                result = filter_by('catagory', self.request.GET.getlist('by_category'), News.objects.all())
            elif 'by_company' in self.request.GET:
                result = FilterByCompanyname(self.request.GET.getlist('by_company'), News.objects.all())
            else: 
                result = SearchByTitle_All('News', self.request)

            if result['query'].count()==0:
                result['query'] = News.objects.all()
            data = get_paginated_data(self.request, result['query'])
        
            return render(self.request, "frontpages/news/customer_news_list.html", {'news_list':data, 'message':result['message'],  'message_am':result['message_am'], 'NEWS_CATAGORY':News.NEWS_CATAGORY})
        
        except Exception as e:
            print("exceptio at news list ",e)
            return redirect('index')


class CustomerNewsDetail(View):
    def get(self, *args, **kwargs): 
        try:
            companies = []
            for comp in Company.objects.all():
                if comp.news_set.count() > 0:
                    companies.append(comp)
            news = get_object_or_404(News, id = self.kwargs['id'])
        except Exception as e:
            print("Exception at customerNews Detail ", e)
            return redirect('customer_news_list')
        related_news = related_company_title('News', news)
        return render(self.request, "frontpages/news/customer_news_detail.html", {'news':news,'related_news':related_news['query'], 'related_message':related_news['message'], 'related_message_am':related_news['message_am'], 'companies':companies, "NEWS_CATEGORY": News.NEWS_CATAGORY})

############ Event
###Admin side
class AdminCompanyEventList(LoginRequiredMixin, ListView):
    model = CompanyEvent
    template_name = "admin/collaborations/admin_companyevent_list.html"
    context_object_name = "events"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CompanyEventForm.objects.all()
        else: 
            return CompanyEvent.objects.filter(company =  self.request.user.get_company())


class CreateCompanyEvent(LoginRequiredMixin, CreateView):
        model = CompanyEvent
        form_class = CompanyEventForm
        template_name = "admin/collaborations/create_events.html"

        def form_valid(self,form):
            event = form.save(commit=False)
            if event.start_date.date() > timezone.now().date():
                event.status = "Upcoming"
            elif event.start_date.date() == timezone.now().date():
                 event.status = 'Open'
            else:
                event.status = 'Closed' 
            event.company = self.request.user.get_company()
            event.created_by = self.request.user               
            event.save()
            messages.success(self.request,"Event Created Successfully")
            return redirect('admin:admin_companyevent_list')

        def form_invalid(self,form):
            messages.warning(self.request,form.errors)
            return redirect('admin:create_companyevent')


def change_to_datetime(calender_date):
    str_date = datetime.datetime.strptime(calender_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    return datetime.datetime.strptime(str_date,'%Y-%m-%d' )

class EditCompanyEvent(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        return render(self.request, "admin/collaborations/create_events.html",{'edit':True,'event':CompanyEvent.objects.get(id = self.kwargs['pk'])})

    def post(self,*args,**kwargs):
        form = CompanyEventForm(self.request.POST,self.request.FILES)
        event = CompanyEvent.objects.get(id=self.kwargs['pk']) 
        if form.is_valid():
            form.save(commit=False)
            event.title = self.request.POST['title']
            event.title_am = self.request.POST['title_am']
            event.description = self.request.POST['description']
            event.description_am = self.request.POST['description_am']
            event.start_date = change_to_datetime(self.request.POST['start_date'])
            event.end_date = change_to_datetime(self.request.POST['end_date'])
            if event.start_date.date() > timezone.now().date():
                event.status = "Upcoming"
            elif event.start_date.date() == timezone.now().date():
                 event.status = 'Open'
            else:
                event.status = 'Closed' 
            if self.request.FILES:
                event.image = self.request.FILES['image']
            event.last_updated_by = self.request.user
            event.last_updated_date = timezone.now()
            event.save() 
            messages.success(self.request,"Event Edited Successfully")
            return redirect('admin:admin_companyevent_list')
        else:
            messages.warning(self.request,form.errors)
            return redirect('admin:admin_companyevent_list')








####### Event customer side
def check_event_participation(request, event_participants):
        today = timezone.now().date()
        for participant in event_participants:
            if participant.notify_on <= today: #lesser than is used, because if we check event participation notification once a day and 
                                                      # if the system could not send on the notify date, then it will send even if the notify me date has passed, but the event is in upcoming status
                if sendEventNotification(request, participant):
                    participant.notified = True
                    participant.save()
                else:
                    print("Couldn't send event notification ")


def check_event_enddate(request, open_events):
    today = timezone.now().date()
    for event in open_events: 
        if today >= event.end_date.date():
            print("event closed found ", event.title, " ", event.end_date, " ", event.end_date.date())
            if sendEventClosedNotification(request, event):
                event.status = "Closed"
                event.save()        
            else:
                print("Couldn't send Email to close event")

class CustomerEventList(View):
	def get(self, *agrs, **kwargs):
 
            result ={}
            if 'by_status' in self.request.GET:
                result = filter_by('status',[self.request.GET['by_status']], CompanyEvent.objects.all())
            elif 'by_company' in self.request.GET:
                result = FilterByCompanyname(self.request.GET.getlist('by_company'), CompanyEvent.objects.all())
            else:
                result = SearchByTitle_All('Event', self.request)
            if result['query'].count() == 0:
                result['query'] = CompanyEvent.objects.all()
            data = get_paginated_data(self.request, result['query'])
            #12345 make it background
            check_event_enddate(self.request, CompanyEvent.objects.filter( status = 'Upcoming') )
            event_participants = EventParticipants.objects.filter(notified = False, event__status = "Upcoming")
            check_event_participation(self.request, event_participants)
            eventcompanies = []
            for comp in Company.objects.all():
                if comp.companyevent_set.count() > 0:
                    eventcompanies.append(comp)
            
            return render(self.request, "frontpages/news/customer_event_list.html", {'events':data, 'message':result['message'],  'message_am':result['message_am'],'event_companies':eventcompanies})
        
        
class CustomerEventDetail(View):
    def get(self, *args, **kwargs): 
        try:
            eventcompanies = []
            for comp in Company.objects.all():
                if comp.companyevent_set.all().count() > 0:
                    eventcompanies.append(comp)
            event = get_object_or_404( CompanyEvent, id = self.kwargs['id']  )
            related_objs = related_company_title_status('Event', event)
            return render(self.request, "frontpages/news/customer_event_detail.html", {'event':event,'event_participant_form':EventParticipantForm, 'event_companies':eventcompanies, 'related_objs':related_objs['query'], 'related_message':related_objs['message'], 'related_message_am':related_objs['message_am']})
        except Exception as e:
            print("Exception at customerEventDetail", e)
            result = SearchByTitle_All('Event', self.request)
            return redirect('customer_event_list')

#12345  use ajax for event participation.
class EventParticipation(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):   
                try:  
                    event = get_object_or_404( CompanyEvent, id = self.kwargs['id'])
                    print(self.request.POST["notify_on"])
                    older = EventParticipants.objects.filter(event = event, patricipant_email = self.request.POST['patricipant_email']).first()
                    if older:
                        older.notify_on = self.request.POST["notify_on"]
                        older.notified = False
                        older.save()
                    else:
                        participant = EventParticipants(user =self.request.user, event= event, patricipant_email=self.request.POST['patricipant_email'], notify_on=self.request.POST[ "notify_on"])
                        participant.save()
                    return redirect(f'/collaborations/customer_event_detail/{event.id}/')
                except Exception as e:
                    print("Exception occured while trying to paricipate in event", e)
                    return redirect(f"/collaborations/customer_event_detail/{self.kwargs['id']}/")
        

#########Document
###Admin Side
class CreateDocument(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        check_user_has_company(self.request)
        return render(self.request, "admin/document/create_document.html", {'form':DocumentForm})
    def post(self, args, **kwargs):
        form = DocumentForm(self.request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.created_by = self.request.user
            document.document =  self.request.FILES['document']
            document.save()
            messages.success(self.request,'Successfully created the document!')
            return redirect("/admin/list_document_by_category/all/")
        else:
            messages.warning(self.request,'Could not create the document!' + str(form.errors))
            return render(self.request, "admin/document/create_document.html", {'form':DocumentForm})
        

class EditDocument(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            doc = get_object_or_404(Document, id = self.kwargs['id'])
            return render(self.request, "admin/document/create_document.html", {'edit':True, 'document':doc, 'form':DocumentForm, })
        except Http404:
            messages.warning(self.request, "Document not Found!")
            return render(self.request, "admin/document/list_document_by_category.html", {'categories':Document.DOC_CATEGORY})
        
    def post(self, args, **kwargs):
        try:
            document = get_object_or_404(Document, id = self.kwargs['id'])
        except Http404:
            messages.warning(self.request, "Document not Found!")
            return render(self.request, "admin/document/list_document_by_category.html", {'categories':Document.DOC_CATEGORY})
        document.title = self.request.POST['title']
        document.category = self.request.POST['category']
        if self.request.FILES:
            document.document =  self.request.FILES['document']
        document.last_updated_by = self.request.user
        document.last_updated_date = timezone.now()
        document.save()
        messages.success(self.request,'Successfully Edited the document!')
        return render(self.request, f"admin/document/list_document_by_category.html", {'documents':Document.objects.filter(category = document.category), 'categories': Document.DOC_CATEGORY})
        
       
class DocumentListing(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        documents = []
        try:
            if check_user_has_company(self.request):
                if self.kwargs['option'] != 'all':
                    documents =  Document.objects.filter( category = self.kwargs['option'] , company=self.request.user.get_company())
                    if documents.count() != 0:
                        return render(self.request, "admin/document/list_document_by_category.html", {'documents':documents, 'categories':Document.DOC_CATEGORY})
                    else:
                        messages.warning(self.request, f"No documents for {self.kwargs['option']}")
                return render(self.request, "admin/document/list_document_by_category.html", {'categories':Document.DOC_CATEGORY})
            else:        
                return render(self.request, "admin/document/list_document_by_category.html", {'categories':Document.DOC_CATEGORY})
        except Exception as e:
            print("exceptio at document list ",e)
            return redirect('admin:index')
