from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q

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
from product.api.serializer import ProductFullSerializer, ProductInfoSerializer, ProductImageSerializer

from accounts.models import User, Customer, CompanyAdmin
from accounts.api.serializers import CustomerCreationSerializer, CustomerDetailSerializer

from collaborations.api.api_views import get_paginated_data, get_paginator_info
#api/comp-by-main-category/
class ApiCompanyByMainCategoryList(APIView):   
    #  request[main_category = "Beverage", "Food", "Pharmaceuticals", "All"]
    def get(self,request): 
        main_category = request.query_params['main_category']  
        if ',' in main_category:# if multiple categories are selected
            categories = request.query_params['main_category'].split(',')[:-1]
            companies =    Company.objects.filter(main_category__in = categories)
        elif main_category != "All":
            companies = Company.objects.filter(main_category = main_category)
        else:
            companies = Company.objects.all()
        paginated = get_paginated_data(request, companies)
        subsectors = Category.objects.all()
        return Response(data = {'error':False, 'paginator':get_paginator_info(paginated), 'count' : companies.count(), 'companies': CompanyInfoSerializer(paginated, many =True).data, 
                                'message':'Companies', 'message_am': 'ድርጅቶች', 'sub_sectors': CategorySerializer(subsectors, many = True).data})

class ApiSearchCompany(APIView):
    def get(self,request):
        try:
            companies = Company.objects.all()
            if 'by_title' in request.query_params:
                companies = Company.objects.filter(Q(name__icontains=request.query_params['by_title'])|Q(name_am__icontains=request.query_params['by_title'])|Q(company_product__name=request.query_params['by_title'])).distinct()
            if 'by_subsector' in request.query_params:
                companies = companies.filter(category__id=request.query_params['by_subsector'])
            # companies = companies.exclude(main_category='FBPIDI') #if this were on top of the first if, it means it has to fetch data just to exclude it
            paginated = get_paginated_data(request, companies)
            subsectors = Category.objects.all()
            count = companies.count()
            return Response(data = {'error':False, 'paginator':get_paginator_info(paginated), 'count' : count, 'companies': CompanyInfoSerializer(paginated, many =True).data, 
                                    'message':f'{count} result found!', 'message_am': f'{count} ውጤት ተገኝቷል!', 'sub_sectors': CategorySerializer(subsectors, many = True).data})
        except Exception as e:
            print("Exception inside ApisearchCompany ",e)
            return Response(data = {'error':True, 'message':str(e)})


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
