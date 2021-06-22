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

from company.models import Company, InvestmentProject,CompanyLike
from company.api.serializers import CompanyInfoSerializer, CompanyFullSerializer, InvestmentProjectserializer, CompanyMessageSerializer

from product.models import SubCategory,Product, ProductImage, ProductPrice
from product.api.serializer import ProductFullSerializer, ProductInfoSerializer, ProductImageSerializer

from accounts.models import User, Customer, CompanyAdmin
from accounts.api.serializers import CustomerCreationSerializer, CustomerDetailSerializer

from collaborations.api.api_views import get_paginated_data, get_paginator_info
#api/comp-by-main-category/

def user_liked_companies(user):
    if user.is_authenticated:
        likes = CompanyLike.objects.filter(user = user)
        return [l.company.id for l in likes]
    return []


class ApiUserLikedCompanies(APIView):
    def get(self, request):
        try:
            return Response(data = {'error':False, 'liked_companies':user_liked_companies(request.user)})
        except Exception as e:
            return Response(data = {'error':True, 'message':str(e)})


class ApiCompanyByMainCategoryList(APIView):   
    #  request[main_category = "Beverage", "Food", "Pharmaceuticals", "All"]
    def get(self,request): 
        main_category = request.query_params['main_category']  
        if ',' in main_category:# if multiple categories are selected
            categories = request.query_params['main_category'].split(',')[:-1]
            companies =    Company.objects.filter(main_category__in = categories,stage=False).exclude(main_category="FBPIDI")
        elif main_category != "All":
            companies = Company.objects.filter(main_category = main_category,stage=False).exclude(main_category="FBPIDI")
        else:
            companies = Company.objects.all().exclude(main_category="FBPIDI",stage=False)
        if 'by_title' in request.query_params:
            companies = companies.filter(   Q( Q(name__icontains=request.query_params['by_title']) | Q(name_am__icontains=request.query_params['by_title']) | 
                                                Q(company_product__name=request.query_params['by_title'])) & Q(is_active = True)).distinct().exclude(main_category="FBPIDI")
        paginated = get_paginated_data(request, companies)
        subsectors = Category.objects.all()
        return Response(data = {'error':False, 'paginator':get_paginator_info(paginated), 'count' : companies.count(), 'companies': CompanyInfoSerializer(paginated, many =True).data, 'liked_companies':user_liked_companies(request.user),
                                'message':'Companies', 'message_am': 'ድርጅቶች', 'sub_sectors': CategorySerializer(subsectors, many = True).data})


class ApiSearchCompany(APIView):
    def get(self,request):
        try:
            companies = Company.objects.filter(stage=False)
            if 'by_title' in request.query_params:
                companies = Company.objects.filter(Q(name__icontains=request.query_params['by_title'])|Q(name_am__icontains=request.query_params['by_title'])|Q(company_product__name=request.query_params['by_title']),stage=False).exclude(main_category="FBPIDI").distinct()
            if 'by_subsector' in request.query_params:
                companies = companies.filter(category__id=request.query_params['by_subsector'],stage=False).exclude(main_category="FBPIDI")
            # companies = companies.exclude(main_category='FBPIDI') #if this were on top of the first if, it means it has to fetch data just to exclude it
            paginated = get_paginated_data(request, companies)
            subsectors = Category.objects.all()
            count = companies.count()
            return Response(data = {'error':False, 'paginator':get_paginator_info(paginated), 'count' : count, 'companies': CompanyInfoSerializer(paginated, many =True).data, 'liked_companies': user_liked_companies(request.user),
                                    'message':f'{count} result found!', 'message_am': f'{count} ውጤት ተገኝቷል!', 'sub_sectors': CategorySerializer(subsectors, many = True).data})
        except Exception as e:
            print("Exception inside ApisearchCompany ",e)
            return Response(data = {'error':True, 'message':str(e)})


class ApiCompanyDetailView(APIView):
    def get(self, request):
        try:
            company = get_object_or_404(Company, id = request.query_params['id'])
            data = CompanyFullSerializer( company ).data
            data['liked_company'] = user_liked_companies(request.user)
            
            return Response(data= data)
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


      
class ApiLikeCompany(APIView):
    def get(self, request):
        try:
            company = Company.objects.get (id= int(request.query_params['c_id'] ))
            if CompanyLike.objects.filter(  user = request.user, company = company ).exists():
                return Response( data={'error':True, 'message':"Already Liked Company"})
            c_like = CompanyLike(user = request.user, company = company   )
            c_like.save()
            return Response({'error':False})

        except Exception as e:
            print("########Exception at Like_Company ",e)
            return Response({'error':True})


class ApiDislikeCompany(APIView):
    def get(self, request):
        try:
            c_like = CompanyLike.objects.filter(user = request.user, company = Company.objects.get (id= int(request.query_params['c_id'] ))).first()
            if c_like:
                c_like.delete()
            return Response({'error':False})

        except Exception as e:
            print("########Exception at DislikeCompany ",e)
            return Response({'error':True, 'message':str(e)})


class ApiCompanyUs(APIView):
    def get(self, request):
        try:
            return Response( data={'error':False, 'company':CompanyFullSerializer(Company.objects.get(id = request.query_params['c_id'])).data } )
        except Exception as e:
            return Response(data={'error':True, 'message':str(e)})


class ApiContactCompany(APIView):
    def get(self, request):
        try:
            return Response( data={'error':False, 'company':CompanyInfoSerializer(Company.objects.get(id = request.query_params['c_id'])).data } )
        except Exception as e:
            return Response(data={'error':True, 'message':str(e)})
        
    def post(self, request):
        try:
            serializer = CompanyMessageSerializer(data = request.data)
            if serializer.is_valid():
                contact = serializer.create(validated_data = request.data)
                contact.save()
                return Response(data = {'error':False,  })
            else:
                return Response(data = {'error':True, 'message': serializer.errors})
        except Exception as e:
            return Response(data = {'error':True, 'message':str(e)})



