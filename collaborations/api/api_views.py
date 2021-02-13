from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


#the following 3 work
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes,api_view

from rest_framework import authentication, permissions
from collaborations.models import (PollsQuestion, PollsResult, Choices, News, NewsImages, Blog, BlogComment,
                                    Announcement, AnnouncementImages, Tender, TenderApplicant, Faqs, JobApplication, 
                                    JobCategory, Project, Research, ResearchProjectCategory, Vacancy, ForumQuestion,
                                    ForumComments, CommentReplay)

from company.models import Company, CompanyEvent, EventParticipants


from collaborations.api.serializers import (PollListSerializer, PollDetailSerializer, ChoiceSerializer, NewsListSerializer, NewsDetailSerializer, 
                                            EventListSerializer, BlogSerializer, BlogCommentSerializer, AnnouncementSerializer, AnnouncementDetailSerializer, 
                                            TenderSerializer,TenderApplicantSerializer)
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

class PollListApiView(generics.ListAPIView):
    #for the future we will override the get_queryset() method to filter 
    queryset = PollsQuestion.objects.all()
    serializer_class = PollListSerializer

class PollDetailApiView( APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id = None):
        user = request.user
        poll = PollsQuestion.objects.get(id = id)
        data = {}
        if user == poll.user:
            data['error'] = True
            data['message'] = "You can not vote on this poll, since you are the creator of the poll."
            return Response()
        elif PollsResult.objects.filter(user = user , poll=poll).exists():
            data['error'] = True
            data['message'] = "You already have voted for this poll."           
        else:
            data['error'] = False
        data['data'] = PollDetailSerializer(poll).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, id = None):
            data = {}
            try:
                selected_choice = Choices.objects.get( id = request.data['selected_choice'])
                poll = PollsQuestion.objects.get(id = id)
                result = PollsResult(user = request.user, poll=poll, choice=selected_choice, remark= request.data['remark'])
                result.save()
                data['message'] = 'Successfully Voted!'
                return Response(data, status=status.HTTP_201_CREATED)

            except Exception as e:
                data['error'] = True
                data['message'] = f"Exception Occuered: {str(e)}"
                return Response(data, status=status.HTTP_304_NOT_MODIFIED)
           
class NewsListApiView(APIView):

    def get(self, request):
        data = {}
        try:
            data['news_list'] = NewsDetailSerializer( News.objects.all(), many = True).data
            data['news_category'] = News.NEWS_CATAGORY
            data['error'] = False
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data['error'] = True
            data['message'] = f"Exceptin Occured: {str(e)}"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)     


class NewsDetailApiView(generics.RetrieveAPIView):
    def get(self, request, id = None):
        news = News.objects.get(id = id)
        return Response( NewsDetailSerializer(news).data)


class EventListApiView(APIView):
    def get(self, request):
        try:
            data = {'event_list': EventListSerializer(CompanyEvent.objects.all(), many = True).data, 'error': False}
            return Response( data, status=status.HTTP_200_OK )
        except Exception as e:
            data= {'error' :True, 'message':f"Exception Occured: {str(e)}"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class EventDetailApiView(APIView):
    def get(self, request, id = None):
        event = CompanyEvent.objects.get(id = id)
        return Response( EventListSerializer(event).data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def EventNotifyApiView(request, id = None):
            if request.data['email'] and request.data['notify_in']:
                notify_in = int(request.data['notify_in'])
                event = CompanyEvent.objects.get(id = id)
                participant = EventParticipants(user =request.user, event= event,
                                                patricipant_email=request.data['email'])
                #??? Real comparison
                if event.start_date.month <= datetime.datetime.now().month:
                    if notify_in <=  event.start_date.day - datetime.datetime.now().day: 
                        participant.notified= False
                        participant.notifiy_in = notify_in
                        try:
                            participant.save()
                        except Exception as e:
                            return Response(data={'error':True, 'message':'You aleard have registered for a notification.'}, status = status.HTTP_205_RESET_CONTENT)
                        return Response(data={'error':False}, status=status.HTTP_201_CREATED)     
                else:
                    return Response(data={'error':True, 'message':'Invalid Date to notify'}, status = status.HTTP_205_RESET_CONTENT)

            return Response(data={'error':True, 'message':'Invalid Date to notify'}, status = status.HTTP_205_RESET_CONTENT)

            

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
        return Response( data = {'blogs':BlogSerializer(blog, many = True).data, 'tags':get_blog_tags()})

class ApiBlogDetail(APIView):
    def get(self, request):
        blog = Blog.objects.get(id = request.data['id'])
        return Response(data = {'count_comment': blog.countComment(), 'blog':BlogSerializer(blog).data,
                                'comments': BlogCommentSerializer(blog.comments(), many = True ).data 
                               })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ApiCreateBlogComment(request):
    blog = Blog.objects.get(id = request.data['id'])
    comment = BlogComment(blog=blog, sender = request.user, content = request.data['content'])
    comment.save()
    return Response(data = {'error':False, 'message':"Successfully Commented on blog!"})


# announcement-list/  
class ApiAnnouncementList(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

# announcement-detail/  request.data['id']
class ApiAnnouncementDetail(APIView):
    def get(self, request):
        if request.data['id']:
            try:
                announcement = get_object_or_404(Announcement,id=int(request.data['id']))
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
            tender = get_object_or_404(Tender, id = int(request.data['id']))
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