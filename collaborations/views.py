
import os
import datetime
from django.utils import timezone
 
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.views import View
from django.db.models import Q

from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
									 #redirect with context 
 
from .forms import PollsForm, TenderForm, TenderEditForm, CreateJobApplicationForm

from company.models import Company, CompanyBankAccount, Bank, CompanyStaff, CompanyEvent, EventParticipants
from company.forms import EventParticipantForm
from accounts.models import User, CompanyAdmin, Company

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from accounts.email_messages import sendEventNotification, sendEventClosedNotification
from wsgiref.util import FileWrapper
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from collaborations.forms import (BlogsForm, BlogsEdit, BlogCommentForm, FaqsForm, VacancyForm,JobCategoryForm,ForumQuestionForm,CommentForm,CommentReplayForm,NewsForm, 
								AnnouncementForm,ResearchForm,ResearchProjectCategoryForm, TenderApplicantForm, PollsForm, CreatePollForm, CreateChoiceForm, DocumentForm )

from collaborations.models import ( PollsQuestion, Choices, PollsResult, Tender, TenderApplicant, Blog, BlogComment,Faqs, Vacancy,JobApplication, 
									JobCategory,ForumQuestion, Faqs, Vacancy, JobApplication, JobCategory, News, NewsImages, ForumComments, 
									CommentReplay,Announcement,AnnouncementImages,Research,ResearchProjectCategory, Document)
from collaborations.api.serializers import NewsListSerializer

from django.http import JsonResponse

### a dictionay holding model names with model objects, Used to hold a model object for a string
models = { 'Announcement':Announcement, 'Blog':Blog, 'BlogComment':BlogComment, 'Choice':Choices, 'CompanyEvent':CompanyEvent, 'Tender':Tender, 'TenderApplicant':TenderApplicant, 
            'ForumQuestion':ForumQuestion, 'ForumComments':ForumComments, 'JobApplication':JobApplication, 'JobCategory':JobCategory, 'PollsQuestion':PollsQuestion, 'News':News }

def related_company_title(model_name, obj):
    """
    given a modle name and an obj, searchs for other model objs with related company, if none found search for related objs with related title or description,
    if none found returns 4 elements from the model
    """
    model = models[model_name]
    result = FilterByCompanyname( [obj.company], model.objects.exclude(id =obj.id)  )
    print(result)
    if result.count() != 0:
        return {'query':result, 'message':f"Other {model_name}s from {obj.company.company_name} "}
    else:
        result = search_title_related_objs(  obj, model.objects.exclude(id =obj.id)  )
        if result['query'].count() != 0:
            return {'query': result, 'message':f'Other {model_name}s with related content' }
        else:
            return {'query':model.objects.exclude(id = obj.id)[:4], 'message': f'Other {model_name}s ' }
   

def related_company_title_status(model_name, obj):
    """
    given status column containing obj finds related objs with related company or title with status open or upcoming \n 
    For Event, Poll, Status
    """
    model = models[model_name]
    q =  Q(   Q(status = 'Open') | Q(status = 'Upcoming')  )
    c =  Q(   Q(company__company_name__contains = obj.company.company_name ) | Q(company__company_name_am__contains = obj.company.company_name_am ) ) 
    result = model.objects.filter(c , q).exclude(id = obj.id)
    if result.count() == 0:
        t = Q (  Q(title__icontains = obj.title) | Q(title_am__icontains = obj.title_am )  )
        result = model.objects.filter(  q , t  ).exclude(id = obj.id)
        if result.count() == 0:
            return {'query':model.objects.exclude(id = obj.id)[:3], 'message': f'Other {model_name}s ' }
        else:
            return {'query': result, 'message':f'Other {model_name}s with related content' }
    else:
        return {'query': result, 'message':f"Other {model_name}s from {obj.company.company_name} "}


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
            return { 'query': query, 'message': f" {model_name} ",  'message_am': f" {model_name} "} # 3 Polls Found!
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


def FilterByCompanyname(company_list,  query_set):
    try:
        q_object = Q()
        for company_name in company_list:
            q_object.add( Q(company__company_name = company_name ), Q.OR )
            q_object.add( Q(company__company_name_am = company_name ), Q.OR )
        return query_set.filter(q_object).distinct()
    except Exception as e:
        print("###########Exception at FilterByCompanyName", str(e))
        return []



def SearchCategory_Title(model_name, request):
    """
    Uses both search by title and filter by category at once
    """
    result = SearchByTitle_All('News', request) #returns matching objects by title and title_am, if none all objects
    category_name = request.GET.getlist('by_category')
    if category_name[0] == 'All':
            return {'query':result['query'], 'message':f"{result['query'].count()} {request.GET['by_title']} result found in {category_name[0]} category!", 'searched_category':'All', 'searched_name': request.GET['by_title'] }   
    result = filter_by('catagory', category_name, result['query'])
    result['searched_category'] = category_name[0]
    result['searched_name'] = request.GET['by_title']
    return result


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
    return {'query':query, 'message':f"No results Found!", 'message_am':f"ካስገቡት ቃል  ጋር የሚግናኝ አልተገኘም፡፡ !" ,'searched_category':'All', 'searched_name': field_name }


