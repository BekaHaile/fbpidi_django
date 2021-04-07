import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes, authentication_classes,api_view

from company.models import Company, CompanyEvent, EventParticipants
from collaborations.models import (PollsQuestion, PollsResult, Choices, News, NewsImages, Blog, BlogComment,
                                    Announcement, AnnouncementImages, Tender, TenderApplicant, Faqs, JobApplication, 
                                    JobCategory, Project, Research, ResearchProjectCategory, Vacancy, ForumQuestion,
                                    ForumComments, CommentReplay, Faqs)
from collaborations.forms import CreateJobApplicationForm, ForumQuestionForm, CommentForm, CommentReplayForm, ResearchForm
from collaborations.api.serializers import (PollListSerializer,  ChoiceSerializer, NewsListSerializer, NewsDetailSerializer, 
                                            EventListSerializer, BlogSerializer,BlogDetailSerializer, BlogCommentSerializer, AnnouncementSerializer, AnnouncementDetailSerializer, 
                                            TenderSerializer,TenderApplicantSerializer, VacancyListSerializer, JobCategorySerializer,
                                            ResearchProjectCategorySerializer, ProjectSerializer, ResearchSerializer, 
                                            ForumQuestionSerializer, ForumDetailSerializer, ForumCommentSerializer, CommentReplay, FaqSerializer, JobApplicationSerializer
                                            )


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
                query = model.objects.all()
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
    category_name =  request.query_params['by_category'].split(',')
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



class PollListApiView(generics.ListAPIView):
    #for the future we will override the get_queryset() method to filter 
    queryset = PollsQuestion.objects.all()
    serializer_class = PollListSerializer
    


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
        data = {'data': PollListSerializer(poll).data}
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
            data = {}
            try:
                selected_choice = Choices.objects.get( id = request.data['selected_choice'])
                poll = PollsQuestion.objects.get(id = request.data['id'])
            except Http404:
                return Response(data={'error':True, 'message':'poll or selected choice not Found'})
            try:
                result = PollsResult(created_by = request.user, poll=poll, choice=selected_choice, remark= request.data['remark'])
                result.save()
                data['message'] = 'Successfully Voted!'
                return Response(data = data)
            except Exception as e:
                data['error'] = True
                data['message'] = "can't vote twice!"
                return Response(data=data)


