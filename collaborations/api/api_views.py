import datetime
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes, authentication_classes,api_view

from company.models import Company, CompanyEvent, EventParticipants
from company.api.serializers import CompanyInfoSerializer, CompanyNameSerializer


from collaborations.models import (PollsQuestion, PollsResult, Choices, News, NewsImages, Blog, BlogComment,
                                    Announcement, AnnouncementImages, Tender, TenderApplicant, Faqs, JobApplication, 
                                    JobCategory, Project, Research, ResearchAttachment, ResearchProjectCategory, Vacancy, ForumQuestion,
                                    ForumComments, CommentReplay, Faqs)
from collaborations.forms import CreateJobApplicationForm, ForumQuestionForm, CommentForm, CommentReplayForm, ResearchForm
from collaborations.api.serializers import (PollListSerializer,PollDetailSerializer,  ChoiceSerializer, NewsListSerializer, NewsDetailSerializer, JobApplicationCreationSerializer,
                                            EventListSerializer, BlogSerializer,BlogDetailSerializer, BlogCommentSerializer, AnnouncementSerializer, AnnouncementDetailSerializer, 
                                            TenderSerializer,TenderApplicantSerializer, VacancyListSerializer, JobCategorySerializer,ResearchCreationSerializer,ForumCommentCreationSerializer,
                                            ResearchProjectCategorySerializer, ProjectSerializer, ResearchSerializer, ForumCreationSerializer,CommentReplayCreationSerializer,
                                            ForumQuestionSerializer, ForumDetailSerializer, ForumCommentSerializer, CommentReplay, FaqSerializer, JobApplicationSerializer)


### a dictionay holding model names with model objects, Used to hold a model object for a string
models = { 'Research':Research,'Announcement':Announcement, 'Blog':Blog, 'BlogComment':BlogComment, 'Choice':Choices, 'Event':CompanyEvent, 'Tender':Tender, 'TenderApplicant':TenderApplicant, 
            'Forums':ForumQuestion, 'Forum Comments':ForumComments, 'Polls':PollsQuestion, 'News':News, 'Vacancy':Vacancy, 'Job Application':JobApplication, 'Job Category':JobCategory }


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
        if not 'by_title' in request.query_params: #not searching, just displaying latest news 
            query  = model.objects.all()
            return { 'query': query, 'message': f" {model_name} ",  'message_am': f" {model.model_am} "} # 3 Polls Found!
        else:   #if there is a filter_key list
            filter_key = request.query_params['by_title']
            query = model.objects.filter( Q(title__icontains = filter_key) | Q(title_am__icontains = filter_key) |Q(description__icontains = filter_key ) | Q(description_am__icontains = filter_key) ).distinct() 
            # if there is no match for the filter_key or there is no filter_key at all
            if query.count() == 0: 
                return { 'query': [], 'message': f"No match containing '{filter_key}'!", 'message_am': f"ካስገቡት ቃል '{filter_key}' ጋር የሚገናኝ አልተገኘም፡፡ !" }       
            return { 'query': query, 'message': f"{query.count()} result found!", 'message_am': f"{query.count()} ውጤት ተገኝቷል!" }
    except Exception as e:
        print("Exception at SearchBYTitle_All", str(e))
        return {'query':[], 'message':'Exception occured!'}


