#imports for Restframework
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from accounts.models import User,Company,CompanyAdmin,Customer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, CompanyAdminSerializer, CustomerCreationSerializer
from rest_framework.authtoken.models import Token

class CompanyAdminSignUpView(APIView):
     def post(self, request):
            data = {}
            user_serializer = UserSerializer (data = request.data)
            if user_serializer.is_valid():
                #before saving the user object check if the company_admin data is valid
                companyadmin_serializer = CompanyAdminSerializer(data = request.data)
                if companyadmin_serializer.is_valid():

                    # I'm using user_serializer.create instead of .save, because if the user is saved, but somehow 
                    # the companyAdmin serializer got some error in the save method, the user object will be created
                    # but now saved, so, the system will return exception, without saving any user obj!! 
                    user = user_serializer.create(validated_data =request.data) 
                    companyadmin = companyadmin_serializer.save(user = user)    
                    data['response'] = "Successfully registered a new Company Admin user."
                    data['companyadmin']  = CompanyAdminSerializer(companyadmin).data
                    data['token'] = Token.objects.get(user = user).key
                else:
                    data = companyadmin_serializer.errors
            else:
                data = user_serializer.errors
            return Response(data)

class CustomerSignUpView(APIView):
    def post(self, request):
            data = {}
            user_serializer = UserSerializer (data = request.data)
            if user_serializer.is_valid():
                #before saving the user object check if the company_admin data is valid
                customer_serializer = CustomerCreationSerializer(data = request.data)
            
                if customer_serializer.is_valid():
                        user = user_serializer.create(validated_data = request.data) 
                        customer = customer_serializer.save(user = user)    
                        data['response'] = "Successfully registered a new Customer user."
                        data['customer']  = CustomerCreationSerializer(customer).data
                        data['token'] = Token.objects.get(user = user).key
                   
                else:
                        data = customer_serializer.errors
                
            else:
                data = user_serializer.errors
            return Response(data)

class CompleteLogin(APIView):
    pass


##############3            