class NewsListApiView(APIView):
    def get(self, request):
        data = {}
        result = []
        try:
            if 'by_category' in request.query_params and 'by_title' in request.query_params:
                result = SearchCategory_Title('News', request)
                # data = get_paginated_data(request, result['query'])
                return Response(data= {'error':False, 'news_list':NewsDetailSerializer( result['query'], many = True).data, 'message':result['message'],  'message_am':result['message_am'],'NEWS_CATAGORY':News.NEWS_CATAGORY})
            elif 'by_category' in request.query_params:
                result = filter_by('catagory', request.query_params['by_category'].split(','), News.objects.all())
            elif 'by_company' in request.query_params:
                print("$$$$$$$$$$4 ",type(request.query_params['by_company'].split(',')))
                result = FilterByCompanyname(request.query_params['by_company'].split(','), News.objects.all())
            else: 
                result = SearchByTitle_All('News', request)

            if result['query'].count()==0:
                result['query'] = News.objects.all()
            # data = get_paginated_data(self.request, result['query'])
            # print("$$$$$$ ", request.query_params)
        
            # print("###########33", request.query_params['by_category'], ' ')
            # data['error'] = False
            # data['news_list'] = NewsDetailSerializer( News.objects.all(), many = True).data
            # data['news_category'] = News.NEWS_CATAGORY
            # return Response(data, status=status.HTTP_200_OK)
            return Response(data= {'error':False, 'news_list': NewsDetailSerializer( result['query'], many = True).data, 'message':result['message'],  'message_am':result['message_am'], 'NEWS_CATAGORY':News.NEWS_CATAGORY})
            
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
            data = { 'error': False,'event_list': EventListSerializer(CompanyEvent.objects.all(), many = True).data,}
            return Response( data, status=status.HTTP_200_OK )
        except Exception as e:
            data= {'error' :True, 'message':f"Exception Occured: {str(e)}"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


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

                    



            
def get_blog_tags():
        blog = Blog.objects.filter(publish = True)
        stringlist = []
        truestring = []
        for b in blog:
            splited = b.tag.split(" ")
            for split in splited:
                stringlist.append(split)
        taglist = set(stringlist)
        taglist = list(taglist)

        for string in taglist:
            if string == '':
                continue
            truestring.append(string)
        return truestring
    

class ApiBlogList(APIView):
    def get(self, request):
        blog = Blog.objects.filter(publish = True)
        return Response( data = {'error':False, 'blogs':BlogSerializer(blog, many = True).data, 'tags':get_blog_tags()})


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
def ApiCreateBlogComment(request):
    try:
        blog = Blog.objects.get(id = request.data['id'])
    except Exception:
        return Response(data = {'error':True, 'message':"Blog Not Found!"})
    comment = BlogComment(blog=blog, sender = request.user, content = request.data['content'])
    comment.save()
    return Response(data = {'error':False, 'message':"Successfully Commented on blog!"})


# announcement-list/  
class ApiAnnouncementList(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

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
        vacancies = Vacancy.objects.filter(closed = False)
        jobcatetory = JobCategory.objects.all()
        return Response(data = {'error':False, 'vacancies': VacancyListSerializer(vacancies, many= True).data,
                                'jobcategory':JobCategorySerializer(jobcatetory, many = True).data
                })


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
            if JobApplication.objects.filter(vacancy=vacancy, user=request.user).exists():
                return Response(data = {'error':True, 'message': "You can't apply to the same vacancy Twice"})
            jobcategory = JobCategory.objects.all()
        except Http404:
            return Response(data = {'error': True , 'message':'Vacancy Not Found!'})
        
        return Response( data = {'error':False, 'vacancy': vacancy.id, 'current_status':JobApplication.CURRENT_STATUS,
                                                'jobcategory': JobCategorySerializer(jobcategory, many = True).data})

    def post(self, request):
        try:
            vacancy = get_object_or_404(Vacancy, id = int(request.data['id']))
            if JobApplication.objects.filter(vacancy=vacancy, user=request.user).exists():
                return Response(data = {'error':True, 'message': "You can't apply to the same vacancy Twice"})
        except Http404:
            return Response(data = {'error': True , 'message':'Vacancy Not Found!'})
        form = CreateJobApplicationForm(request.POST,request.FILES)
        if form.is_valid():
            job =  form.save(commit=False)
            job.user = request.user
            job.vacancy =  Vacancy.objects.get(id =request.data['id'])
            job.save()
            return Response(data = {'error':False, 'application': JobApplicationSerializer(job).data })
        else:
            return Response(data ={'error':True, 'message': form.errors}, )


# def get_user_created_projects(request):   
#         return [] if  request.user.is_anonymous else Project.objects.filter(user = request.user, accepted="APPROVED")


def get_user_created_researchs(request):
        return [] if  request.user.is_anonymous else Research.objects.filter(user = request.user, accepted="APPROVED")

class ApiResearch(APIView):
    def get(self, request):
        researchs = Research.objects.filter(accepted="APPROVED")
        category = ResearchProjectCategory.objects.all()
        user_created = get_user_created_researchs(request)		
        return Response(data = {'error':False, 'researchs': ResearchSerializer(researchs, many = True).data, "user_created": ResearchSerializer(user_created, many = True).data,
                                'category':ResearchProjectCategorySerializer(category, many = True).data})

##didn't include try except while getting research obj because, in api, id is sent by the code when users click a button
class ApiResearchDetail(APIView):
    def get(self, request):
        research = Research.objects.get(id = request.query_params['id'])
        category = ResearchProjectCategory.objects.all()
        user_created = get_user_created_researchs(request)
        return Response(data = {'error':False, 'research': ResearchSerializer(research).data, "user_created": ResearchSerializer(user_created, many = True).data,
                                'category':ResearchProjectCategorySerializer(category, many = True).data})


class ApiCreateResearch(APIView):
    authentication_classes =([TokenAuthentication])
    permission_classes =([IsAuthenticated])
    def get(self, request):
        category = ResearchProjectCategory.objects.all()
        user_created = Research.objects.filter(user = request.user, accepted = "APPROVED")
        return Response(data = {'error':False, 'category':ResearchProjectCategorySerializer(category, many = True).data, 
                                'user_created':ResearchSerializer(user_created,many = True).data})
    
    def post(self, request):
        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            research = form.save(commit = False)
            if request.user.is_customer:
                research.accepted = "PENDING"
            else:
                research.accepted = "APPROVED"
            research.user = request.user
            if request.FILES:
                research.attachements = request.FILES['attachements']
            research.save()
            return Response(data = {'error':False, 'researchs': ResearchSerializer(research).data})
        return Response(data ={'error':True, 'message': f"Invaid inputs to create a research!{form.errors}"})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiResearchAction(request): 
    # edit depending on request.data['option']
        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid:    
            try:
                 research= get_object_or_404(Research, id = request.data['id'])
            except Http404:
                return Response(data={'error':True, 'message': 'Research object not Found!' })
            print(research.user.id, " ", request.user.id)   
            
            if research.user == request.user:
                if request.data['option'] == 'delete':
                    research.delete()
                    return Response(data = {'error':False, 'researchs':ResearchSerializer( Research.objects.all(),many =True ).data})  

                elif request.data['option'] == 'edit':
                    research.title = request.data['title']
                    research.description = request.data['description']
                    research.detail = request.data['detail']
                    status = request.data['status']
                    category = request.data['category']
                    if request.FILES:
                        research.attachements = request.FILES['attachements']  
                    research.save()   
                    return Response(data= {'error':False, 'research': ForumDetailSerializer(research).data})
        
            else:
                return Response( data = {'error':True, 'message': "You can't edit others comment" })
        else:
            return Response(data = {'error':True, 'messsage':"Invalid Inputs"})  



def get_user_created_forums(request):
    return [] if  request.user.is_anonymous else ForumQuestion.objects.filter(user = request.user)

class ApiForumQuestionList(APIView):
    def get(self, request):
        forum = ForumQuestion.objects.all()
        user_created = get_user_created_forums(request)
        return Response(data = {'error':False, 'forums':ForumQuestionSerializer(forum, many = True).data, 'user_created':ForumQuestionSerializer(user_created, many = True).data })


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
        form = ForumQuestionForm(request.POST, request.FILES)
        if form.is_valid:
            forum =ForumQuestion
            if request.data['option'] == 'create':
                forum = form.save(commit =False) #sets title and description
                forum.user = request.user
                if request.FILES:
                    forum.attachements = request.FILES['attachements']
            else:#if option = 'edit' or 'delete'
                try:
                    forum = get_object_or_404(ForumQuestion, id = request.data['id'])
                except Http404:
                    return Response(data={'error':True, 'message': 'Forum object not Found!' })
                if forum.user == request.user and request.data['option'] == 'delete':
                    forum.delete()
                    return Response(data = {'error':False, 
                                            'forums':ForumQuestionSerializer( ForumQuestion.objects.all(),many =True ).data})  

                elif forum.user == request.user and request.data['option'] == 'edit':
                    forum.title = request.data['title']
                    forum.description = request.data['description']
                    if request.FILES:
                        forum.attachements = request.FILES['attachements']        
                else:
                    return Response( data = {'error':True, 'message': "You can't edit others comment" })

            #save for forum object created at create and edit        
            forum.save()
            return Response(data= {'error':False, 'forum': ForumDetailSerializer(forum).data})
        else:
            return Response(data = {'error':True, 'messsage':"Invalid Inputs"})  


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiCommentAction(request): 
        #create or edit depending on request.data['option']
        form = CommentForm(request.POST, request.FILES)
        
        if form.is_valid:
            comment =ForumComments
            if request.data['option'] == 'create':
                try:
                    forum_question = get_object_or_404(ForumQuestion, id = request.data['forum_id'])
                except Http404:
                    return Response(data = {'error':True, 'message':'Forum Not Found!'})

                comment = form.save(commit =False) #sets title and description
                comment.user = request.user
                comment.forum_question = forum_question
                if request.FILES:
                    comment.attachements = request.FILES['attachements']  # saving is done at last (works for both create and edit)
            else:#if option = 'edit' or delete
                try:
                    comment = get_object_or_404(ForumComments, id = request.data['id'])
                except Http404:
                    return Response(data={'error':True, 'message': 'Comment object not Found!' })

                if comment.user == request.user and request.data['option'] == 'delete':
                    forum = comment.forum_question
                    comment.delete()
                    return Response(data={'error':False, 'forum':ForumDetailSerializer(forum).data})
                elif comment.user == request.user and request.data['option'] == 'edit':
                    comment.comment = request.data['comment']
                    if request.FILES:
                        comment.attachements = request.FILES['attachements']
                else:
                    return Response(data = {'error':True, 'message':"You can't edit others comment!"})  
            comment.save()
            return Response(data= {'error':False, 'forum': ForumDetailSerializer(comment.forum_question).data})
        else:
            return Response(data = {'error':True, 'messsage':"Invalid Inputs"})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiCommentReplayAction(request): 
        #create or edit depending on request.data['option']
        form = CommentReplayForm(request.POST, request.FILES)
        if form.is_valid:
            replay =CommentReplay
            if request.data['option'] == 'create':
                replay = form.save(commit =False) #sets content
                replay.user = request.user
                try:
                    replay.comment = ForumComments.objects.get(id = request.data['comment_id'])
                except:
                    return Response(data={'error':True, 'message': 'comment object not Found!' })
                if request.FILES:
                    replay.attachements = request.FILES['attachements']
            else:#if option = 'edit'
                try:
                    replay = get_object_or_404(CommentReplay, id = request.data['id'])
                except Http404:
                    return Response(data={'error':True, 'message': 'Reply object not Found!' })
                if replay.user == request.user and request.data['option'] == 'delete':
                    forum = replay.comment.forum_question
                    replay.delete()
                    return Response(data={'error':False, 'forum':ForumDetailSerializer(forum).data})
                elif replay.user == request.user and request.data['option'] == 'edit':
                    replay.content = request.data['content']
                    if request.FILES:
                        replay.attachements = request.FILES['attachements']
                else:
                    return Response(data = {'error':True, 'message':"You can't edit others replay!"})  
            replay.save()
            return Response(data= {'error':False, 'forum': ForumDetailSerializer(replay.comment.forum_question).data})
        else:
            return Response(data = {'error':True, 'messsage':"Invalid Inputs"})


class ApiFaq(generics.ListAPIView):
    queryset = Faqs.objects.all()
    serializer_class = FaqSerializer



