
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status, generics, authentication, permissions
from rest_framework.decorators import permission_classes, authentication_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from admin_site.models import Category, UserTracker
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer

from collaborations.models import News
from collaborations.api.serializers import NewsListSerializer

from company.models import Company
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer

from product.models import SubCategory,Product, ProductImage, ProductPrice
from product.api.serializer import ProductFullSerializer, ProductInfoSerializer, ProductImageSerializer

from accounts.models import User,UserProfile, Customer, CompanyAdmin
from accounts.api.serializers import CustomerCreationSerializer, CustomerDetailSerializer

class ApiIndexView(APIView):
    def get(self, request):
        total_companies = Company.objects.all().count()
        total_products = Product.objects.all().count()
        happy_customers = Customer.objects.all().count()
        total_viewers = UserTracker.objects.all().count()
        return Response ( data = {
            'products':ProductInfoSerializer(Product.objects.all()[:10], many = True).data,
            'category': CategorySerializer( Category.objects.all(), many = True).data,
            'sub_category': SubCategorySerializer( SubCategory.objects.all(), many = True).data,
            'news_list': NewsListSerializer( News.objects.all()[:10], many = True).data,
            'NEWS_CATAGORY': News.NEWS_CATAGORY,
            'total_companies':total_companies,'total_products':total_products,'happy_customers':happy_customers,'total_viewers':total_viewers     
            }
        )

class ApiTotalViewerData(APIView):
    def get(self, request):
        try:
            total_companies = Company.objects.all().exclude(main_category="FBPIDI").count()
            total_products = Product.objects.all().count()
            happy_customers = UserProfile.objects.all().count()
            total_viewers = UserTracker.objects.all().count()
            return Response (data ={'error':False, 'total_companies':total_companies  ,'total_products':total_products,'happy_customers':happy_customers,'total_viewers':total_viewers})
        except Exception as e:
            print("@@@@@ Exception at ApiTatalViewerData ",e)
            return Response (data = {'error':True, 'message':str(e)})
    
class ApiProfileView(APIView):
    # authentication_classes  = ([TokenAuthentication])
    permission_classes = ([IsAuthenticated])
    def get(self, request):
        try:
            user_detail = get_object_or_404(Customer, user = request.user)
            return Response ( data={'error':False, 'user_detail': CustomerDetailSerializer(user_detail).data}, status=status.HTTP_200_OK )
        except Http404:
            return Response(data = {"error": True, 'message':"Customer Not Found!"})
    def post(self, request ):
        try:
            user_detail = Customer.objects.get(user=request.user)
            user = UserProfile.objects.get(id=request.user.id)
            
            if request.data['first_name'] != None:
                user.first_name = request.data['first_name']
            if request.data['last_name'] != None:
                user.last_name = request.data['last_name']
            if request.data['phone_number'] != None:
                user.phone_number = request.data['phone_number']
            if request.data['email'] != None:
                user.email = request.data['email']
                
            if 'profile_image' in self.request.data and self.request.data['profile_image'] != None:
                user.profile_image = request.data['profile_image']
                user_detail.profile_image = request.data['profile_image']
            user.save()
            if request.data['address'] != None:
                user_detail.address = request.data['address']
            if request.data['city'] != None:
                user_detail.city = request.data['city']
            if request.data['postal_code'] != None:
                user_detail.postal_code = request.data['postal_code']
            if request.data['country'] != None:
                user_detail.country = request.data['country']
            if request.data['facebook_link'] != None:
                user_detail.facebook_link = request.data['facebook_link']
            if request.data['google_link'] != None:
                user_detail.google_link = request.data['google_link']
            if request.data['twitter_link'] != None:
                user_detail.twiter_link = request.data['twitter_link']
            if request.data['pinterest_link'] != None:
                user_detail.pintrest_link = request.data['pinterest_link']
            if request.data['bio'] != None:
                user_detail.bio = request.data['bio']
            user_detail.save()
            return Response(data  ={'error':False, 'user': CustomerDetailSerializer(user_detail).data})
        except Exception as e:
            return Response(data = {'error':True, 'message':str(e)})