class PollIndex(View):
    def get(self, *args, **kwargs):
        result = SearchByTitle_All('PollsQuestion', self.request) # this returns all if there is no search key or filter by search
        return render(self.request, "frontpages/poll/polls-list.html", { 'polls':result['query'], 'message' : result['message']})


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
                    company = company_staff.company
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
    now = datetime.datetime.now()
    for tender in tenders:
        endstr = str(tender.end_date.date)
        #need real comparison
        if tender.end_date.day < datetime.datetime.now().day and tender.end_date.month <= now.month:
                    sendTenderClosedEmailNotification(request, tender.user, tender)
                    tender.status = "Closed"
                    tender.save()
                    
    return True

#Admin Side
class TenderList(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
                  
        try:    
            if self.request.user.is_superuser:
                tenders = Tender.objects.all()
                #12345 make this thing work in background
                # result = check_tender_enddate(self.request, tenders.filter(status="Open"))       
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
                result = SearchByTitle_All('Tender', self.request)
                return render(self.request, "frontpages/tender/customer_tender_list.html", {'tenders':result['query'], 'message':result['message']})
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
			return render(self.request, "frontpages/tender/customer_tender_detail.html", {'tender':tender, 'applied':True})
		else:
			print("Error Occured!")
			messages.warning(self.request,"Error while Applying!")
			return redirect("/collaborations/tender_list/")


############ News

class CreateNews(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:
                if self.request.user.is_company_admin:
                    company = Company.objects.get(user = self.request.user)
                elif self.request.user.is_company_staff:
                    company_staff = CompanyStaff.objects.filter(user=self.request.user).first()
                    company = company_staff.company
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
            if self.kwargs['id']:
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

                if self.request.FILES:
                    for image in self.request.FILES.getlist('images'):
                        imag = NewsImages(created_by=self.request.user, created_date=timezone.now(), news=news, name = image.name, image = image)
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
        if 'by_category' in self.request.GET and 'by_title' in self.request.GET:
            result = SearchCategory_Title('News', self.request)
            return render(self.request, "frontpages/news/customer_news_list.html", {'news_list':result['query'], 'message':result['message'], 'NEWS_CATAGORY':News.NEWS_CATAGORY,
                                                                'searched_category':result['searched_category'], 'searched_name':result['searched_name']})
        elif 'by_category' in self.request.GET:
            result = filter_by('catagory', self.request.GET.getlist('by_category'), News.objects.all())
        elif 'by_company' in self.request.GET:
            query = FilterByCompanyname(self.request.GET.getlist('by_company'), News.objects.all())
            if query.count() > 0:
                result = {'query' : query, 'message' : f"{query.count()} Found!", 'message_am' : f"{query.count()} ተገኝቷል!" }
            else:
                result = {'query' : News.objects.all(), 'message' : 'No match found!', 'message_am' : 'የጠየቁትን ማግኘት አልቻልንም!'} 
        else:
            
            result = SearchByTitle_All('News', self.request)
        return render(self.request, "frontpages/news/customer_news_list.html", {'news_list':result['query'], 'message':result['message'], 'message_am':result['message_am'], 'NEWS_CATAGORY':News.NEWS_CATAGORY})
       

class CustomerNewsDetail(View):
    def get(self, *args, **kwargs): 
        try:
            all_company = Company.objects.all()[:5]
            companies = []
            for comp in all_company:
                if comp.news_set.count() > 0:
                    companies.append(comp)
            news = get_object_or_404(News, id = self.kwargs['id'])
         
        except Exception as e:
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^ Exception at customerNews Detail ", e)
            return redirect('customer_news_list')
            
        related_news = related_company_title('News', news)
        return render(self.request, "frontpages/news/customer_news_detail.html", {'news':news,'related_news':related_news['query'], 'related_message':related_news['message'], 'companies':companies, "NEWS_CATEGORY": News.NEWS_CATAGORY})
    

##### Customer Events
def check_event_participation(request, event_participants):
    today = datetime.datetime.now()
    today = today.strftime('%Y-%m-%d %H:%M:%S')
   
    for participant in event_participants:  
        start_day = participant.event.start_date
        start_day = start_day.strftime('%Y-%m-%d %H:%M:%S')
        # if start_day > today and start_day - today == participant.notifiy_in:
        #     sendEventNotification(request, participant) 
    return True


def check_event_enddate(request, open_events):
    now = datetime.datetime.now() 
    for event in open_events:
        endstr = str(event.end_date.date)
        #need real comparison
        if event.end_date.day < datetime.datetime.now().day and event.end_date.month < now.month:
                    sendEventClosedNotification(request, event)
                    event.status = "Closed"
                    event.save()        
    return True


class CustomerEventList(View):
	def get(self, *agrs, **kwargs):
            result = SearchByTitle_All('CompanyEvent', self.request)
            if 'by_status' in self.request.GET:
                result = filter_by('status',[self.request.GET['by_status']], result['query'])
            if 'by_company' in self.request.GET:
                query = FilterByCompanyname(self.request.GET.getlist('by_company'), result['query'])
                if query.count() > 0:
                   result ['query'] = query
                   result ['message'] = f'{query.count()} Found!' 
                else:
                    result['message'] = 'No match found!'
            #12345 make it background
            event_participants = EventParticipants.objects.filter(notified = False, event__status = "Upcoming")
            check_event_participation(self.request, event_participants)
            all_company = Company.objects.all()
            eventcompanies = []
            for comp in all_company:
                if comp.companyevent_set.count() > 0:
                    eventcompanies.append(comp)
            return render(self.request, "frontpages/news/customer_event_list.html", {'events':result['query'], 'message':result['message'], 'event_companies':eventcompanies})
        
        
class CustomerEventDetail(View):
    def get(self, *args, **kwargs): 
        try:
            all_company = Company.objects.all()
            eventcompanies = []
            for comp in all_company:
                if comp.companyevent_set.all().count() > 0:
                    eventcompanies.append(comp)
            event = get_object_or_404( CompanyEvent, id = self.kwargs['id']  )
            related_objs = related_company_title_status('CompanyEvent', event)
            return render(self.request, "frontpages/news/customer_event_detail.html", {'event':event,'event_participant_form':EventParticipantForm, 'event_companies':eventcompanies, 'related_objs':related_objs['query'], 'related_message':related_objs['message']})
        except Exception as e:
            print("$$$$$$$$$$$$$$$$$$$$44 Exception at customerEventDetail", e)
            result = SearchByTitle_All('CompanyEvent', self.request)
            return redirect('customer_event_list')

#12345  use ajax for event participation.
class EventParticipation(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):   
        
        if 'patricipant_email' in self.request.POST and 'notify_in' in self.request.POST:
                notify_in = int(self.request.POST['notify_in'])
                try:
                    event = get_object_or_404( CompanyEvent, id = self.kwargs['id'])
                except Http404:
                    return redirect(f"/collaborations/customer_event_detail/{self.kwargs['id']}/")
                participant = EventParticipants(user =request.user, event= event,
                                                patricipant_email=request.POST['patricipant_email'])
                #12345 Real date comparison
                if event.start_date.month <= datetime.datetime.now().month:
                    if notify_in <=  event.start_date.day - datetime.datetime.now().day: 
                        participant.notified= False
                        participant.notifiy_in = notify_in
                        try:
                            participant.save()   # if the email has been previously registered, it will through an unique exception
                        except Exception as e:
                            return redirect(f"/collaborations/customer_event_detail/{self.kwargs['id']}/")
                        return redirect(f"/collaborations/customer_event_detail/{self.kwargs['id']}/")
                            
                    else:
                        print('Invalid Date to notify')
                        return redirect(f"/collaborations/customer_event_detail/{self.kwargs['id']}/")
                        
                else:
                    print('Invalid month to notify')
                    return redirect(f"/collaborations/customer_event_detail/{self.kwargs['id']}/")

        print('Email and notifi me in are required!')
        return redirect(f"/collaborations/customer_event_detail/{self.kwargs['id']}/")


#########Document
###Admin Side
class CreateDocument(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, "admin/document/create_document.html", {'form':DocumentForm})
    def post(self, args, **kwargs):
        form = DocumentForm(self.request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = self.request.user
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
        except Http404:
            messages.warning(self.request, "Document not Found!")
            return render(self.request, "admin/document/list_document_by_category.html", {'categories':Document.DOC_CATEGORY})
        # return redirect("/admin/list_document_by_category/all/")
        return render(self.request, "admin/document/create_document.html", {'edit':True, 'document':doc, 'form':DocumentForm, })
    
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
        document.save()
        messages.success(self.request,'Successfully Edited the document!')
        return render(self.request, f"admin/document/list_document_by_category.html", {'documents':Document.objects.filter(category = document.category), 'categories': Document.DOC_CATEGORY})
        
       
class DocumentListing(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if self.kwargs['option'] != 'all':
            documents =  Document.objects.filter( category = self.kwargs['option'])
            if documents.count() != 0:
                return render(self.request, "admin/document/list_document_by_category.html", {'documents':documents, 'categories':Document.DOC_CATEGORY})
            else:
                messages.warning(self.request, f"No documents for {self.kwargs['option']}")
        return render(self.request, "admin/document/list_document_by_category.html", {'categories':Document.DOC_CATEGORY})

