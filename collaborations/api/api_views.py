from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes,api_view


from rest_framework import authentication, permissions
from collaborations.models import (PollsQuestion, PollsResult, Choices, News, NewsImages, Blog, BlogComment,
                                    Announcement, AnnouncementImages, Tender, TenderApplicant, Faqs, JobApplication, 
                                    JobCategory, Project, Research, ResearchProjectCategory, Vacancy, ForumQuestion,
                                    ForumComments, CommentReplay, Faqs)
from collaborations.forms import CreateJobApplicationForm, ForumQuestionForm, CommentForm, CommentReplayForm, ResearchForm

from company.models import Company, CompanyEvent, EventParticipants


from collaborations.api.serializers import (PollListSerializer,  ChoiceSerializer, NewsListSerializer, NewsDetailSerializer, 
                                            EventListSerializer, BlogSerializer, BlogCommentSerializer, AnnouncementSerializer, AnnouncementDetailSerializer, 
                                            TenderSerializer,TenderApplicantSerializer, VacancyListSerializer, JobCategorySerializer,
                                            ResearchProjectCategorySerializer, ProjectSerializer, ResearchSerializer, 
                                            ForumQuestionSerializer, ForumDetailSerializer, ForumCommentSerializer, CommentReplay, FaqSerializer, JobApplicationSerializer
                                            )
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

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
        try:
            data['error'] = False
            data['news_list'] = NewsDetailSerializer( News.objects.all(), many = True).data
            data['news_category'] = News.NEWS_CATAGORY
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data['error'] = True
            data['message'] = f"Exceptin Occured: {str(e)}"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)     


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

    #    try:   
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

                    



            # if request.data['email'] and request.data['notify_on'] and request.data['id'] :
            #     id = request.data['id']
            #     notify_on = request.data['notify_on']
            #     event = CompanyEvent.objects.get(id = id)
            #     participant = EventParticipants(user =request.user, event= event,
            #                                     patricipant_email=request.data['email'])
            #     #??? Real comparison
            #     if event.start_date.month <= datetime.datetime.now().month:
            #         if notify_on <=  event.start_date.day - datetime.datetime.now().day: 
            #             participant.notified= False
            #             participant.notifiy_in = notify_on
            #             try:
            #                 participant.save()   # if the email has been previously registered, it will through an unique exception
            #             except Exception as e:
            #                 return Response(data={'error':True, 'message':'You aleard have registered for a notification.'}, status = status.HTTP_205_RESET_CONTENT)
                            
            #             return Response(data={'error':False}, status=status.HTTP_201_CREATED)  
                    
            #         else:
            #             return  Response(data={'error':True, 'message':'Invalid Date to notify'}, status = status.HTTP_205_RESET_CONTENT)
            #     else:
            #         return Response(data={'error':True, 'message':'Invalid month to notify'}, status = status.HTTP_205_RESET_CONTENT)

            # return Response(data={'error':True, 'message':'Email, event id and number of days to notify are required!'}, status = status.HTTP_205_RESET_CONTENT)

            
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
            return Response(data = {'error':False, 'count_comment': blog.countComment(), 'blog':BlogSerializer(blog).data,'comments': BlogCommentSerializer(blog.comments(), many = True ).data })
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



