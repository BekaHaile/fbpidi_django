from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from collaborations.models import PollsQuestion, PollsResult, Choices, Tender, News, NewsImages
from rest_framework.decorators import permission_classes
from collaborations.api.serializers import PollListSerializer, PollDetailSerializer, ChoiceSerializer, NewsListSerializer, NewsDetailSerializer
from django.contrib.auth.mixins import LoginRequiredMixin

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


#     queryset = News.objects.all()
#     serializer_class = NewsListSerializer

class NewsDetailApiView(generics.RetrieveAPIView):
    def get(self, request, id = None):
        news = News.objects.get(id = id)
        return Response( NewsDetailSerializer(news).data)






        


