
import os
import json
import datetime

from PIL import Image
from django.views import View
from django.http import Http404
from django.urls import reverse
from django.utils import timezone 
from django.contrib import messages
from django.db.models import Q, Count
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, reverse
from accounts.models import User, CompanyAdmin, Company
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import  JsonResponse
from django.views.generic import CreateView,  DetailView, ListView

from datetime import timedelta
from accounts.email_messages import sendWeekBlogAndNews

from admin_site.decorators import company_created,company_is_active
from company.models import Company,CompanyEvent, EventParticipants
from .forms import  TenderForm
from collaborations.forms import (NewsForm, CompanyEventForm, EventParticipantForm, TenderApplicantForm, DocumentForm )

from collaborations.models import ( PollsQuestion, Choices, PollsResult, Tender, TenderApplicant, Blog, BlogComment,Faqs, Vacancy,JobApplication, 
									JobCategory,ForumQuestion, Faqs, Vacancy, JobApplication, JobCategory, News, NewsImages, ForumComments, 
									Announcement,AnnouncementImages,Research,ResearchProjectCategory, Document)

### a dictionay holding model names with model objects, Used to hold a model object for a string
models = { 'Research':Research,'Announcement':Announcement, 'Blog':Blog, 'BlogComment':BlogComment, 'Choice':Choices, 'Event':CompanyEvent, 'Tender':Tender, 'TenderApplicant':TenderApplicant, 
            'Forums':ForumQuestion, 'Forum Comments':ForumComments, 'Polls':PollsQuestion, 'News':News, 'Vacancy':Vacancy, 'Job Application':JobApplication, 'Job Category':JobCategory }

decorators = [never_cache, company_created(),company_is_active()]


def image_cropper(x,y,w,h,raw_image):
        # if the image is not cropped 
        if (x == '' or y == '' or w == '' or h == ''):
            image = Image.open(raw_image)
            resized_image = image.resize((600, 600), Image.ANTIALIAS)
            resized_image.save(raw_image.path)
            return True

        x = float(x)
        y = float(y)
        w = float(w)
        h = float(h)
        image = Image.open(raw_image)
        cropped_image = image.crop((x, y, w+x, h+y))
        ## replace the image with the cropped one
        cropped_image.save(raw_image.path)
        return True



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
        result = search_title_related(  obj, model.objects.exclude(id =obj.id)  )
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


def search_title_related( obj, query_list):
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
                return { 'query': query, 'message': f"No match containing '{filter_key}'!", 'message_am': f"ካስገቡት ቃል '{filter_key}' ጋር የሚገናኝ አልተገኘም፡፡ !" }       
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
            return {'query':result['query'],'message':f"{result['query'].count()} {request.GET['by_title']} result found !", 
                                            'message_am': f"{result['query'].count()} ውጤት ተገኝቷል",
                                            'searched_category':'All', 'searched_name': request.GET['by_title'] }   
    result = filter_by('catagory', category_name, result['query'])
    result['searched_category'] = category_name[0]
    result['searched_name'] = request.GET['by_title']
    return result

