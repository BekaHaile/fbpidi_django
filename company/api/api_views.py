from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status, generics, authentication, permissions
from rest_framework.decorators import permission_classes, authentication_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from admin_site.models import Category
from admin_site.api.serializers import CategorySerializer, SubCategorySerializer

from collaborations.models import News
from collaborations.api.serializers import NewsListSerializer

from company.models import Company, InvestmentProject
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer, InvestmentProjectserializer

from product.models import SubCategory,Product, ProductImage, ProductPrice
from product.api.serializer import ProducteFullSerializer, ProductInfoSerializer, ProductImageSerializer

from accounts.models import User, Customer, CompanyAdmin
from accounts.api.serializers import CustomerCreationSerializer, CustomerDetailSerializer


#api/comp-by-main-category/
class ApiCompanyByMainCategoryList(APIView):   
    #  request.query_params['company_type'] should be = manufacturer or supplier, request[product_category = "Beverage", "Food", "Pharmaceuticals", "all"]
    def get(self,request): 
        product_category = request.query_params['product_category']    
        companies = []
        # companies = Company.objects.filter(company_type= request.query_params['company_type']) #all companies with 
        if product_category != "all": # if it is "Beverage" or "Food" or "Pharmaceuticals"
            companies = Company.objects.filter(category__category_type = product_category  )
        else:
            companies = Company.objects.all()
            # companies = companies.filter(product_category__category_name__category_type = product_category)
        return Response(
            data = {'error':False, 'count' : companies.count(), 'companies': CompanyInfoSerializer(companies, many =True).data},
            status= status.HTTP_200_OK)


class ApiCompanyDetailView(APIView):
    def get(self, request):
        try:
            company = get_object_or_404(Company, id = request.query_params['id'])
            return Response(data= CompanyFullSerializer( company ).data)
        except Http404:
            return Response(data = {"error":True, "message": "Company Not Found!"})


class ApiProject(APIView):
    def get(self, request):
        try:
            projects = InvestmentProject.objects.all()
            return Response(data = {'error':False, 'projects': InvestmentProjectserializer(projects, many = True).data})
        except Exception as e:
            return Response(data ={'error':True, 'message':str(e)})

class ApiProjectDetail(APIView):
    def get(self, request):
        try:
            project = InvestmentProject.objects.get(id = request.query_params['id'])
            return Response(data = {'error':False, 'project': InvestmentProjectserializer(project).data})
        except Exception as e:
            return Response(data ={'error':True, 'message':str(e)})