def FilterByCompanyname(company_list,  query_set):
    try:
        q_object = Q()
        for company_name in company_list:
            q_object.add( Q(company__name__icontains = company_name ), Q.OR )
            q_object.add( Q(company__name_am__icontains = company_name ), Q.OR )
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
    category_name =  request.query_params['by_category'].split(',')[:-1]
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
    accepts field_name like category or title etc and filter keys like ['Food','Beverage'] and filters from a query
    """
    kwargs ={}
    q= Q()  
    for value in field_values:
        if value == 'All':
            break
        print(field_name," ",value)
        kwargs ['{0}__{1}'.format(field_name, 'contains')] = value
        q.add(Q(**kwargs),Q.OR)
        kwargs = {}
    result = query.filter(q)
    
    if not result.count() == 0:
        return {'query':result,'message':f"{result.count()} result found!",'searched_category':'All','message_am':f"{result.count()} ተገኝቷል! " ,'searched_name': field_name }
    return {'query':result, 'message':f"No results Found!", 'message_am':f" ምንም ውጤት አልተገኘም፡፡ !" ,'searched_category':'All', 'searched_name': field_name }

# returns paginated data from a query set
def get_paginated_data(request, query):
    page_number = request.query_params.get('page', 1)
    try:
        return Paginator(query, 1).page(page_number)
    except Exception as e:
        print("exception at get_paginate_data ",e)
        return Paginator(query, 2).page(1)


def get_paginator_info(paginated_data):
    try:
        context = {'page_range': list(paginated_data.paginator.page_range), 'current':paginated_data.number, 'next': paginated_data.next_page_number() if paginated_data.has_next() else None , 'previous' :paginated_data.previous_page_number() if paginated_data.has_previous() else None,  } 
        return context 
    except Exception as e:
        print('!!!!!!!!!!!!!!!!! Exception in geting paginator info',e)
        return {} 


class PollListApiView(generics.ListAPIView):
    def get(self, request):
        result ={}
        try:
            if 'by_company' in request.query_params:
                result = FilterByCompanyname(request.query_params['by_company'].split(',')[:-1], PollsQuestion.objects.all())
            elif 'by_no_vote' in request.query_params:
                result['query'] = PollsQuestion.objects.annotate(num_vote=Count('pollsresult')).order_by('-num_vote')
                if result['query'].count() > 0:
                    result['message'] = "Polls in order of number of votes!"
                    result['message_am'] = "በመራጮች ብዛት ቅደም ተከተል"
                else:
                    result['message'] = "No result Found!"
                    result['message_am'] = "ምንም ውጤት አልተገኘም"
            else:
                result = SearchByTitle_All('Polls', request) # this returns all if there is no search key or filter by search
            companies = []
            for comp in Company.objects.all():
                if comp.pollsquestion_set.count()>0:
                    companies.append(comp)
            if result['query']==0:
                result['message'] = 'No Result Found!'

            paginated = get_paginated_data(request, result['query'])
            return Response( data = {'error':False, 'paginator':get_paginator_info(paginated), 'polls':PollListSerializer(paginated, many =True).data, 'message' : result['message'], 
                                        'message_am':result['message_am'],'companies':CompanyNameSerializer(companies, many =True).data})

        except Exception as e:
            print("exception at polls list ",e)
            return Response({'error':True, 'message':str(e)})


class PollDetailApiView( APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            id = request.query_params['id']
            poll = get_object_or_404(PollsQuestion, id = id)
        except Http404:
            return Response(data = {'error':True, 'message':"Poll object not Found!"})
        data = {'data': PollDetailSerializer(poll).data}
        if user == poll.created_by:
            data['error'] = True
            data['message'] = "You can not vote on this poll, since you are the creator of the poll."
            return Response(data)
        elif PollsResult.objects.filter(user = user , poll=poll):
            data['error'] = True
            data['message'] = "You already have voted for this poll." 
            return Response(data)          
        else:
            data['error'] = False
            return Response(data)
        return Response(data = {'data':data})
        
    def post(self, request):
            try:
                selected_choice = Choices.objects.get( id = request.data['selected_choice'])
                poll = PollsQuestion.objects.get(id = request.data['id'])
            except Http404:
                return Response(data={'error':True, 'message':'poll or selected choice not Found'})
            try:
                result = PollsResult(user = request.user, poll=poll, choice=selected_choice, remark= request.data['remark'])
                result.save()
                return Response(data = {'error':False, 'message':"Successfully Voted!"})
            except Exception as e:
                return Response(data={'error':True,'message': f"can't vote twice! ,{str(e)}"})


class NewsListApiView(APIView):
    def get(self, request):
        
        result = []
        try:
            if 'by_category' in request.query_params and 'by_title' in request.query_params:
                result = SearchCategory_Title('News', request)
                paginated = get_paginated_data(request, result['query'])
                return Response(data= {'error':False, 'paginator':get_paginator_info(paginated), 'news_list':NewsDetailSerializer( paginated, many = True).data, 'message':result['message'],  'message_am':result['message_am'],'NEWS_CATAGORY':News.NEWS_CATAGORY})
            elif 'by_category' in request.query_params:
                result = filter_by('catagory', request.query_params['by_category'].split(',')[:-1], News.objects.all())
            elif 'by_company' in request.query_params:
                result = FilterByCompanyname(request.query_params['by_company'].split(',')[:-1], News.objects.all())
            else: 
                result = SearchByTitle_All('News', request)

            paginated = get_paginated_data(request, result['query'])
            context = {'error':False,'paginator': get_paginator_info(paginated), 'news_list': NewsDetailSerializer(paginated, many = True).data, 'message':result['message'],  'message_am':result['message_am'], 'NEWS_CATAGORY':News.NEWS_CATAGORY}
            return Response(data= context )
            
        except Exception as e:
            return Response(data = {'error': True, 'message': f"Exceptin Occured: {str(e)}"})
   

class NewsDetailApiView(generics.RetrieveAPIView):
    def get(self, request, ):
        try:
            news = get_object_or_404( News, id = request.query_params['id'])
            return Response( data  = {'error' : False, 'news':NewsDetailSerializer(news).data} )
        except Http404:
            return Response(data = {"error":True, 'message':"News Object not Found!"})


class EventListApiView(APIView):
    def get(self, request):
        try:
            if 'by_status' in request.query_params:
                result = filter_by('status',[request.query_params['by_status']], CompanyEvent.objects.all())
            elif 'by_company' in request.query_params:
                result = FilterByCompanyname(request.query_params['by_company'].split(',')[:-1], CompanyEvent.objects.all())
            else:
                result = SearchByTitle_All('Event', request)

            eventcompanies = []
            for comp in Company.objects.all():
                if comp.companyevent_set.count() > 0:
                    eventcompanies.append(comp)       
            
            paginated = get_paginated_data(request, result['query'])
            return Response( data = { 'error': False, 'paginator': get_paginator_info(paginated), 'event_list': EventListSerializer( paginated, many = True).data, 'message':result['message'],  'message_am':result['message_am'],'companies':CompanyNameSerializer( eventcompanies,many =True).data}, status=status.HTTP_200_OK )
        
        except Exception as e:
            return Response(data={'error' :True, 'message':f"Exception Occured: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class EventDetailApiView(APIView):
    def get(self, request):
        try:
            event = get_object_or_404( CompanyEvent, id = request.query_params['id'])
            return Response( data = {'error':False, 'event':EventListSerializer(event).data})
        except Http404:
            return Response(data = {'error':True, 'Message': 'Event Not Found!'})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def EventNotifyApiView(request):   
                if request.data['email'] and request.data['notify_on'] and request.data['id'] :
                    event = CompanyEvent.objects.get(id = request.data['id'])
                    older = EventParticipants.objects.filter(event = event, patricipant_email = request.data['email']).first()
                    if older:
                        older.notify_on = request.data['notify_on']
                        older.notified = False
                        older.save()
                    else:
                        participant = EventParticipants(user =request.user, event= event, patricipant_email= request.data['email'], notify_on=request.data['notify_on'])
                        participant.save()
                    return Response(data={'error':False}, status=status.HTTP_201_CREATED)
                return Response(data={'error':True, 'message':'Email, event id and number of days to notify are required!'}, status = status.HTTP_205_RESET_CONTENT)
      

def set_message(result):
		if result['query'].count()==0:
			result['message'] = 'No Result Found!'
			result['message_am'] = "ምንም ውጤት አልተገኘም"
		else:
			result['message'] = f"{result['query'].count()} result found !"
			result['message_am']  = f"{result['query'].count()} ውጤት ተገኝቷል"
		return result


def get_tags(lang):
		blog = Blog.objects.filter(publish=True) 
		string = ""
		if(lang=="amharic"):
			for b in blog:
				string+=b.tag_am+','
		if(lang=="english"):
			for b in blog:
				string+=b.tag+','
		string = string[:-1]
		tag_list = string.split(',')
		tag_list = set(tag_list)
		return tag_list


class ApiBlogList(APIView):
    def get(self, request):
        result ={}
        if 'by_company' in request.query_params:
            result = FilterByCompanyname(request.query_params['by_company'].split(',')[:-1], Blog.objects.filter(publish=True))
        else:
            result['query'] = Blog.objects.filter(publish = True)
            if 'by_title' in request.query_params:
                q = Q( Q(title__icontains = request.query_params['by_title']) | Q(title_am__icontains = request.query_params['by_title']) )
                result['query'] = result['query'].filter(q)
                result = set_message(result)
            elif 'by_tag' in request.query_params:
                q = Q( Q(tag__icontains = request.query_params['by_tag']) | Q(tag_am__icontains = request.query_params['by_tag']) )
                result['query'] = result['query'].filter(q)
                result = set_message(result)
            else:
                result['query'] = Blog.objects.filter(publish=True)
                result['message']  = "Blogs"
                result['message_am'] = Blog.model_am
        tags = get_tags("english")
        tags_am = get_tags("amharic")
        companies = []
        for comp in Company.objects.all():
            if comp.blog_set.count() > 0:
                companies.append(comp)
        paginated = get_paginated_data(request, result['query'])
        return Response( data = {'error':False, 'paginator':get_paginator_info(paginated), 'blogs':BlogSerializer(paginated, many = True).data, 'message':result['message'],  
                                'message_am':result['message_am'],'companies': CompanyNameSerializer(companies,many = True).data,'tags':tags,'tags_am':tags_am})


class ApiBlogDetail(APIView):
    def get(self, request):
        try:    
            blog = get_object_or_404( Blog, id = request.query_params['id'])
            return Response(data = {'error':False, 'count_comment': blog.countComment(), 'blog':BlogDetailSerializer(blog).data   })
        except Http404:
            return Response(data = {'error':True, 'message': 'Blog Not Found!'})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiBlogCommentAction(request):
    try:
        if request.data['option'] == "create":
            try:
                blog = Blog.objects.get(id = request.data['blog'])
            except Exception as e:
                return Response(data = {'error':True, 'message':"Blog Not Found!"})
            comment = BlogComment(blog=blog, created_by = request.user, content = request.data['content'])
            comment.save()
            return Response(data = {'error':False, 'message':"Successfully Commented on blog!", 'blog':BlogDetailSerializer(blog).data})
        else: #for edit and delete
            try:
                blog_comment = get_object_or_404(BlogComment, id =request.data['id'] )
            except Http404:
                return Response(data = {'error':True, 'message':"Object doesn't Exist"})
            if blog_comment.created_by == request.user:
                if request.data['option'] == "edit":
                    blog_comment.content = request.data['content']
                    blog_comment.last_updated_date = timezone.now()
                    blog_comment.save() 
                    return Response(data = {'error':False, 'blog':BlogDetailSerializer(blog_comment.blog).data})
                else:
                    blog = blog_comment.blog
                    blog_comment.delete()
                    return Response(data = {'error':False, 'blog':BlogDetailSerializer(blog).data})
            else:
                return Response(data = {'error':True, 'message':"You have no permission to chage this Comment!"})
    except Exception as e:
        return Response(data = {'error':True, 'message':f'{str(e)}'})


# announcement-list/  
class ApiAnnouncementList(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    def get(self, request):
        try:
            result = {}
            if 'by_company' in request.query_params:
                result = FilterByCompanyname(request.query_params['by_company'].split(',')[:-1], Announcement.objects.all())
            else:
                result = SearchByTitle_All('Announcement', request)
            if result['query']  :
                result['query'] = Announcement.objects.all()
            paginated = get_paginated_data(request, result['query'])
            companies = []
            for comp in Company.objects.all():
                if comp.announcement_set.count() > 0:
                    companies.append(comp)
            return Response(data = {'error':False, 'paginator':get_paginator_info(paginated), 'object_list':AnnouncementSerializer(paginated, many = True).data, 'message':result['message'], 'message_am':result['message_am'], 'companies':CompanyNameSerializer( companies,many =True).data})
        except Exception as e:
            print ("##Exception in Announcement list ",e)
            return Response(daa = {'error':True, 'message':e})
            
    
# announcement-detail/  request.query_params['id']
class ApiAnnouncementDetail(APIView):
    def get(self, request):
        if request.query_params['id']:
            try:
                announcement = get_object_or_404(Announcement,id=int(request.query_params['id']))
            except Exception:
                return Response({'error':True, 'message': "Announcement object not Found!"})

        return Response (data = { 'error':False, 
            'announcement': AnnouncementDetailSerializer( announcement).data })


class ApiTenderList(APIView):
    def get(self, request):
        try:
            result = {}       
            if 'by_status' in request.query_params:
                result = filter_by('status', [ request.query_params['by_status'] ], Tender.objects.all())
            elif 'by_company' in request.query_params:
                by_company = FilterByCompanyname(request.query_params['by_company'].split(',')[:-1],  Tender.objects.all())
                result = filter_by('status', ['Open', 'Upcoming'], by_company['query'])
            elif 'by_document_type' in request.query_params:
                by_type = filter_by('tender_type', [request.query_params['by_document_type'] ],  Tender.objects.all())
                result = filter_by('status', ['Open', 'Upcoming'], by_type['query'])
            elif 'by_title' in request.query_params:
                by_title=Tender.objects.filter( Q(title__icontains=request.query_params['by_title'])|Q(title_am__icontains=request.query_params['by_title']) ).distinct()
                result = filter_by('status', ['Open', 'Upcoming'], by_title)
            else:
                result['query'] = Tender.objects.filter( Q(status='Open') | Q(status = 'Upcoming') )
                if result['query'].count() > 0:
                    result['message'] = f"{result['query'].count()} result Found"
                    result['message_am'] = f"{result['query'].count()} ተገኝቷል!"
                else:
                    result['message'] = "No result Found"
                    result['message_am'] = "ምንም ውጤት አልተገኝም!"

            companies = []
            for comp in Company.objects.all():
                if comp.tender_set.count() > 0:
                    companies.append(comp)
            
            paginated = get_paginated_data(request, result['query'])
            return Response(data = {'error':False, 'paginator':get_paginator_info(paginated), 'tenders':TenderSerializer(paginated, many =True).data, 'companies': CompanyNameSerializer(companies, many = True).data, 'message':result['message'], 'message_am':result['message_am']} )
            
        except Exception as e:
            print( "Error while getting tenders",e)
            return Response(data = {'error':False, 'tenders':TenderSerializer(Tender.objects.all(), many = True).data}, status=status.HTTP_200_OK)
    

class ApiTenderDetail(APIView):
    def get(self, request):
        try:
            tender = get_object_or_404(Tender, id = int(request.query_params['id']))
        except Http404:
            return Response(data = {'error': True , 'message':'Tender object does not exist!'})
        return Response(data = {'error':False, 'tender':TenderSerializer(tender).data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            get_object_or_404(Tender, id = request.data['tender'])
            serializer =TenderApplicantSerializer(data = request.data) 
            if serializer.is_valid():
                applicant = serializer.save()
                return Response(data = {'error':False, 'applied':True, 
                                        'tender': TenderSerializer( Tender.objects.get(id = request.data['tender'])).data})
        except Exception as e:
            print("Exception ", str(e))
            return Response(data = {'error':True, 'applied':False, 'message': 'Please Fill the form with valid data!'})


class ApiVacancyList(APIView):
    def get(self, request):
        
        result = []
        jobcatetory = JobCategory.objects.all()
        companies = []
        for comp in Company.objects.all():
            if comp.vacancy_set.count()>0:
                companies.append(comp)

        if 'by_category' in request.query_params and 'by_title' in request.query_params:
            q= Q( Q(title__contains = request.query_params['by_title']) | 
                    Q(title_am__contains = request.query_params['by_title']) )
            query = Vacancy.objects.filter(q)# search by title then filter by category
            result = filter_by('category__category_name',request.query_params['by_category'].split(',')[:-1], query)
        elif 'by_category' in request.query_params:
            result = filter_by('category__category_name', request.query_params['by_category'].split(',')[:-1], Vacancy.objects.all())
        elif 'by_company' in request.query_params:
            result = FilterByCompanyname(request.query_params['by_company'].split(',')[:-1], Vacancy.objects.all())
        else: 
            result = SearchByTitle_All('Vacancy', request)
        
        paginated = get_paginated_data(request, result['query'])
        return Response(data = {'error':False, 'paginator':get_paginator_info(paginated), 'vacancies': VacancyListSerializer(paginated, many= True).data, 'jobcategory':JobCategorySerializer(jobcatetory, many = True).data,
                                'message':result['message'],  'message_am':result['message_am'], 'companies':CompanyNameSerializer( companies, many = True).data})


class ApiVacancyDetail(APIView):
    def get(self, request):
        try:
            vacancy = get_object_or_404(Vacancy, id = int(request.query_params['id']))
            jobcategory = JobCategory.objects.all()
        except Http404:
            return Response(data = {'error': True , 'message':'Vacancy object does not exist!'})
        return Response(data = {'error':False, 'vacancy':VacancyListSerializer(vacancy).data, 'jobcategory': JobCategorySerializer(jobcategory, many = True).data} )
    
    #12345 applying for vacancy can be handled here , first z front end will make the user to login to apply
    def post(self, request):
        pass


class ApiVacancyApplication(APIView):
    authentication_classes = ([TokenAuthentication])
    permission_classes = ([IsAuthenticated])
    def get(self, request):
        try:
            vacancy = get_object_or_404(Vacancy, id = int(request.query_params['id']))
            if JobApplication.objects.filter(vacancy=vacancy, created_by=request.user).exists():
                return Response(data = {'error':True, 'message': "You can't apply to the same vacancy Twice"})
            jobcategory = JobCategory.objects.all()
        except Http404:
            return Response(data = {'error': True , 'message':'Vacancy Not Found!'})
        
        return Response( data = {'error':False, 'vacancy': vacancy.id, 'current_status':JobApplication.CURRENT_STATUS,
                                                'jobcategory': JobCategorySerializer(jobcategory, many = True).data})

    def post(self, request):
        try:
            vacancy = get_object_or_404(Vacancy, id = int(request.data['id']))
            if JobApplication.objects.filter(vacancy=vacancy, created_by=request.user).exists():
                return Response(data = {'error':True, 'message': "You can't apply to the same vacancy Twice"})
        except Http404:
            return Response(data = {'error': True , 'message':'Vacancy Not Found!'})
        serializer = JobApplicationCreationSerializer(data=request.data)
        if serializer.is_valid():
            application =  serializer.create(validated_data=request.data)
            application.created_by = request.user
            application.save()
            return Response(data = {'error':False, 'application': JobApplicationSerializer(application).data })
        else:
            return Response(data ={'error':True, 'message': f"{serializer.errors}"} )

        # try:
        #     vacancy = get_object_or_404(Vacancy, id = int(request.data['id']))
        #     if JobApplication.objects.filter(vacancy=vacancy, created_by=request.user).exists():
        #         return Response(data = {'error':True, 'message': "You can't apply to the same vacancy Twice"})
        # except Http404:
        #     return Response(data = {'error': True , 'message':'Vacancy Not Found!'})
        # form = CreateJobApplicationForm(request.POST,request.FILES)
        # if form.is_valid():
        #     application =  form.save(commit=False)
        #     application.created_by = request.user
        #     application.cv = request.data['cv']
        #     application.
        #     application.vacancy =  Vacancy.objects.get(id =request.data['id'])
        #     application.save()
        #     return Response(data = {'error':False, 'application': JobApplicationSerializer(application).data })
        # else:
        #     return Response(data ={'error':True, 'message': form.errors}, )


def get_user_created_researchs(request):
        return [] if  request.user.is_anonymous else Research.objects.filter(created_by = request.user)

class ApiResearchList(APIView):
    def get(self, request):
        try:
            researchs = Research.objects.filter(accepted="APPROVED")
            category = ResearchProjectCategory.objects.all()
            user_created = get_user_created_researchs(request)	
            result = {}
            if 'by_category' in request.query_params:
                result = filter_by("category__cateoryname",request.query_params['by_category'].split(',')[:-1], Research.objects.filter(accepted="APPROVED"))
            elif 'by_title' in request.query_params:
                q = Research.objects.filter(title__icontains = request.query_params['by_title'], accepted="APPROVED").distinct()
                if q.count()>0:
                    result ={ 'query':q, 'message':f"{q.count()} Result found!",'message_am':f"{q.count()} ውጤት ተገኝቷል!"}
                else:
                    result = {'query':[],'message':"No result found!",'message_am':"ምንም ውጤት አልተገኘም!"}
            else:
                result = {'query':Research.objects.filter(accepted="APPROVED"),'message':"Researchs",'message_am':"ምርምር"}

            paginated = get_paginated_data(request, result['query'])
            return Response(data = {'error':False, 'paginator':get_paginator_info(paginated) ,'researchs': ResearchSerializer(paginated, many = True).data, "user_created": ResearchSerializer(user_created, many = True).data,
                                    'message':result['message'], 'message_am':result['message_am'],'category':ResearchProjectCategorySerializer(category, many = True).data})
        except Exception as e:
            return Response({'error': True, 'message' : e})

##didn't include try except while getting research obj because, in api, id is sent by the code when users click a button
class ApiResearchDetail(APIView):
    def get(self, request):
        try:
            research = get_object_or_404( Research, id = request.query_params['id'])
            category = ResearchProjectCategory.objects.all()
        except Http404:
            return Response(data ={'error':True, 'message':"Object Doesn't Exist"})
        user_created = get_user_created_researchs(request)
        return Response(data = {'error':False, 'research': ResearchSerializer(research).data, "user_created": ResearchSerializer(user_created, many = True).data,
                                'category':ResearchProjectCategorySerializer(category, many = True).data})


class ApiCreateResearch(APIView):
    authentication_classes =([TokenAuthentication])
    permission_classes =([IsAuthenticated])
    def get(self, request):
        category = ResearchProjectCategory.objects.all()
        user_created = get_user_created_researchs(request)
        return Response(data = {'error':False, 'category':ResearchProjectCategorySerializer(category, many = True).data, 
                                'user_created':ResearchSerializer(user_created,many = True).data})
    
    def post(self, request):
        try:
            serializer = ResearchCreationSerializer(data =request.data)
            if serializer.is_valid():
                research = serializer.create(validated_data=request.data)
                research.created_by = request.user
                research.accepted = "PENDING" if request.user.is_customer else "APPROVED"
                research.save()
                if 'attachements' in request.data:
                    print("attachements found!")
                    attachement = ResearchAttachment(research = research, attachement = request.data['attachements'])
                    attachement.save()
                return Response(data = {'error':False, 'research': ResearchSerializer(research).data})
            return Response(data ={'error':True, 'message': f"Invaid inputs to create a research!{form.errors}"})
        except Exception as e:
            return Response(data ={'error':True, 'message':f"exception occured {str(e)}"})

        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiResearchAction(request): 
    # edit depending on request.data['option']
        try:
            try:
                 research= get_object_or_404(Research, id = request.data['id'])
            except Http404:
                return Response(data={'error':True, 'message': 'Research object not Found!' })
            
            if research.created_by == request.user:
                if request.data['option'] == 'delete':
                    research.delete()
                    return Response(data = {'error':False, 'researchs':ResearchSerializer( Research.objects.all(),many =True ).data})  

                elif request.data['option'] == 'edit':
                    research.title = request.data['title']
                    research.description = request.data['description']
                    research.detail = request.data['detail']
                    status = request.data['status']
                    category = request.data['category']
                    research.last_updated_by= request.user
                    research.last_updated_date = timezone.now()
                    research.save()
                    if 'attachements' in request.data and request.data['attachements'] != '':
                        doc = research.researchattachment_set.first() 
                        doc.attachement= request.data['attachements'] 
                        doc.timestamp = timezone.now()
                        doc.save()    
                    return Response(data= {'error':False, 'research': ResearchSerializer(research).data})
            else:
                return Response( data = {'error':True, 'message': "You can't edit others comment" })
        except Exception as e:
            return Response(data = {'error':True, 'messsage':f"Invalid Inputs {str(e)}"})  


class ApiProjectList(APIView):
    def get(self, request):
        pass


def get_user_created_forums(request):
    return [] if  request.user.is_anonymous else ForumQuestion.objects.filter(created_by = request.user)


class ApiForumQuestionList(APIView):
    def get(self, request):
        try:
            user_created = get_user_created_forums(request)
            if 'by_title' in request.query_params:
                query = ForumQuestion.objects.filter(title__icontains = request.query_params['by_title'])
                if query.count() > 0:
                    result = {'query':query, 'message':f'{query.count()} result found!', 'message_am':f'{query.count()} ውጤቶች ተገኝተዋል' }
                else:
                    result = {'query':ForumQuestion.objects.all()[:5], 'message':'No result found!', 'message_am':'ምንም ውጤት አልተገኘም' }
            else:
                result = {'query':ForumQuestion.objects.all()[:5], 'message':'Forums', 'message_am':'ውይይቶች' }

            paginated = get_paginated_data(request, result['query'])
            return Response(data = {'error':False, 'paginator': get_paginator_info(paginated), 'forums':ForumQuestionSerializer(paginated, many = True).data, 
                            'user_created':ForumQuestionSerializer(user_created, many = True).data,'message':result['message'], 'message_am':result['message_am'] })
        except Exception as e:
            print('Exception in ApiForumQuestionList ', e)
            return Response(data = {'error':True, 'message':e})


class ApiForumQuestionDetail(APIView):
    def get(self, request):
        try:
            forum = get_object_or_404(ForumQuestion, id = request.query_params['id'])
            user_created = get_user_created_forums(request) #if forum was created user
        except Http404:
            return Response(data = {'error':True, 'message': "Forum object not found"})
        return Response(data = {'error':False, 'forum':ForumDetailSerializer(forum).data, 'user_created':ForumDetailSerializer(user_created, many = True).data})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiCreateForumQuestion(request): 
    #create or edit depending on request.data['option']
        try:
            if request.data['option'] == 'create':
                serializer = ForumCreationSerializer(data = request.data)
                if serializer.is_valid():
                    forum = serializer.create(validated_data = request.data)
                    forum.created_by = request.user
                    if 'attachements' in request.data:
                        forum.attachements = request.data['attachements']
                    forum.save()
            else:#if option = 'edit' or 'delete'
                try:
                    forum = get_object_or_404(ForumQuestion, id = request.data['id'])
                except Http404:
                    return Response(data={'error':True, 'message': 'Forum object not Found!' })
                if forum.created_by == request.user and request.data['option'] == 'delete':
                    forum.delete()
                    return Response(data = {'error':False, 'forums':ForumQuestionSerializer( ForumQuestion.objects.all(),many =True ).data})  

                elif forum.created_by == request.user and request.data['option'] == 'edit':
                    forum.title = request.data['title']
                    forum.description = request.data['description']
                    if 'attachements' in request.data and request.data['attachements'] != '':
                        forum.attachements = request.data['attachements']
                    forum.last_updated_by= request.user
                    forum.last_updated_date = timezone.now()
                    forum.save()        
                else:
                    return Response( data = {'error':True, 'message': "You can't edit others comment" })
         
            return Response(data= {'error':False, 'forum': ForumDetailSerializer(forum).data})
        except Exception as e:
            return Response(data = {'error':True, 'messsage':f"Invalid Inputs {str(e)}"})  


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiCommentAction(request): 
        #create or edit depending on request.data['option']
        try:
            
            if request.data['option'] == 'create':
                try:
                    forum_question = get_object_or_404(ForumQuestion, id = request.data['forum_question'])
                except Http404:
                    return Response(data = {'error':True, 'message':'Forum Not Found!'})
                serializer = ForumCommentCreationSerializer(data = request.data)
                if serializer.is_valid():
                    comment = serializer.create(validated_data=request.data) 
                    comment.created_by = request.user
                    comment.save()
                else:
                    return Response(data= {'error':True, 'message':str(serializer.errors)}) 

            else:#if option = 'edit' or delete
                try:
                    comment = get_object_or_404(ForumComments, id = request.data['id'])
                except Http404:
                    return Response(data={'error':True, 'message': 'Comment object not Found!' })

                if comment.created_by == request.user and request.data['option'] == 'delete':
                    forum = comment.forum_question
                    comment.delete()
                    return Response(data={'error':False, 'forum':ForumDetailSerializer(forum).data})
                elif comment.created_by == request.user and request.data['option'] == 'edit':
                    comment.comment = request.data['comment']
                    comment.last_updated_by = request.user
                    comment.last_updated_date = timezone.now()
                    comment.save()
                else:
                    return Response(data = {'error':True, 'message':"You can't edit others comment!"})  
            
            return Response(data= {'error':False, 'forum': ForumDetailSerializer(comment.forum_question).data})
        except Exception as e:
            return Response(data = {'error':True, 'messsage':f"Invalid Inputs {str(e)}"})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiCommentReplayAction(request): 
        #create or edit depending on request.data['option']
        
        try:
            if request.data['option'] == 'create':
                try:
                    comment = get_object_or_404(ForumComments, id = request.data['comment'])
                except:
                    return Response(data={'error':True, 'message': 'comment object not Found!' })
                serializer =CommentReplayCreationSerializer(data = request.data)
                if serializer.is_valid():
                    reply = serializer.create(request.data)
                    reply.created_by= request.user
                    reply.save()
                else:
                    return Response(data = {'error':True, 'message':'Invalid input {str(serializer.errors)}'})
            else:#if option = 'edit' or delete
                try:
                    reply = get_object_or_404(CommentReplay, id = request.data['id'])
                except Http404:
                    return Response(data={'error':True, 'message': 'Reply object not Found!' })
                if reply.created_by == request.user and request.data['option'] == 'delete':
                    forum = reply.comment.forum_question
                    reply.delete()
                    return Response(data={'error':False, 'forum':ForumDetailSerializer(forum).data})
                elif reply.created_by == request.user and request.data['option'] == 'edit':
                    reply.content = request.data['content']
                    reply.last_updated_by = request.user
                    reply.last_updated_date = timezone.now()
                    reply.save()
                else:
                    return Response(data = {'error':True, 'message':"You can't edit others reply!"})  
            return Response(data= {'error':False, 'forum': ForumDetailSerializer(reply.comment.forum_question).data})
        except Exception as e:
            return Response(data = {'error':True, 'messsage':f"Invalid Inputs {str(e)}"})


class ApiFaq(APIView):
    def get(self, request):
        try:
            if 'by_title' in request.query_params:
                title = request.query_params['by_title']
                query = Faqs.objects.filter( Q(questions__icontains = title) | Q(questions_am__icontains = title)).filter(status ="APPROVED")
            elif 'by_company' in request.query_params:
                company = request.query_params['by_company']
                query = Faqs.objects.filter(Q(company__name = company) | Q(company__name_am = company) ).filter(status ="APPROVED")
            else:
                query = Faqs.objects.filter(status ="APPROVED")
            paginated = get_paginated_data(request, query)
            if query.count() == 0:
                return Response(data ={'error':False, 'paginator':get_paginator_info(paginated), 'faqs':[], 'message':'No result found!', 'message_am':'ምንም ውጤት አልተገኘም'})
            
            return Response(data ={'error':False, 'paginator':get_paginator_info(paginated), 'faqs':FaqSerializer(paginated, many =True).data, 'message': f"{query.count()} result found!", "message_am":f"{query.count()} ውጤት ተገኝቷል"})
            
        except Exception as e:
            return Response (data = {'error':True, 'message':f"{str(e)}"})