# accepts dynamic field name with filtering field value keys, and filters from the query
def filter_by(field_name, field_values, query):
    """
    accepts field_name like category or title etc and filter keys like ['key1','key2'] and filters from a query
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
        return Paginator(query, 6).page(page_number)
    except Exception as e:
        print("exception at get_paginate_data ",e)
        return Paginator(query, 6).page(1)


class IndexSearch(View):
    modules =  [('News','customer_news_list'),('Event','customer_event_list'),('Announcement','announcement_list'),('Polls','polls'),
                ('Tender','tender_list'),('Vacancy','vacancy'),('Blog','customer_blog_list'),('Research','research_list'), ('Forum','forum_list')]

    title_models = ['News','Event','Announcement','Polls','Tender','Vacancy']
    
    def blog_search(self):
        try:
            q = Q( Q(title__icontains = self.request.GET['by_title']) | Q(title_am__icontains = self.request.GET['by_title']) )
            return Blog.objects.filter(q)
        except Exception as e:
            print("@@@ Exception at IndexSearch blog, ",e)
            return redirect("index")    
    
    def forum_search(self):
        try:
            return ForumQuestion.objects.filter(title__icontains = self.request.GET['by_title'])
        except Exception as e:
            print("@@@ Exception at forum_search blog, ",e)
            return redirect("index")

    def research_search(self):
        try:
            return Research.objects.filter(Q(title__icontains = self.request.GET['by_title']))
        except Exception as e:
            print("@@@ Exception at research_search blog, ",e)
            return redirect("index")


    def get(self, *args, **kwargs):
        result = {}
        total = 0
    
        try:
            if 'by_title' in self.request.GET and 'by_model' in self.request.GET:
                model = self.request.GET['by_model']
                if model in self.title_models:
                    model_query =  SearchByTitle_All(model, self.request)['query']
                    if model_query.count() > 0:
                        total+= model_query.count()
                        result[model] = model_query

                elif model == "Blog":
                    blog_query = self.blog_search()
                    if blog_query.count()>0:
                        total+= blog_query.count()
                        result['Blog'] = blog_query

                elif model == "Forum":
                    forum_query = self.forum_search()
                    if forum_query.count() > 0:
                        total+= forum_query.count()
                        result['Forum'] = forum_query

                elif model == "Research":
                    research_query = self.research_search()
                    if research_query.count() > 0:
                        total+= research_query.count()
                        result['Research'] = research_query

                else: #if All
                    for model in self.title_models:
                        model_query =  SearchByTitle_All(model, self.request)['query']
                        if model_query.count() > 0:
                            total+= model_query.count()
                            result[model] = model_query
                        
                    blog_query = self.blog_search()
                    if blog_query.count()>0:
                        total+= blog_query.count()
                        result['Blog'] = blog_query
                    
                    research_query = self.research_search()
                    if research_query.count() > 0:
                        total+= research_query.count()
                        result['Research'] = research_query
                    
                    forum_query = self.forum_search()
                    if forum_query.count() > 0:
                        total+= forum_query.count()
                        result['Forum'] = forum_query
                
            else:
                return redirect("/")
            data = result
            data['modules'] = self.modules
            if total == 0:
                data['message'] = "No result found!"
                data['message_am']= "ምንም ውጤት አልተገኝም"
            else:
                data['message'] = f"{total} result found"
                data['message_am'] = f"{total} ውጤት ተገኝቷል"
            data['searched_name'] = self.request.GET['by_title']

            return render(self.request, "frontpages/index_search_page.html",data)
        except Exception as e:
            print("@@@@@@@@@@@@@ Exception ",e)
            return redirect("/")
        


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
                result['query'] = []
                result['message'] = 'No Result Found!'
            data = get_paginated_data(self.request, result['query'])
            return render(self.request, "frontpages/poll/polls-list.html", { 'polls':data, 'message' : result['message'], 'message_am':result['message_am'],'companies':companies})

        except Exception as e:
            print("exceptio at polls list ",e)
            return redirect('index')


#only visible to logged in and never voted before
class PollDetail(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        message = ""
        context = {}
        try:        
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
        except Exception as e:
            print("exceptio at polls detail ",e)
            return redirect('index')

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
@method_decorator(decorators,name='dispatch')
class CreateTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:    
            company = self.request.user.get_company()
            return render(self.request,'admin/collaborations/create_tender.html',{'form':TenderForm})
        except Exception as e: 
            print("execption at createtender ", str(e))
            return redirect("admin:error_404")
    def post(self,*args,**kwargs):
        
            form = TenderForm(self.request.POST)       
            try:
                if form.is_valid():
                    tender = form.save(commit=False)
                    tender.created_by = self.request.user 
                    tender.start_date = change_to_datetime(self.request.POST['start_date'])
                    tender.end_date = change_to_datetime(self.request.POST['end_date'])
                    today = datetime.datetime.now().date()
                    tender.save()                  
                    messages.success(self.request,"Tender Successfully Created")
                    return redirect("admin:tenders")   
                messages.warning(self.request, "Error! Tender was not Created!" )
                return render(self.requesst, 'admin/collaborations/create_tender.html',{'form':form})   
            except Exception as e:
                print("Exception at collaborations.views.CreateTender post" , str (e))
                messages.warning(self.request, "Could not create Tender")
                return redirect("admin:tenders")
                

@method_decorator(decorators,name='dispatch')
class TenderList(LoginRequiredMixin, ListView):
    model = Tender
    template_name = "admin/collaborations/tenders.html"
    context_object_name = 'tenders'  
    def get_queryset(self):
        try:
            if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
                return Tender.objects.all() 
            else:
                return Tender.objects.filter(company = self.request.user.get_company())
        except Exception as e:
            print("Exception while listing admin tenders ",e)
            return [] 


@method_decorator(decorators,name='dispatch')
class TenderDetail(LoginRequiredMixin, DetailView):
    model = Tender
    context_object_name = 'tender'
    template_name = 'admin/collaborations/tender_detail.html'
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['form'] = TenderForm
            return context
        except Exception as e:
            print("@@@ Exception at Tender Detail", e)
            return []

@method_decorator(decorators,name='dispatch')
class EditTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            tender = Tender.objects.get(id =self.kwargs['id'] )
            return render(self.request,'admin/collaborations/create_tender.html', {'form':TenderForm(),'tender':tender,'edit':True})
        except Exception as e:
            print("Exception at Edit Tender,get ", e)
            return redirect("admin:error_404")

    def post(self,*args,**kwargs):  
        try:
            form = TenderForm(self.request.POST)  
            tender= Tender.objects.get(id = self.kwargs['id'])                                 
            if  form.is_valid():
                tender.title = self.request.POST['title']
                tender.title_am = self.request.POST['title_am']
                tender.description = self.request.POST['description']
                tender.description_am = self.request.POST['description_am']
                tender.start_date = change_to_datetime(self.request.POST['start_date']) # using this to store a date without timezone
                tender.end_date = change_to_datetime(self.request.POST['end_date'])
                tender.last_updated_by = self.request.user
                tender.last_updated_date = timezone.now()
                tender.save()
                messages.success(self.request,"Tender Successfully Edited")
                return redirect("admin:tenders") 
            else:
                print("@@Exception at Edit Tender, ",form.errors)
                messages.warning(self.request, "Error! Tender was not Edited!", )
                return render(self.request,'admin/collaborations/create_tender.html', {'form':form,'tender':tender,'edit':True})
        except Exception as e:
                print("There is an Exception while tying to edit a tender!", e)  
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



class ApplyForCompanyTender(View):
    def post(self, *args, **kwargs):           
        try:
            tender = Tender.objects.get(id=self.kwargs['id'])
            applicant = TenderApplicant(first_name = self.request.POST['first_name'], last_name = self.request.POST['last_name'],email = self.request.POST['email'],phone_number = self.request.POST['phone_number'],company_name = self.request.POST['company_name'],company_tin_number=self.request.POST['company_tin_number'],tender = tender)
            applicant.save()
            return render(self.request, "frontpages/company/company_tender_detail.html", {'obj':tender,'object':tender.company, 'applied':True})
        except Exception as e:
            print("@@@ Exception at Apply For CompanyTender ",e)
            return redirect("/")

class ApplyForTender(View):
    def post(self, *args, **kwargs):
        try:
            tender= Tender.objects.get(id = self.kwargs['id']) 
            applicant = TenderApplicant(first_name = self.request.POST['first_name'], last_name = self.request.POST['last_name'],email = self.request.POST['email'],phone_number = self.request.POST['phone_number'],company_name = self.request.POST['company_name'],company_tin_number=self.request.POST['company_tin_number'],tender = tender)
            applicant.save()
            messages.success(self.request, "Application Successfully Completed")
            return render(self.request, "frontpages/tender/customer_tender_detail.html", {'tender':tender, 'applied':True})
        except Exception as e:
            print("Exception at Apply for tender ",e)
            return redirect("/collaborations/tender_list/")


############ News
@method_decorator(decorators,name='dispatch')
class CreateNews(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:
            return render(self.request,'admin/collaborations/create_news.html',{'form':NewsForm})
        except Exception as e:
            return redirect("admin:error_404")
    
    def post(self, *args, **kwargs):
        try:
            form = NewsForm( self.request.POST,self.request.FILES) 
            if form.is_valid:
                news = form.save(commit=False)
                news.created_by = self.request.user
                news.save()               
                data = self.request.POST
                image_cropper(data['x'],data['y'],data['width'],data['height'], news.image )
                messages.success(self.request, "News Created Successfully!")
                return redirect("admin:news_list") 
            else:
                messages.warning(self.request, "Error! News not Created!")
                return render(self.request,'admin/collaborations/create_news.html',{'form':form})
        except Exception as e:
            print("@@@@@@ Exception while creating News ",form.errors)
            return redirect("admin:error_404")


@method_decorator(decorators,name='dispatch')
class EditNews(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:   
            news = News.objects.get(id =  self.kwargs['id'])
            return render(self.request,'admin/collaborations/create_news.html',{'news':news, 'form':NewsForm(instance= news),'edit':True})
        except Exception as e: 
            print("execption at create News ", str(e))
            messages.warning(self.request,"Error, Could Not Find the News! ")
            return redirect("admin:error_404")
        
    def post(self, *args, **kwargs):
        try:
            news = get_object_or_404(News, id = self.kwargs['id'])
            form = NewsForm(self.request.POST, self.request.FILES, instance = news) 
            if form.is_valid:
                news = form.save(commit = False)
                news.last_updated_by = self.request.user
                news.last_updated_date = timezone.now()    
                news.save()
                data = self.request.POST
                image_cropper(data['x'],data['y'],data['width'],data['height'], news.image )
                messages.success(self.request, "News Edited Successfully!")
                return redirect(f"/admin/news_list/") 
            
            messages.warning(self.request, "Error! News not Edited!")
            return render(self.request,'admin/collaborations/create_news.html',{'news':news, 'form':form,'edit':True})
        except Exception as e:
            print("@@ Exception at Edit News at ",e)
            messages.warning(self.request, "Error! News not Edited!")
            return redirect("admin:news_list")


@method_decorator(decorators,name='dispatch')
class AdminNewsList(LoginRequiredMixin, ListView):
    model = News
    template_name = "admin/collaborations/admin_news_list.html"
    context_object_name = 'newslist'
    def get_queryset (self):
        if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
            return News.objects.all()
        else:
            try: 
                return News.objects.filter(company=self.request.user.get_company()) 
            except Exception as e:
                print("Exception while trying to fetch news objects")
                return []



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

            # if result['query'].count()==0:
            #     result['query'] = News.objects.all()
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
@method_decorator(decorators,name='dispatch')
class AdminCompanyEventList(LoginRequiredMixin, ListView):
    model = CompanyEvent
    template_name = "admin/collaborations/admin_companyevent_list.html"
    context_object_name = "events"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_fbpidi_staff:
            return CompanyEvent.objects.all()
        else: 
            return CompanyEvent.objects.filter(company =  self.request.user.get_company())


@method_decorator(decorators,name='dispatch')
class CreateCompanyEvent(LoginRequiredMixin, CreateView):
        model = CompanyEvent
        form_class = CompanyEventForm
        template_name = "admin/collaborations/create_events.html"

        def form_valid(self,form):
            try:
                event = form.save(commit=False)
                today = datetime.datetime.now().date()
                if today < event.start_date.date():
                    event.status = "Upcoming"
                elif event.start_date.date() <= today and today <=event.end_date.date():
                    event.status = "Open"
                elif today > event.end_date.date():
                    event.status = "Closed"
                event.company = self.request.user.get_company()
                event.created_by = self.request.user               
                event.save()
                data = self.request.POST
                image_cropper(data['x'],data['y'],data['width'],data['height'], event.image )
                messages.success(self.request,"Event Created Successfully")
                return redirect('admin:admin_companyevent_list')
            except Exception as e:
                print("@@@ Exception at CreateCompany Event ",e)
                return redirect('admin:create_companyevent')


        def form_invalid(self,form):
            messages.warning(self.request,form.errors)
            return render(self.request, "admin/collaborations/create_events.html", {'form':form})


def change_to_datetime(calender_date):
    str_date = datetime.datetime.strptime(calender_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    return datetime.datetime.strptime(str_date,'%Y-%m-%d' )


@method_decorator(decorators,name='dispatch')
class EditCompanyEvent(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            event  =CompanyEvent.objects.get(id = self.kwargs['pk'])
            return render(self.request, "admin/collaborations/create_events.html",{'edit':True,'form': CompanyEventForm(instance=event), 'event':event})
        except Exception as e:
            return redirect("admin:error_404")

    def post(self,*args,**kwargs):
        try:
            event = get_object_or_404(CompanyEvent, id=self.kwargs['pk'])
            form = CompanyEventForm(self.request.POST,self.request.FILES, instance=event)
            if  form.is_valid():
                event = form.save(commit=False)
                event.start_date = change_to_datetime(self.request.POST['start_date'])
                event.end_date = change_to_datetime(self.request.POST['end_date'])
                today = datetime.datetime.now().date()
                if today < event.start_date.date():
                    event.status = "Upcoming"
                elif event.start_date.date() <= today and today <=event.end_date.date():
                    event.status = "Open"
                elif today > event.end_date.date():
                    event.status = "Closed"
                event.last_updated_by = self.request.user
                event.last_updated_date = timezone.now()
                event.save()  
            
                data = self.request.POST
                image_cropper(data['x'],data['y'],data['width'],data['height'], event.image )
                
                messages.success(self.request,"Event Edited Successfully")
                return redirect('admin:admin_companyevent_list')
            else:
                messages.warning(self.request,"Error occured! Event not edited!")
                return render(self.request, "admin/collaborations/create_events.html",{'edit':True,'form': form, 'event':event})
        
        except Exception as e:
            print("@@@ Exception at Edit Company Event ", e)
            return redirect("admin:admin_companyevent_list")


class CustomerEventList(View):
	def get(self, *agrs, **kwargs):
            result ={}
            try:
                if 'by_status' in self.request.GET:
                    result = filter_by('status',[self.request.GET['by_status']], CompanyEvent.objects.all())
                elif 'by_company' in self.request.GET:
                    result = FilterByCompanyname(self.request.GET.getlist('by_company'), CompanyEvent.objects.all())
                else:
                    result = SearchByTitle_All('Event', self.request)
                data = get_paginated_data(self.request, result['query'])

                eventcompanies = []
                for comp in Company.objects.all():
                    if comp.companyevent_set.count() > 0:
                        eventcompanies.append(comp)
                
                return render(self.request, "frontpages/news/customer_event_list.html", {'events':data, 'message':result['message'],  'message_am':result['message_am'],'event_companies':eventcompanies})
            except Exception as e:
                print("@@@ Exception at Customer Event List, ",e)
                return redirect("/")
        
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


@login_required
def AjaxEventParticipation(request, id):
    messages = []
    data = json.loads(request.body) 
    try:  
        event = get_object_or_404( CompanyEvent, id = id)
        cropped = data['notify_on'][:10]
        selected_date = datetime.datetime.strptime( cropped, '%Y-%m-%d')
        if (event.start_date.date()<= selected_date.date() and selected_date.date() <= event.end_date.date() ):
            older = EventParticipants.objects.filter(event = event, patricipant_email = data['participant_email']).first()
            if older:
                older.notify_on = selected_date
                older.notified = False
                older.save()
                message = f"Updated The Reminder For The Email {data['participant_email']}! \n The system will remind you on {cropped}"
            else:
                participant = EventParticipants(user = request.user, event= event, patricipant_email=data['participant_email'], notify_on=selected_date)
                participant.save()
                message = f"New Reminder Saved For The Email {data['participant_email']}!  \n The system will remind you on {cropped}"
            return JsonResponse({'error':False, "message": message }, safe = False)
        else:
            return JsonResponse({'error':True, "message": f"You inserted Invalid date, \n Make sure that you choose a date between {event.start_date.date()} and {event.end_date.date()}" }, safe = False)


    except Exception as e:
        print("Exception occured while trying to paricipate in event", e)
        return JsonResponse({'error':True,"message":f"Exception occured while registering, "}, safe = False)

    
#12345  use ajax for event participation.
class EventParticipation(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):   
        try:  
            event = get_object_or_404( CompanyEvent, id = self.kwargs['id'])
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
@method_decorator(decorators,name='dispatch')
class CreateDocument(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            return render(self.request, "admin/document/create_document.html", {'form':DocumentForm})
        except Exception:
            return redirect("admin:error_404")

    def post(self, args, **kwargs):
        try:
            form = DocumentForm(self.request.POST)
            if form.is_valid():
                document = form.save(commit=False)
                document.created_by = self.request.user
                document.document =  self.request.FILES['document']
                document.save()
                messages.success(self.request,'Successfully created the document!')
                return redirect("/admin/list_document_by_category/all/")
            else:
                messages.warning(self.request,'Could not create the document!' )
                return render(self.request, "admin/document/create_document.html", {'form':form})
        except Exception as e:
            print("@@@ Exception at CreateDocument ", e)
            return redirect("admin:index")
        

@method_decorator(decorators,name='dispatch')
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
            document.title = self.request.POST['title']
            document.category = self.request.POST['category']
            if self.request.FILES:
                document.document =  self.request.FILES['document']
            document.last_updated_by = self.request.user
            document.last_updated_date = timezone.now()
            document.save()
            messages.success(self.request,'Successfully Edited the document!')
            return render(self.request, f"admin/document/list_document_by_category.html", {'documents':Document.objects.filter(category = document.category), 'categories': Document.DOC_CATEGORY})
        except Exception as e:
            messages.warning(self.request, "Document not Edited!")
            return render(self.request, "admin/document/list_document_by_category.html", {'categories':Document.DOC_CATEGORY}) 


@method_decorator(decorators,name='dispatch')      
class DocumentListing(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        documents = []
        try:     
            if self.kwargs['option'] != 'all':
                documents =  Document.objects.filter( category = self.kwargs['option'] , company=self.request.user.get_company())
                if documents.count() != 0:
                    return render(self.request, "admin/document/list_document_by_category.html", {'documents':documents, 'categories':Document.DOC_CATEGORY})
                else:
                    messages.warning(self.request, f"No documents for {self.kwargs['option']}")
            return render(self.request, "admin/document/list_document_by_category.html", {'categories':Document.DOC_CATEGORY})
        except Exception as e:
            print("exceptio at document list ",e)
            return redirect("admin:error_404")


def get_weekly_and_old(queryset):
    try:
        unnotified = queryset.filter(subscriber_notified = False)
        week_dates  = [ timezone.now().date() - timedelta(days = d) for d in range(8)] #since we also need to subtract 7 days, the range has to b 8
        this_week_objects = unnotified.filter( created_date__date__in= week_dates )
        week_obj_ids = [obj.id for obj in this_week_objects]
        return {'error':False, "this_week_objects": this_week_objects, "all": unnotified}
    except Exception as e:
        return {'error':True, 'message':str(e)}


def send_blogs(request):
    blogs = get_weekly_and_old(Blog.objects.filter(publish = True))
    news = get_weekly_and_old(News.objects.all())
    if blogs['error']==False:
        if news['error'] == False:
            week_blogs_count = blogs['this_week_objects'].count()
            blogs= blogs['all']
            week_news_count = news['this_week_objects'].count()
            news = news['all']
            try:
                current_site = get_current_site(request)
                from accounts.models import Subscribers
                subscribers_email =[ s.email for s in Subscribers.objects.filter(is_active = True)]
                mail_subject = f'Latest News and Blogs From FBPIDI'
                context = {
                    'blogs': blogs,
                    'week_blogs_count':week_blogs_count,
                    'news':news,
                    'week_news_count':week_news_count,
                    'domain': current_site.domain,
                    'fbpidi': Company.objects.get(main_category='FBPIDI'),
                    'unsubscribe_link':'unsubscribe',
                    'redirect_url':'activate_subscribtion'
                }
                from django.core.mail import EmailMessage
                from django.template.loader import render_to_string,get_template

                message = get_template('email/news_email.html').render(context)
                email = EmailMessage( mail_subject, message, to=subscribers_email)
                email.content_subtype = "html"
                # email.send(fail_silently=False)
                # print("Inquiry Replay message sent to Email ", inquiry.sender_email)
                return render(request, 'email/news_email.html', context)
            except Exception as e:
                print("Exception While Sending Inquiry Email ", str(e))
                return redirect("/")

        else:
            print("news error", news['message'])
            return redirect("/")
    else:
        print("news error", news['message'])
        return redirect("/")
    