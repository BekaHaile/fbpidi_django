from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from collaborations.models import PollsQuestion, PollsResult, Choices, Tender
from rest_framework.decorators import permission_classes
from collaborations.api.serializers import PollCreationSerializer, PollSerializer, ChoiceSerializer

class PollsApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PollSerializer
    queryset = PollsQuestion.objects.all()



class PollApiView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # @permission_classes((IsAuthenticated))
    def get(self, request): #listing polls doesnot require login
        data = {}
        if request.user.is_superuser or request.user.is_company_admin:
            data['polls'] = PollSerializer( PollsQuestion.objects.all(), many = True ).data
        return Response(data, status=status.HTTP_200_OK)

    @permission_classes((IsAuthenticated))
    def post(self, request):
            data = {}
            serializer = PollCreationSerializer(data = request.data)
            if serializer.is_valid():
                user = request.user
                poll = serializer.save(user)
                data['data'] =  serializer.data
                data['message'] = "Successfully registered a new Poll."
               
            else:
                data = serializer.errors
            return Response(data)

class ChoicesApiView(generics.ListCreateAPIView):
    queryset = Choices.objects.all()
    serializer_class = ChoiceSerializer
         
class ChoicesView(APIView):
    def get(self, request, id=None):
        serializer = ChoiceSerializer(Choices.objects.get(id = id))
        data['data'] = serializer.data
        return Response(data)
        
    
    def post(self, request, id=None ):
        data = {}
        serializer = ChoiceSerializer(data = request.data)
        if serializer.is_valid():
            choice = serializer.save()
            poll = PollsQuestion.objects.get(id = id)
            poll.choices.add(choice)
            poll.save()
            data['data'] =  serializer.data
            data['response'] = "Successfully registered a new choice."       
        else:
            data = serializer.errors
        return Response(data)
    
    def put(self, request, id=None):
        data = {}
        serializer = ChoiceSerializer(data = request.data)
        if serializer.is_valid():
            choice = Choices.objects.get(id = id)
            choice = serializer.update(instance = choice, validated_data=request.data)
            data['data']= ChoiceSerializer(choice).data
            data['response'] = "Successfully updated a  choice."
            
        else:
            data = serializer.errors
        return Response(data)




        


