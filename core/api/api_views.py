
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status, generics, authentication, permissions
from rest_framework.decorators import permission_classes, authentication_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from admin_site.models import Category,SubCategory
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer

from collaborations.models import News
from collaborations.api.serializers import NewsListSerializer

from company.models import Company
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer

from product.models import Product, ProductImage, ProductPrice
from product.api.serializer import ProducteFullSerializer, ProductInfoSerializer, ProductImageSerializer

from accounts.models import User, Customer, CompanyAdmin
from accounts.api.serializers import CustomerCreationSerializer, CustomerDetailSerializer

class ApiIndexView(APIView):
    def get(self, request):
        return Response ( data = {
            'products':ProductInfoSerializer(Product.objects.all(), many = True).data,
            'category': CategorySerializer( Category.objects.all(), many = True).data,
            'sub_category': SubCategorySerializer( SubCategory.objects.all(), many = True).data,
            'news_list': NewsListSerializer( News.objects.all(), many = True).data,
            'NEWS_CATAGORY': News.NEWS_CATAGORY     
            }
        )
    
#product-by-category/  request.data['category_id']
class ApiProductByCategoryView(APIView):
     def get(self, request):
         products = Product.objects.filter(category = request.data['category_id'])
         return Response(
             data ={'count': products.count(),
                 'products': ProductInfoSerializer(products, many = True).data
               },
            status = status.HTTP_200_OK
         )


class ApiProductDetailView(APIView):
    def get(self, request):
        try:
            product = get_object_or_404(Product, id = request.data['id'])
            return Response( data = {'error':False, 'product':ProducteFullSerializer(product ).data},)
        except Http404:
            return Response(data = {'error': True, 'message':'Product Not Found!'})
        


#product-by-main-category/ request.data['category']
class ApiProductByMainCategory(APIView):
    def get(self, request):
        category= request.data['category']
        products = []
        if category == "all":
            products=Product.objects.all()
        else:
            products = Product.objects.filter(category__category_name__category_type = category)
        return Response( data = { 'error':False, 'count':len(products), 
                                'products': ProductInfoSerializer(products, many = True).data},
                                 status = status.HTTP_200_OK
                        )

#client/comp-by-main-category/
class ApiCompanyByMainCategoryList(APIView):   
    #  request.data['company_type'] should be = manufacturer or supplier, request[product_category = "Beverage", "Food", "Pharmaceuticals", "all"]
    def get(self,request): 
        product_category = request.data['product_category']
        companies = Company.objects.filter(company_type= request.data['company_type']) #all companies with 
        if product_category != "all": # if it is "Beverage" or "Food" or "Pharmaceuticals"
            companies = companies.filter(product_category__category_name__category_type = product_category)
        return Response(
            data = {'error':False, 'count' : companies.count(), 'companies': CompanyInfoSerializer(companies, many =True).data},
            status= status.HTTP_200_OK)


class ApiCompanyDetailView(APIView):
    @permission_classes((IsAuthenticated))
    def get(self, request):
        try:
            company = get_object_or_404(Company, id = request.data['id'])
            return Response(data= CompanyFullSerializer( company ).data)
        except Http404:
            return Response(data = {"error":True, "message": "Company Not Found!"})
        

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
        user_detail = Customer.objects.get(user=request.user)
        user = User.objects.get(id=request.user.id)
        
        if request.data['first_name'] != None:
            user.first_name = request.data['first_name']
        if request.data['last_name'] != None:
            user.last_name = request.data['last_name']
        if request.data['phone_number'] != None:
            user.phone_number = request.data['phone_number']
        if request.data['email'] != None:
            user.email = request.data['email']
            
        if self.request.FILES.get('profile_image') != None:
            user.profile_image = request.FILES.get('profile_image')
            user_detail.profile_image = request.FILES.get('profile_image')
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


    


